import os
import json
import importlib
import logging
from core.base import AgentBase

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

AGENTS_DIR = "agents"


def discover_agents():
    """Discover agents dynamically based on manifest files."""
    agents = {}
    for folder in os.listdir(AGENTS_DIR):
        folder_path = os.path.join(AGENTS_DIR, folder)
        manifest_path = os.path.join(folder_path, "manifest.json")

        # Skip non-directories or directories without a manifest
        if not os.path.isdir(folder_path):
            logger.debug(f"Skipping non-directory: {folder_path}")
            continue

        if not os.path.exists(manifest_path):
            logger.warning(f"Manifest file missing in: {folder_path}")
            continue

        # Read and validate manifest.json
        try:
            with open(manifest_path, "r") as f:
                manifest = json.load(f)
        except json.JSONDecodeError as e:
            logger.error(f"Invalid JSON in {manifest_path}: {e}")
            continue

        agent_name = manifest.get("name")
        module_path = manifest.get("entry_point")  # Module path
        class_name = manifest.get("class_name")   # Class name within the module

        if not agent_name or not module_path or not class_name:
            logger.warning(f"Invalid manifest fields in {manifest_path}")
            continue

        # Construct the full module path
        full_module_path = f"{AGENTS_DIR}.{folder}.{module_path}"
        try:
            # Import the module
            module = importlib.import_module(full_module_path)
            # Get the class from the module
            agent_class = getattr(module, class_name, None)

            if not agent_class:
                logger.warning(f"Class {class_name} not found in module {full_module_path}")
                continue

            # Validate that the class implements the AgentBase interface
            if not issubclass(agent_class, AgentBase):
                logger.warning(f"Agent {agent_name} does not implement the standard interface (AgentBase).")
                continue

            agents[agent_name] = agent_class
            logger.info(f"Successfully loaded agent: {agent_name}")
        except ImportError as e:
            logger.error(f"Failed to import module {full_module_path}: {e}")

    return agents

