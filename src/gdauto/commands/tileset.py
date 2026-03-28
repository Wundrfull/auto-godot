"""TileSet creation and terrain automation."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

import rich_click as click

from gdauto.errors import GdautoError, ParseError, ValidationError
from gdauto.formats.tres import parse_tres_file, serialize_tres_file
from gdauto.formats.values import GodotJSONEncoder, serialize_value
from gdauto.output import GlobalConfig, emit, emit_error
from gdauto.tileset.builder import build_tileset


@click.group(invoke_without_command=True)
@click.pass_context
def tileset(ctx: click.Context) -> None:
    """TileSet creation and terrain automation."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())


def _parse_tile_size(s: str) -> tuple[int, int]:
    """Parse a 'WxH' string into (width, height) positive integers."""
    parts = s.lower().split("x")
    if len(parts) != 2:
        raise ValidationError(
            message=f"Invalid tile size format: {s}",
            code="INVALID_TILE_SIZE",
            fix="Use format WxH (e.g., 32x32)",
        )
    try:
        w, h = int(parts[0]), int(parts[1])
    except ValueError:
        raise ValidationError(
            message=f"Invalid tile size values: {s}",
            code="INVALID_TILE_SIZE",
            fix="Width and height must be integers (e.g., 32x32)",
        )
    if w <= 0 or h <= 0:
        raise ValidationError(
            message=f"Tile size must be positive: {s}",
            code="INVALID_TILE_SIZE",
            fix="Width and height must be positive integers",
        )
    return (w, h)


@tileset.command("create")
@click.argument("image", type=click.Path(exists=False))
@click.option(
    "--tile-size",
    type=str,
    required=True,
    help="Tile size as WxH (e.g., 32x32).",
)
@click.option("--columns", type=int, required=True, help="Number of tile columns.")
@click.option("--rows", type=int, required=True, help="Number of tile rows.")
@click.option(
    "--margin", type=int, default=0,
    help="Margin around the atlas edges in pixels. Default: 0.",
)
@click.option(
    "--separation", type=int, default=0,
    help="Separation between tiles in pixels. Default: 0.",
)
@click.option(
    "-o", "--output", type=click.Path(), default=None,
    help="Output .tres path. Default: <image_stem>.tres.",
)
@click.option(
    "--res-path", type=str, default=None,
    help="Godot res:// path for the texture. Default: res://<image filename>.",
)
@click.pass_context
def create(
    ctx: click.Context,
    image: str,
    tile_size: str,
    columns: int,
    rows: int,
    margin: int,
    separation: int,
    output: str | None,
    res_path: str | None,
) -> None:
    """Create a TileSet .tres from a sprite sheet image.

    Generates a Godot TileSet resource with a TileSetAtlasSource configured
    for the given tile dimensions, columns, and rows.
    """
    image_path = Path(image)
    if not image_path.exists():
        emit_error(
            GdautoError(
                message=f"File not found: {image}",
                code="FILE_NOT_FOUND",
                fix="Check the path to your sprite sheet image",
            ),
            ctx,
        )
        return

    try:
        tile_w, tile_h = _parse_tile_size(tile_size)
    except ValidationError as exc:
        emit_error(exc, ctx)
        return

    image_res = res_path or f"res://{image_path.name}"
    output_path = Path(output) if output else image_path.with_suffix(".tres")

    resource = build_tileset(image_res, tile_w, tile_h, columns, rows, margin, separation)
    serialize_tres_file(resource, output_path)

    def _human(data: dict[str, Any], verbose: bool = False) -> None:
        click.echo(
            f"Created {data['output_path']} with "
            f"{data['columns']}x{data['rows']} tiles "
            f"({data['tile_size']} each)"
        )

    emit(
        {
            "output_path": str(output_path),
            "tile_size": f"{tile_w}x{tile_h}",
            "columns": columns,
            "rows": rows,
            "total_tiles": columns * rows,
        },
        _human,
        ctx,
    )


