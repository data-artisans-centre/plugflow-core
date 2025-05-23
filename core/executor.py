import json

def execute_agent_flow(flow, agents, params):
    """
    Execute agents in the specified order.

    Args:
        flow (list): List of agent names in execution order.
        agents (dict): Dictionary of discovered agents.
        params (str): Parameters in JSON format to pass to agents.
    """
    param_dict = json.loads(params) if params else {}
    for agent_name in flow:
        agent_class = agents.get(agent_name)
        if not agent_class:
            print(f"Agent {agent_name} not found.")
            continue

        # Instantiate and execute the agent
        try:
            agent_instance = agent_class()
            print(f"Executing {agent_name}...")
            result = agent_instance.execute(**param_dict)
            print(f"Result from {agent_name}: {result}")
        except Exception as e:
            print(f"Error executing {agent_name}: {e}")
