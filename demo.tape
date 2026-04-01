# odoo-addons-path terminal demo
# Showcases: auto-detection, verbose mode, explicit paths, and version check

# ── Output ────────────────────────────────────────────────────────────────────
Output ./docs/demo.gif

# ── Dependencies ──────────────────────────────────────────────────────────────
Require odoo-addons-path

# ── Settings ──────────────────────────────────────────────────────────────────
Set Shell bash
Set TypingSpeed 25ms
Set Width 2300
Set Height 1600
Set FontSize 49
Set FontFamily "JetBrains Mono, Fira Code, monospace"
Set Theme { "name": "odoo-addons-path", "background": "#111111", "foreground": "#f5f5f5", "cursor": "#ea580c", "black": "#2a2a2a", "red": "#ef4444", "green": "#22c55e", "yellow": "#eab308", "blue": "#3b82f6", "magenta": "#d946ef", "cyan": "#06b6d4", "white": "#f5f5f5", "brightBlack": "#52525b", "brightRed": "#f87171", "brightGreen": "#4ade80", "brightYellow": "#facc15", "brightBlue": "#60a5fa", "brightMagenta": "#e879f9", "brightCyan": "#22d3ee", "brightWhite": "#ffffff" }
Set WindowBar Colorful
Set WindowBarSize 60
Set BorderRadius 15
Set Margin 30
Set Padding 40
Set LineHeight 1.3

# ── Scene 1: Auto-detection ───────────────────────────────────────────────────
Hide
Type "export PS1='\[\033[38;2;249;115;22m\]❯\[\033[0m\] '"
Enter
Type "clear"
Enter
Show

Sleep 500ms
Type "odoo-addons-path ~/projects/mybig-trobz-project"
Sleep 400ms
Enter

Sleep 1s

# ── Scene 2: Verbose mode — see detected layout and path categories ────────────
Sleep 1s
Hide
Type "clear"
Enter
Show

Sleep 500ms
Type "odoo-addons-path ~/projects/mybig-trobz-project --verbose"
Sleep 400ms
Enter

Sleep 1500ms

# ── Scene 3: Explicit addon dir with glob pattern ─────────────────────────────
Sleep 1s
Hide
Type "clear"
Enter
Show

Sleep 500ms
Type "odoo-addons-path ~/projects/mybig-trobz-project \"
Sleep 400ms
Enter
Type "  --addons-dir './addons/repo1/18.0, ./addons/repo2/18.0'"
Sleep 400ms
Enter

Sleep 1s

# ── Scene 4: Version consistency check ───────────────────────────────────────
Sleep 1s
Hide
Type "clear"
Enter
Show

Sleep 500ms
Type "odoo-addons-path ~/projects/mybig-trobz-project --check-versions"
Sleep 400ms
Enter

Sleep 1500ms

Sleep 2s
