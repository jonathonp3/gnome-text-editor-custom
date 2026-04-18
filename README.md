# GNOME Text Editor (Custom Build)

Custom Flatpak build for GNOME Text Editor with 12+ premium themes and critical patches.

## 🚀 Quick Start
1. Run the theme injector: `python3 update_manifest.py`
2. Build the Stable version: `flatpak run org.flatpak.Builder --force-clean --repo=repo-stable build-dir-stable org.gnome.TextEditor.json`
3. Create the bundle: `flatpak build-bundle repo-stable gnome-text-editor-stable.flatpak org.gnome.TextEditor stable`

## 🎨 Themes Included
* Deep Oceanic (Default)
* Andromeda
* Ant
* Dracula
* Kimi
* Nord
* Solarized (Multiple variants)
* Space KDE
* Sweet
