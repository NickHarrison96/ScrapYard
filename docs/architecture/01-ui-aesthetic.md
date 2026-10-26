# UI Aesthetic – Aero Glass + Hacker

**Status**: Active  
**Date**: 2026-10-26

## Intent
90s-kid energy: Windows Vista/7 **Aero glass** chrome + dark **hacker / phosphor** terminal vibe.

Not:
- Beige classic Win32
- Flat modern SaaS
- Generic AI-dashboard glassmorphism

Yes:
- Translucent blue-tinted title bars and panels
- Soft outer glow / inner highlight (Aero)
- Phosphor green for live data and logs
- Cyan accents for section headers
- Consolas / Segoe UI
- Three-pane RE workstation layout (function list | graph | properties)
- Subtle scanline on the graph canvas

## Palette
- Deep navy / near-black backgrounds
- Aero blue gradients on chrome
- `#33ff66` phosphor for values and log
- `#33ccff` cyan for labels
- Amber for offline / warn status

## Layout
1. Title bar + system buttons
2. Menu bar (File Edit View Graph Agent REA Help)
3. Toolbar
4. Client: left list | center Cytoscape | right props + REA log
5. Status bar

## Files
- `control_plane/ui/index.html`
- `control_plane/ui/styles/early2000s.css` (name kept; content is Aero+hacker)
- `control_plane/ui/app.js`
