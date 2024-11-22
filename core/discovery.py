import os
import json
import importlib

PLUGINS_DIR = "plugins"

def discover_plugins():
    """Discover plugins dynamically based on manifest files."""
    plugins = {}
    for folder in os.listdir(PLUGINS_DIR):
        folder_path = os.path.join(PLUGINS_DIR, folder)
        manifest_path = os.path.join(folder_path, "manifest.json")
        if os.path.isdir(folder_path) and os.path.exists(manifest_path):
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
                plugin_name = manifest.get("name")
                entry_point = manifest.get("entry_point")
                if plugin_name and entry_point:
                    module_path = f"{PLUGINS_DIR}.{folder}.{entry_point}"
                    module = importlib.import_module(module_path)
                    plugins[plugin_name] = module
    return plugins

