SportsAgent
===========

The **SportsAgent** is a Python-based agent designed to interact with the Football API (API-Sports) to fetch various sports-related data, such as team statistics, fixtures, standings, and player details.

Features
--------

- Fetch detailed football data including standings, fixtures, teams, and players.
- Supports various categories like leagues, teams, and top scorers.
- Interactive execution with user input for category selection.
- Includes a health check method to verify API availability.
- Simple integration with the `AgentBase` framework.

Installation
------------

Ensure the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests

Install the dependencies using pip:

.. code-block:: bash

    pip install requests

Parameters
----------

The agent accepts the following parameters:

- ``apikey`` (str): API key for authentication with the Football API.
- ``category`` (str): The category of football data to fetch (e.g., "teams", "standings", "players").
- ``parameters`` (dict, optional): Additional query parameters for API requests.

Example Usage
-------------

Execute the agent directly from the terminal using the following command:

.. code-block:: bash

    python main.py execute football_sports_agent

The script will prompt for category selection and any necessary parameters.

Output
------

The agent returns the fetched football data as a JSON-formatted string. The JSON object contains metadata and detailed responses based on the selected category.

Example Output:

.. code-block:: json

    {
        "response": [
            {
                "team": "Manchester United",
                "league": "Premier League",
                "rank": 3,
                "points": 68
            }
        ]
    }

Health Check
------------

The agent includes a ``health_check`` method to verify the operational status of the Football API. It performs a test request and returns the API's health status.

Example health check output:

.. code-block:: json

    {
        "status": "healthy"
    }

Testing
-------

A test suite is included to validate the agent's functionality. Use `pytest` to run the tests.

Run all tests:

.. code-block:: bash

    pytest agents/football_sports_agent/tests

Contributing
------------

Contributions are welcome! Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

Best practices for contributions:

- Ensure adherence to PEP 8 coding standards.
- Include detailed docstrings and comments for new functionality.
- Write appropriate unit tests for any added or modified methods.

License
-------

This project is distributed under the MIT License. See the LICENSE file for more information.