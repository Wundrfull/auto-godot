---
paths:
  - "assets/sprites/**/*"
  - "art/**/*"
  - "*.tres"
  - "*.aseprite"
---

# Sprite Pipeline Rules

## Import Workflow

1. Export from Aseprite with `--format json-array` (not json-hash)
2. Run `auto-godot sprite import-aseprite` to generate .tres SpriteFrames
3. Run `godot --headless --import` to sync UIDs and generate .import files
4. Run `auto-godot sprite validate` to check SpriteFrames structure

## Common Pitfalls

- After `sprite import-aseprite`, always run `godot --headless --import`
  to generate .import files and assign UIDs. Without this, ExtResource
  paths break at runtime.
- Verify .tres ext_resource paths are full `res://` paths relative to the
  project root, not bare filenames.
- Use `auto-godot sprite list-animations` to verify animation names match
  what scripts reference. Mismatched names cause silent failures.

## ExtResource Format

Generated .tscn/.tres files must use bare ExtResource syntax:
- Correct: `ExtResource("1_script")`
- Wrong: `"ExtResource(\"1_script\")"`

If you see escaped quotes inside ExtResource values, the serializer has
a bug.

## Aseprite Export Settings

When exporting from Aseprite CLI for auto-godot:
```
aseprite -b --sheet <output.png> --data <output.json> --format json-array <input.aseprite>
```

The `--format json-array` flag is required. json-hash format is not
supported by `sprite import-aseprite`.
