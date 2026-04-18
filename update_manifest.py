import json
import os
import glob
import urllib.request
from collections import OrderedDict

# --- CONFIGURATION ---
DEVEL_MANIFEST_URL = "https://gitlab.gnome.org/GNOME/gnome-text-editor/-/raw/main/org.gnome.TextEditor.Devel.json"
STABLE_MANIFEST = "org.gnome.TextEditor.json"
DEVEL_MANIFEST = "org.gnome.TextEditor.Devel.json"
DEFAULT_THEME_ID = "deep-oceanic-navy"
THEME_FILES = sorted(glob.glob("*.xml"))

def download_devel_manifest():
    print(f"Downloading latest Devel manifest...")
    try:
        urllib.request.urlretrieve(DEVEL_MANIFEST_URL, DEVEL_MANIFEST)
        print(" -> Download successful.")
    except Exception as e:
        print(f" -> Error downloading Devel manifest: {e}")

def update_manifest(filename, app_id, branch_name):
    if not os.path.exists(filename):
        print(f"Skipping {filename} (File not found).")
        return

    with open(filename, 'r') as f:
        data = json.load(f)

    print(f"Injecting themes, patches, and names into {filename}...")

    # 1. Standardize the Header (Remove 'id', force 'app-id' and 'name')
    if "id" in data: del data["id"]
    
    # We use a temporary dict to force these to the top of the file
    new_data = OrderedDict()
    new_data["app-id"] = app_id
    new_data["branch"] = branch_name
    new_data["name"] = "Text Editor"
    
    # Copy everything else from the original data
    for key, value in data.items():
        if key not in ["app-id", "branch", "name", "id"]:
            new_data[key] = value

    # 2. Add Default Theme Environment Variable
    env_flag = f"--env=GTK_SOURCE_STYLE_SCHEME={DEFAULT_THEME_ID}"
    if 'finish-args' not in new_data:
        new_data['finish-args'] = []
    new_data['finish-args'] = [arg for arg in new_data['finish-args'] if "GTK_SOURCE_STYLE_SCHEME" not in arg]
    new_data['finish-args'].append(env_flag)

    # 3. Inject Patches
    for module in new_data.get('modules', []):
        if module['name'] == "libeditorconfig":
            patch = {"type": "patch", "path": "patches/fix-strncpy-buffer-truncation.patch"}
            if "sources" in module and patch not in module['sources']:
                module['sources'].append(patch)
        if module['name'] == "gnome-text-editor":
            patch = {"type": "patch", "path": "patches/metainfo-reorder-releases.patch"}
            if "sources" in module and patch not in module['sources']:
                module['sources'].append(patch)

    # 4. Create/Inject the Custom Style Module
    new_module = {
        "name": "custom-gtksource-styles",
        "buildsystem": "simple",
        "build-commands": ["mkdir -p /app/share/gtksourceview-5/styles"],
        "sources": [{"type": "file", "path": t} for t in THEME_FILES]
    }
    for theme in THEME_FILES:
        new_module["build-commands"].append(f"install -Dm644 {theme} /app/share/gtksourceview-5/styles/")

    new_data['modules'] = [m for m in new_data.get('modules', []) if m['name'] != "custom-gtksource-styles"]
    new_data['modules'].insert(0, new_module)

    # 5. Save
    with open(filename, 'w') as f:
        json.dump(new_data, f, indent=2)
    
    print(f"Success! {filename} updated with ID, Branch, and Name.")

if __name__ == "__main__":
    download_devel_manifest()
    update_manifest(DEVEL_MANIFEST, "org.gnome.TextEditor.Devel", "master")
    update_manifest(STABLE_MANIFEST, "org.gnome.TextEditor", "stable")

