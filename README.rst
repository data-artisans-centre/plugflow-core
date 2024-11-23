PlugFlow: A Modular Agent Framework
=====================================

**PlugFlow** is a lightweight and extensible Python framework designed for creating and managing modular agents. It enables seamless integration of agents for various use cases, with dynamic discovery, execution, and standardized interfaces.

.. image:: https://github.com/data-artisans-centre/plugflow-core/actions/workflows/run-tests.yml/badge.svg
   :target: https://github.com/data-artisans-centre/plugflow-core/actions/workflows/run-tests.yml
   :alt: Test Workflow Status

Features
--------

- **Modular Design**: Create self-contained agents with ease.
- **Dynamic Agent Discovery**: Automatically detect and load agents at runtime.
- **Standardized Interface**: All agents adhere to a consistent interface for execution and health monitoring.
- **Extensible**: Build custom agents for any domain or workflow.
- **Integrated Testing**: Include dedicated tests for every agent to ensure reliability.

Quick Start
-----------

-------------------
Installation
-------------------

Clone the repository and set up a virtual environment:

.. code-block:: bash

    git clone https://github.com/data-artisans-centre/plugflow-core.git
    cd plugflow-core
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt

-------------------
Basic Usage
-------------------

Run the framework with an available agent:

.. code-block:: bash

    python main.py execute <agent_name> --params '{"param1": "value1", "param2": "value2"}'

Example:

.. code-block:: bash

    python main.py execute youtube-review --params '{"video_url": "https://www.youtube.com/watch?v=abc123", "max_comments": 10}'

Output:

.. code-block:: json

    [
        {
            "author": "TestUser",
            "comment": "This is a test comment"
        }
    ]

Repository Structure
--------------------

The repository is organized as follows:

.. code-block:: text

    plugflow-core/
    ├── agents/                # Agent-specific directories
    │   ├── <agent_name>/      # Individual agent folder
    │   │   ├── __init__.py    # Main agent logic
    │   │   ├── manifest.json  # Metadata for the agent
    │   │   ├── README.md      # Documentation for the agent
    │   │   └── tests/         # Agent-specific tests
    ├── core/                  # Core logic for PlugFlow
    │   ├── base.py            # Base class for agents
    │   ├── discovery.py       # Dynamic agent discovery
    ├── docs/                  # Project documentation
    ├── tests/                 # Global test cases
    ├── requirements.txt       # Python dependencies
    ├── setup.py               # Package setup file
    ├── main.py                # Entry point for running the framework

Agent Structure
---------------

Each agent must follow this structure:

.. code-block:: text

    agents/
    ├── <agent_name>/
    │   ├── __init__.py       # Main agent logic
    │   ├── manifest.json     # Metadata for the agent
    │   ├── README.md         # Documentation for the agent
    │   ├── tests/            # Agent-specific tests
    │       ├── __init__.py   # Test initialization
    │       └── test_<agent_name>.py  # Unit tests for the agent

Example for `youtube-review` agent:

.. code-block:: text

    agents/
    ├── youtube_review/
    │   ├── __init__.py
    │   ├── manifest.json
    │   ├── README.md
    │   ├── tests/
    │       ├── __init__.py
    │       └── test_youtube_review.py

Development
-----------

-------------------------
Creating a New Agent
-------------------------

1. Create a new folder under `agents/`.
2. Add the required files: `__init__.py`, `manifest.json`, and `README.md`.
3. Implement the agent logic in `__init__.py`, adhering to the `AgentBase` interface.
4. Add unit tests in the `tests/` directory.

Refer to `docs/Creating_Agent.rst` for detailed instructions.

-------------------
Running Tests
-------------------

Run tests for all agents:

.. code-block:: bash

    pytest

Run tests for a specific agent:

.. code-block:: bash

    pytest agents/<agent_name>/tests

-------------------
Documentation
-------------------

Generate project documentation using Sphinx:

1. Install documentation dependencies:

   .. code-block:: bash

       pip install sphinx

2. Build the documentation:

   .. code-block:: bash

       cd docs
       make html

3. View the documentation in `docs/_build/html`.

Contributing
------------

We welcome contributions! Please refer to `CONTRIBUTING.rst` for guidelines.

License
-------

PlugFlow is distributed under the MIT License. See the `LICENSE` file for more information.

Support
-------

For issues or feature requests, please visit our GitHub repository:

- GitHub: https://github.com/data-artisans-centre/plugflow-core


