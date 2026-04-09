---
name: Overnight autoresearch preferences
description: User preferences for autonomous overnight iteration sessions on gdauto
type: feedback
---

When running overnight autoresearch iterations, commit after each successful iteration.
Prioritize Python CLI architecture (Click commands under src/gdauto/) over standalone PowerShell scripts.
PowerShell scripts are acceptable as support, but the main appeal is the Python CLI tool.
Always include pytest tests with each iteration.
Avoid PowerShell execution that needs user approval during unattended sessions.

**Why:** User goes to sleep and cannot approve permission prompts. PowerShell script execution may require interactive approval. Python CLI work and pytest tests run without that friction.

**How to apply:** During autonomous sessions, implement everything as gdauto CLI commands first. Only create .ps1 if it genuinely cannot be a Python command. Never push to remote without explicit approval.
