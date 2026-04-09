# Game Build Loop: Iterative Game Creation with Gap Discovery

Use this prompt in a fresh Godot project repo where gdauto is installed. Claude will attempt to build a complete game from scratch using only CLI tools, logging every blocker encountered.

---

## The Prompt

Copy everything below the line into Claude Code as your first message.

---

You are building a complete idle clicker game in Godot 4.6 using ONLY command-line tools. You must never open the Godot editor GUI. Your entire workflow uses three tools:

1. **gdauto** -- CLI for Godot file manipulation (scenes, scripts, project config, resources)
2. **pixel-mcp** -- MCP server for creating pixel art in Aseprite (create_canvas, draw_pixels, draw_rectangle, draw_circle, set_palette, add_layer, export_spritesheet, etc.)
3. **Aseprite CLI** -- Headless sprite export (`aseprite -b` for batch mode, no GUI needed)

### Your Goal

Build a playable idle clicker game called "Cookie Cosmos" with these features:

**Core gameplay:**
- A large cookie in the center that the player clicks for points
- Score display showing current cookies
- Cookies-per-second display for passive income
- Click multiplier that increases with upgrades

**Upgrade shop (3 tiers):**
- Auto-Clicker ($50): adds 1 cookie/sec passive income
- Double Click ($200): doubles click value
- Golden Cookie ($1000): 10x click value for 10 seconds (cooldown)

**Visual polish:**
- Animated cookie sprite (idle wobble + click squish)
- Particle burst on click
- Score popup text that floats up and fades
- Background gradient or pattern
- UI theme with consistent colors (dark blue bg, gold accents)

**Audio (placeholder setup):**
- Click sound effect node
- Background music node
- Upgrade purchase sound

**Save system:**
- Auto-save on upgrade purchase
- Save/load via JSON to user://

### Rules

1. **Use gdauto for ALL Godot file operations.** Never write .tscn, .tres, or project.godot files by hand. Use `gdauto scene create-simple`, `gdauto scene add-node`, `gdauto script create`, etc.

2. **Use pixel-mcp MCP tools for ALL art creation.** Create sprites, animations, and UI art through the MCP server tools (create_canvas, draw_pixels, set_palette, add_layer, export_spritesheet, etc.).

3. **Use Aseprite CLI for sprite export.** After pixel-mcp creates .aseprite files, export with:
   ```
   gdauto sprite export art/cookie.aseprite -o assets/sprites/cookie
   ```
   Or manually: `aseprite -b art/cookie.aseprite --sheet assets/sprites/cookie/cookie_sheet.png --data assets/sprites/cookie/cookie.json --format json-array --sheet-type packed --trim --list-tags`

4. **Use gdauto sprite import-aseprite for Godot integration:**
   ```
   gdauto sprite import-aseprite assets/sprites/cookie/cookie.json -o assets/sprites/cookie/cookie.tres
   ```

5. **Log EVERY blocker.** When you cannot do something with the available tools, write it to `blockers.md` with this format:
   ```
   ## BLOCKER: [short description]
   - **What I tried:** [exact command or MCP tool call]
   - **What happened:** [error or limitation]
   - **What I needed:** [the ideal command/tool that would unblock this]
   - **Workaround:** [what I did instead, or "none -- fully blocked"]
   - **Category:** [gdauto | pixel-mcp | aseprite | godot | workflow]
   - **Impact:** [critical | high | medium | low]
   ```

6. **Log progress.** After each major milestone, append to `progress.md`:
   ```
   ## Phase N: [phase name]
   - **Status:** [complete | partial | blocked]
   - **What worked:** [list of successful steps]
   - **Blockers hit:** [count and references to blockers.md]
   - **Files created:** [list]
   ```

### Build Phases

Execute these phases in order. Push as far as you can in each phase before moving to the next. Do NOT skip phases.

**Phase 1: Project Scaffold**
- `gdauto project create CookieCosmos --output .`
- Configure display (720x1280 portrait, canvas_items stretch, nearest filter)
- Configure rendering (mobile)
- Set up input actions (click, ui_upgrade)
- Name physics layers

