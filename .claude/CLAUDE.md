# auto-godot Conventions

Guidelines for AI agents and developers working with auto-godot CLI commands.

## Command Patterns

### Shell Escaping
- Always use single quotes for property values containing `$`:
  `--property 'text=Buy ($50)'`
  Double quotes cause shell expansion of `$50`.

### class_name Conflicts
- Never use `--class-name` that matches an autoload singleton name.
  Godot silently fails when a class_name collides with an autoload.

### Resource Imports
- Always run `godot --headless --import` after `sprite export` to sync UIDs.
  Without this, .import files are missing and ExtResource paths break.

### JSON Output
- `--json` is a global flag, not a subcommand option.
  Correct: `auto-godot --json project info`
  Wrong: `auto-godot project info --json`

## Godot Node Type Gotchas

### AnimatedSprite2D is Node2D, Not Control
CenterContainer only centers Control children. AnimatedSprite2D inherits
Node2D, so CenterContainer will not position it. Workaround: wrap in a
Control node and set `mouse_filter = 2` (IGNORE) on the wrapper.

### VBoxContainer / HBoxContainer Children
Children need `size_flags_vertical = 3` (FILL + EXPAND) to fill available
space. Without this, children collapse to minimum size.

### Size Flags Reference
| Value | Meaning |
|-------|---------|
| 0 | FILL (default) |
| 1 | EXPAND |
| 3 | FILL + EXPAND |
| 4 | SHRINK_CENTER |
| 6 | SHRINK_CENTER + EXPAND |

### Input Blocking
Later siblings in the scene tree render on top and block mouse input.
Set `mouse_filter = 2` (IGNORE) on non-interactive overlays, or they
swallow clicks meant for nodes behind them.

### ScrollContainer
Children need explicit `size_flags_horizontal = 3` and
`size_flags_vertical = 3` to fill the scroll area. Without flags,
content collapses to zero size inside the scroll region.

### PanelContainer Visibility
PanelContainer is invisible by default. It needs a Theme or StyleBoxFlat
override to render. Use `auto-godot theme create` to generate a theme,
then assign it to the PanelContainer.

### Control Root for UI Games
For UI-heavy games (clickers, card games, menus), use a Control root
node, not Node2D. Set anchor preset `full_rect` on the root.
Node2D does not respect anchoring or container layout.

## Scene Building Rules

### Render Order
Node order in the scene tree equals render order. Later siblings render
on top of earlier ones. Use `auto-godot scene reorder-node` to fix
layering issues.

### Instanced Scenes
When using `auto-godot scene add-instance`, the instanced scene's root
node type must be compatible with its parent. A CharacterBody2D instanced
under a VBoxContainer will not layout correctly.

### Property Format
Properties passed via `--property` use Godot literal syntax:
- Vectors: `position=Vector2(100, 200)`
- Colors: `modulate=Color(1, 0, 0, 1)`
- Booleans: `visible=false`
- Strings: `text=Hello World` (no quotes needed unless value has spaces)

## Validation Workflow

### Text Validation (Fast, No Godot)
```bash
auto-godot project validate path/to/project
auto-godot scene validate path/to/scene.tscn
auto-godot sprite validate path/to/spriteframes.tres
```
Catches: malformed .tscn/.tres, broken res:// paths, missing sections.
Does NOT catch: runtime load errors, UID mismatches, class conflicts.

### Headless Godot Validation (Thorough, Requires Godot)
```bash
godot --headless --import                  # Sync UIDs and .import files
godot --headless --quit-after 3            # Runtime load test
```
Parse stdout/stderr for ERROR and WARNING lines. This catches issues
that text validation misses: serialization bugs, missing resources,
class_name conflicts.

### Recommended Order
1. `auto-godot project validate` after every batch of changes
2. `auto-godot scene validate` on modified scenes
3. `godot --headless --import` after any sprite/resource changes
4. `godot --headless --quit-after 3` before declaring a phase complete

### Common Validation Errors
| Error Pattern | Cause | Fix |
|---------------|-------|-----|
| `Failed to load resource` | Missing .import file | Run `godot --headless --import` |
| `Invalid UID` | UID mismatch after file move | Delete .import, re-import |
| `Cannot instance scene` | Circular dependency | Check add-instance references |
| `class_name already in use` | Duplicate class_name | Rename one of the conflicting scripts |

## ExtResource Serialization

Generated .tscn files must use bare ExtResource syntax:
- Correct: `ExtResource("1_script")`
- Wrong: `"ExtResource(\"1_script\")"`

If you see escaped quotes inside ExtResource values in a .tscn file,
the serializer has a bug. File an issue.
