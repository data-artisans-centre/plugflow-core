class PluginBase:
    """Standard Plugin Interface"""
    def execute(self, **kwargs):
        """Execute the plugin logic"""
        raise NotImplementedError("Each plugin must implement the 'execute' method")

