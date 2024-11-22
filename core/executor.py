from core.base import PluginBase
import json

def execute_plugin_flow(flow, plugins, params):
    """
    Execute plugins in the specified order.

    Args:
        flow (list): List of plugin names in execution order.
        plugins (dict): Dictionary of discovered plugins.
        params (str): Parameters in JSON format to pass to plugins.
    """
    param_dict = json.loads(params) if params else {}
    for plugin_name in flow:
        plugin_module = plugins.get(plugin_name)
        if plugin_module:
            plugin_class = getattr(plugin_module, "Plugin", None)
            if plugin_class and issubclass(plugin_class, PluginBase):
                plugin_instance = plugin_class()
                print(f"Executing {plugin_name}...")
                plugin_instance.execute(**param_dict)
            else:
                print(f"Plugin {plugin_name} does not implement the standard interface.")
        else:
            print(f"Plugin {plugin_name} not found.")

