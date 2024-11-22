PlugFlow: A Modular Plugin Framework
=====================================

**PlugFlow** is a lightweight and extensible Agentic SLM Python framework for creating and managing modular plugins. Designed for flexibility and scalability, PlugFlow enables seamless integration of plugins for various use cases.
![Test Workflow Status](https://github.com/data-artisans-centre/plugflow-core/actions/workflows/run-tests.yml/badge.svg)


Features
--------

- **Modular Design**: Create self-contained plugins with ease.
- **Dynamic Plugin Discovery**: Automatically detect and load plugins at runtime.
- **Standardized Interface**: All plugins adhere to a consistent interface for execution and health monitoring.
- **Extensible**: Build custom plugins for any domain.

Quick Start
-----------

### Installation

Clone the repository and set up a virtual environment:

.. code-block:: bash

    git clone https://github.com/data-artisans-centre/plugflow-core.git
    cd plugflow
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt

### Basic Usage

Run the framework with an available plugin:

.. code-block:: bash

    python main.py execute <plugin_name> --params '{"param1": "value1", "param2": "value2"}'

Example:

.. code-block:: bash

    python main.py execute youtube-review --params '{"video_url": "https://www.youtube.com/watch?v=abc123", "max_comments": 10}'

### Plugin Structure

Each plugin follows a standardized structure:

.. code-block:: text

    plugins/
    ├── <plugin_name>/
    │   ├── __init__.py       # Main plugin logic
    │   ├── manifest.json     # Plugin metadata
    │   ├── README.md         # Plugin documentation
    │   ├── tests/            # Plugin-specific tests
    │       ├── __init__.py   # Test initialization
    │       └── test_<plugin_name>.py  # Unit tests

### Example Plugin: YouTube Review

The **YouTube Review Plugin** fetches comments from a YouTube video.

Usage:

.. code-block:: bash

    python main.py execute youtube-review --params '{"video_url": "https://youtu.be/abc123", "max_comments": 10}'

Output:

.. code-block:: json

    [
        {
            "author": "TestUser",
            "comment": "This is a test comment",
            "likes": 42,
            "time": "2 days ago"
        }
    ]

Development
-----------

### Adding a New Plugin

1. Create a new folder under `plugins/`.
2. Add the required files: `__init__.py`, `manifest.json`, and `README.md`.
3. Implement the plugin logic in `__init__.py`, adhering to the `PluginBase` interface.

### Running Tests

Each plugin must include unit tests in the `tests/` directory. Run tests for all plugins:

.. code-block:: bash

    pytest

Run tests for a specific plugin:

.. code-block:: bash

    pytest plugins/<plugin_name>/tests

### Configuring Plugins

Add metadata for your plugin in `manifest.json`:

.. code-block:: json

    {
        "name": "youtube-review",
        "entry_point": "__init__"
    }

Documentation
-------------

Generate project documentation using Sphinx and host it on Read the Docs.

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

We welcome contributions! See the `CONTRIBUTOR.rst` file for detailed guidelines.

License
-------

PlugFlow is distributed under the MIT License. See the `LICENSE` file for more information.

Support
-------

For issues or feature requests, please visit our GitHub repository:

- GitHub: https://github.com/data-artisans-centre/plugflow-core

