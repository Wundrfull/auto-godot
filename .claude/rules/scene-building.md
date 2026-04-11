---
paths:
  - "scenes/**/*"
  - "*.tscn"
---

# Scene Building Rules

## Node Type Compatibility

- CenterContainer only centers Control children. AnimatedSprite2D inherits
  Node2D, so CenterContainer will not position it. Wrap in a Control node
  with `mouse_filter = 2` (IGNORE) if needed.
- For UI games (clickers, card games, menus), use a Control root node,
  not Node2D. Set anchor preset `full_rect` on the root.

## Container Layout

- Children of VBoxContainer/HBoxContainer need `size_flags_vertical = 3`
  (FILL + EXPAND) to fill available space. Without this, children collapse.
- ScrollContainer children need explicit `size_flags_horizontal = 3` and
  `size_flags_vertical = 3` to fill the scroll area.

## Render Order and Input

- Node order in the scene tree equals render order. Later siblings render
  on top of earlier ones.
- Later siblings block mouse input. Set `mouse_filter = 2` (IGNORE) on
  non-interactive overlays, or they swallow clicks meant for nodes behind.

## Visibility

- PanelContainer is invisible by default. It needs a Theme or StyleBoxFlat
  override to render.

## Size Flags Reference

| Value | Meaning |
|-------|---------|
| 0 | FILL (default) |
| 1 | EXPAND |
| 3 | FILL + EXPAND |
| 4 | SHRINK_CENTER |
| 6 | SHRINK_CENTER + EXPAND |
