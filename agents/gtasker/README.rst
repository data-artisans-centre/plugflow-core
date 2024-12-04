GoogleServicesAgent: Seamless Integration with Google APIs
==========================================================

**GoogleServicesAgent** is a modular Python agent designed to interact with Google Calendar and Gmail APIs. It supports event creation, modification, and email operations while abstracting the complexity of authentication and API integration.

.. image:: https://github.com/your-repo/google-services-agent/actions/workflows/run-tests.yml/badge.svg
   :target: https://github.com/your-repo/google-services-agent/actions/workflows/run-tests.yml
   :alt: Test Workflow Status

Features
--------

- **Event Management**: Create and delete Google Calendar events programmatically.
- **Email Operations**: Send and read emails through the Gmail API with ease.
- **Authentication Handling**: Simplified OAuth2 authentication flow.
- **Extensible Design**: Easily extend or integrate into larger workflows.
- **Error Handling**: Validates input and handles API errors gracefully.

Quick Start
-----------

-------------------
Installation
-------------------

Clone the repository and set up a virtual environment:

.. code-block:: bash

    git clone https://github.com/your-repo/google-services-agent.git
    cd google-services-agent
    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt

-------------------
Basic Usage
-------------------

Initialize the agent with the required configuration:

.. code-block:: python

    from google_services_agent import GoogleServicesAgent

    service_config = {
        "credentials_path": "path/to/credentials.json",
        "scopes": [
            "https://www.googleapis.com/auth/calendar",
            "https://www.googleapis.com/auth/gmail.modify"
        ],
        "token_path": "path/to/token.json"
    }

    agent = GoogleServicesAgent(service_config)

Execute an operation:

.. code-block:: python

    # Create a calendar event
    event_request = {
        "operation_type": "create_event",
        "summary": "Team Meeting",
        "start_time": "2024-12-05T10:00:00+05:30",
        "end_time": "2024-12-05T11:00:00+05:30",
        "attendees": ["example@example.com"]
    }

    response = agent.execute(event_request)
    print(response)

Repository Structure
--------------------

The repository is organized as follows:

.. code-block:: text

    google-services-agent/
    ├── agents/                # Agent-specific directories
    │   ├── google_services/   # GoogleServicesAgent folder
    │   │   ├── __init__.py    # Main agent logic
    │   │   ├── manifest.json  # Metadata for the agent
    │   │   ├── README.rst     # Documentation for the agent
    │   │   └── tests/         # Agent-specific tests
    ├── core/                  # Core logic for PlugFlow framework
    ├── tests/                 # Global test cases
    ├── requirements.txt       # Python dependencies
    ├── setup.py               # Package setup file
    ├── main.py                # Entry point for running the framework

Agent Structure
---------------

Each agent follows this structure:

.. code-block:: text

    agents/
    ├── google_services/
    │   ├── __init__.py       # Main agent logic
    │   ├── manifest.json     # Metadata for the agent
    │   ├── README.rst        # Documentation for the agent
    │   ├── tests/            # Agent-specific tests
    │       ├── __init__.py   # Test initialization
    │       └── test_google_services.py  # Unit tests for the agent

Development
-----------

-------------------------
Creating a New Operation
-------------------------

1. Define the request model in `__init__.py` using Pydantic.
2. Implement the operation logic in a new method.
3. Add the operation type to the `execute()` method's dispatcher.
4. Write unit tests in `tests/` to validate functionality.

-------------------
Running Tests
-------------------

Run tests for all agents:

.. code-block:: bash

    pytest

Run tests for this agent:

.. code-block:: bash

    pytest agents/google_services/tests

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

GoogleServicesAgent is distributed under the MIT License. See the `LICENSE` file for more information.

Support
-------

For issues or feature requests, please visit our GitHub repository:

- GitHub: https://github.com/your-repo/google-services-agent
