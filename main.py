import click
from core.discovery import discover_agents
from core.executor import execute_agent_flow

@click.group()

def cli():
    """A CLI Tool with Agent Support"""
    pass

@cli.command()
@click.argument("flow", nargs=-1)
@click.option("--params", default="", help="Additional parameters for agents (JSON format)")
def execute(flow, params):
    """
    Execute agent in the specified order.
 
    Example: python main.py execute youtube-review --params '{"video_url": "https://youtu.be/abc123"}'
    """
    agents = discover_agents()
    execute_agent_flow(flow, agents, params)

if __name__ == "__main__":
    cli()

