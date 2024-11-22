class PluginBase:
    """Standard Plugin Interface"""
    def execute(self, **kwargs):
        """Execute the plugin logic"""
        raise NotImplementedError("Each plugin must implement the 'execute' method")

    
    def health_check(self):
        """
        Check the health of the plugin.
        """
        raise NotImplementedError("Each plugin must implement the 'health_check' method")

