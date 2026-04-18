# GNOME Text Editor (Custom Build)

Custom Flatpak build for GNOME Text Editor with 12+ premium themes and critical patches.

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

## 📥 Getting Started
```bash
git clone git@github.com:jonathonp3/gnome-text-editor-custom.git
cd gnome-text-editor-custom
python3 update_manifest.py
```

## 📦 Build Instructions

### Stable Version
```bash
# Build
flatpak run org.flatpak.Builder --force-clean --repo=repo-stable build-dir-stable org.gnome.TextEditor.json
```
# Bundle
```bash
flatpak build-bundle repo-stable gnome-text-editor-stable.flatpak org.gnome.TextEditor stable
```
# Install
```bash
flatpak install --user --reinstall gnome-text-editor-stable.flatpak
```

### Development Version (Master)
```bash
# Build
flatpak run org.flatpak.Builder --force-clean --repo=repo-devel build-dir-devel org.gnome.TextEditor.Devel.json
```
# Bundle
```bash
flatpak build-bundle repo-devel gnome-text-editor-devel.flatpak org.gnome.TextEditor.Devel master
```
# Install
```bash
flatpak install --user --reinstall gnome-text-editor-devel.flatpak
```

