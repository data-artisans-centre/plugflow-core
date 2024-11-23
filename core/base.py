class AgentBase:
    """Standard Agent Interface"""
    def execute(self, **kwargs):
        """Execute the agent logic"""
        raise NotImplementedError("Each agent must implement the 'execute' method")

    
    def health_check(self):
        """
        Check the health of the agent.
        """
        raise NotImplementedError("Each agent must implement the 'health_check' method")