**Phase 2: Create Pixel Art**
Using pixel-mcp MCP tools:
- Create a 64x64 cookie sprite with idle animation (4 frames, gentle wobble)
- Create a 64x64 cookie sprite with click animation (3 frames, squish effect)
- Create a 16x16 particle sprite (small sparkle, 3 frames)
- Create a 32x32 upgrade icon set (3 icons for the 3 upgrades)
- Create UI panel art (9-patch style backgrounds)
- Export all from Aseprite using gdauto sprite export or Aseprite CLI

**Phase 3: Import Assets into Godot**
- `gdauto sprite import-aseprite` for each sprite set
- `gdauto sprite validate` each generated .tres
- `gdauto sprite list-animations` to verify animations

**Phase 4: Build Main Scene**
- Create main scene with Control root
- Add VBoxContainer layout
- Add score Label, cookies/sec Label
- Add AnimatedSprite2D for cookie (assign SpriteFrames)
- Add click Button (invisible, overlaying the cookie)
- Add particle effect for clicks
- Set anchors for full-screen layout
- Create and assign UI theme (dark blue + gold)

**Phase 5: Build Shop Scene**
- Create shop scene from ui-panel template
- Add 3 upgrade buttons with labels and costs
- Add upgrade description labels
- Create shop script with upgrade logic

**Phase 6: Write Game Scripts**
- Main scene script: click handling, score display, passive income
- Game manager autoload: state tracking, upgrade logic, save/load
- Save manager autoload: JSON persistence to user://
- Shop script: upgrade purchase, cost display, afford checking

**Phase 7: Wire Everything Together**
- Connect button signals to script methods
- Instance shop into main scene
- Assign scripts to nodes
- Register autoloads
- Set main scene in project.godot
- Add timers for passive income and auto-save

**Phase 8: Audio Setup**
- Add AudioStreamPlayer nodes (click, music, upgrade)
- Create audio bus layout (Master, SFX, Music)
- Connect audio to game events in scripts

**Phase 9: Visual Polish**
- Add score popup animation (float up + fade)
- Add cookie scale animation on click
- Add background ColorRect or gradient
- Set anchor presets on all UI elements
- Add camera if needed

**Phase 10: Validation**
- `gdauto scene validate` all scenes
- `gdauto project validate` entire project
- `gdauto project stats` for overview
- List all nodes, resources, scripts
- Verify no missing resource references

### After All Phases

Write a final summary to `summary.md`:
```
# Cookie Cosmos Build Summary

## Completion
- Phases completed: X/10
- Total blockers: N
- Critical blockers: N
- Steps fully blocked (no workaround): N

## Tool Usage Stats
- gdauto commands used: [list unique commands]
- pixel-mcp tools used: [list unique tools]
- Aseprite CLI invocations: N
- Files created by hand (workarounds): N

## Top Blockers (by impact)
[list top 5 blockers with descriptions]

## What Worked Well
[list the smoothest parts of the workflow]

## Missing Tools (recommendations)
[list tools/commands that should exist but don't]
```

### Important Behaviors

- **Do NOT give up at the first blocker.** Log it and move on to the next step. Come back to blocked steps later if you find a workaround.
- **Do NOT write Godot files by hand** unless completely blocked. If you must, log it as a blocker with "workaround: wrote file by hand".
- **Do NOT ask me questions.** Make your best judgment and keep going. Log uncertainty as blockers.
- **Push through EVERY phase** even if earlier phases had blockers. Partial progress in every phase is better than perfect completion of phase 1.
- **Be specific in blocker logs.** "Couldn't do X" is useless. "Ran `gdauto scene add-node --property 'texture=...'` and got error Y because Z" is useful.
- **Run gdauto commands with `--json` flag** when you need to parse output programmatically.
- **Check your work** with `gdauto scene list-nodes`, `gdauto scene validate`, `gdauto resource inspect` after major operations.

### Environment Setup

Before starting, verify:
```bash
# gdauto is installed and working
gdauto --version

# Aseprite is available (headless)
"C:\Program Files (x86)\Steam\steamapps\common\Aseprite\Aseprite.exe" --version

# pixel-mcp is available (check MCP tools)
# (pixel-mcp tools should be available as MCP tools in your context)

# Godot is available (for validation only)
"C:\Users\dared\Documents\GameDev\Godot_v4.6-stable_win64_console.exe" --version
```

Now begin with Phase 1. Push as far as you can. Log everything.