@tileset.command("inspect")
@click.argument("tres_file", type=click.Path(exists=False))
@click.pass_context
def inspect(ctx: click.Context, tres_file: str) -> None:
    """Inspect a TileSet .tres resource and display its structure.

    Parses the TileSet and shows atlas sources, tile counts, terrain sets,
    physics layers, and external resource references.
    """
    config: GlobalConfig = ctx.obj
    tres_path = Path(tres_file)

    if not tres_path.exists():
        emit_error(
            GdautoError(
                message=f"File not found: {tres_file}",
                code="FILE_NOT_FOUND",
                fix="Check the path to your .tres file",
            ),
            ctx,
        )
        return

    try:
        resource = parse_tres_file(tres_path)
    except (ParseError, Exception) as exc:
        emit_error(
            GdautoError(
                message=f"Failed to parse {tres_file}: {exc}",
                code="PARSE_ERROR",
                fix="Ensure the file is a valid Godot .tres resource",
            ),
            ctx,
        )
        return

    if resource.type != "TileSet":
        emit_error(
            GdautoError(
                message=f"Resource type is '{resource.type}', not 'TileSet'",
                code="INVALID_RESOURCE_TYPE",
                fix="Expected a TileSet .tres file",
            ),
            ctx,
        )
        return

    data = _build_inspect_data(resource)

    if config.json_mode:
        sys.stdout.write(
            json.dumps(data, cls=GodotJSONEncoder, indent=2) + "\n"
        )
    elif not config.quiet:
        _print_inspect_human(data, verbose=config.verbose)


def _build_inspect_data(resource: Any) -> dict[str, Any]:
    """Build the structured inspection dict for a TileSet resource."""
    tile_size_val = resource.resource_properties.get("tile_size", "unknown")
    tile_size_str = (
        serialize_value(tile_size_val)
        if tile_size_val != "unknown"
        else "unknown"
    )

    atlas_sources = _extract_atlas_sources(resource)
    terrain_sets = _extract_terrain_sets(resource)
    physics_count = _count_physics_layers(resource)

    return {
        "type": resource.type,
        "format": resource.format,
        "uid": resource.uid,
        "tile_size": tile_size_str,
        "atlas_sources": atlas_sources,
        "terrain_sets": terrain_sets,
        "physics_layers": physics_count,
        "ext_resources": [
            {"type": ext.type, "path": ext.path}
            for ext in resource.ext_resources
        ],
    }


def _extract_atlas_sources(resource: Any) -> list[dict[str, Any]]:
    """Extract atlas source info from TileSetAtlasSource sub-resources."""
    sources: list[dict[str, Any]] = []
    tile_coord_re = re.compile(r"^\d+:\d+/")
    terrain_re = re.compile(r"^\d+:\d+/terrain_set")
    physics_re = re.compile(r"^\d+:\d+/physics_layer")

    for sub in resource.sub_resources:
        if sub.type != "TileSetAtlasSource":
            continue
        region_size = sub.properties.get("texture_region_size")
        tile_count = sum(1 for k in sub.properties if tile_coord_re.match(k))
        terrain_tiles = sum(1 for k in sub.properties if terrain_re.match(k))
        physics_tiles = sum(1 for k in sub.properties if physics_re.match(k))
        sources.append({
            "id": sub.id,
            "texture_region_size": (
                serialize_value(region_size) if region_size else "unknown"
            ),
            "tile_count": tile_count,
            "terrain_tiles": terrain_tiles,
            "physics_tiles": physics_tiles,
        })
    return sources


def _extract_terrain_sets(resource: Any) -> list[dict[str, Any]]:
    """Extract terrain set info from resource properties."""
    terrain_sets: list[dict[str, Any]] = []
    mode_re = re.compile(r"^terrain_set_(\d+)/mode$")

    for key in resource.resource_properties:
        m = mode_re.match(key)
        if m:
            idx = int(m.group(1))
            terrain_sets.append({
                "index": idx,
                "mode": serialize_value(resource.resource_properties[key]),
            })
    return terrain_sets


def _count_physics_layers(resource: Any) -> int:
    """Count physics layers defined in resource properties."""
    physics_re = re.compile(r"^physics_layer_\d+")
    return sum(1 for k in resource.resource_properties if physics_re.match(k))


def _print_inspect_human(data: dict[str, Any], verbose: bool = False) -> None:
    """Display TileSet inspection in human-readable format."""
    click.echo(f"TileSet (format={data['format']})")
    click.echo(f"  Tile size: {data['tile_size']}")
    click.echo(f"  Atlas sources: {len(data['atlas_sources'])}")
    for src in data["atlas_sources"]:
        click.echo(
            f"    [{src['id']}] region={src['texture_region_size']}, "
            f"tiles={src['tile_count']}, terrain={src['terrain_tiles']}, "
            f"physics={src['physics_tiles']}"
        )
    if data["terrain_sets"]:
        click.echo(f"  Terrain sets: {len(data['terrain_sets'])}")
    if data["physics_layers"]:
        click.echo(f"  Physics layers: {data['physics_layers']}")
    if data["ext_resources"]:
        click.echo(f"  External resources:")
        for ext in data["ext_resources"]:
            click.echo(f"    {ext['type']}: {ext['path']}")
