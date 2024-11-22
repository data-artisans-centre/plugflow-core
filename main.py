import click
from core.discovery import discover_plugins
from core.executor import execute_plugin_flow

@click.group()
def cli():
    """A CLI Tool with Plugin Support"""
    pass

@cli.command()
@click.argument("flow", nargs=-1)
@click.option("--params", default="", help="Additional parameters for plugins (JSON format)")
def execute(flow, params):
    """
    Execute plugins in the specified order.
    
    Example: python main.py execute youtube-review --params '{"video_url": "https://youtu.be/abc123"}'
    """
    plugins = discover_plugins()
    execute_plugin_flow(flow, plugins, params)

if __name__ == "__main__":
    cli()

