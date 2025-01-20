CrickAlert Agent
===============

The **CrickAlert Agent** is designed to fetch and filter cricket match information using the Cricbuzz RapidAPI. It provides real-time access to cricket match data with flexible search capabilities for matches, teams, venues, and series.

Features
--------

- Fetch recent cricket matches
- Search matches by various criteria (team, venue, series, format)
- Real-time match information
- Flexible filtering options
- Health check functionality
- Integration with the PlugFlow framework

Installation
------------

Ensure that the required dependencies are installed from `requirements.txt`:

.. code-block:: text

    requests
    json

Install the dependencies using pip:

.. code-block:: bash

    pip install requests

Parameters
----------

The agent accepts the following parameters:

- ``api_key`` (str): RapidAPI key for authentication (required)
- ``search_term`` (str, optional): Term to filter matches (team, venue, series, etc.)
- ``endpoint`` (str, optional): API endpoint to query (default: 'matches/v1/recent')

Example Usage
-------------

To execute the agent, use the PlugFlow CLI:

.. code-block:: vscode terminal

    python main.py execute crickAlert --params '{\"api_key\": \"your_api_key\"}'

With search term:

.. code-block:: bash

    python main.py execute crickAlert --params '{\"api_key\": \"your_api_key\", \"search_term\": \"ipl\"}'

Output
------

The agent returns a JSON object containing the match results. The output includes the following fields:

- ``status``: The execution status ("success" or "failed")
- ``matches``: Array of match objects containing match details
- ``count``: Number of matches found
- ``search_term``: The search term used (if any)

Example:

.. code-block:: json

    {
        "status": "success",
        "matches": [
            {
                "matchInfo": {
                    "matchId": "1234",
                    "seriesName": "IPL 2024",
                    "team1": {"teamName": "Mumbai Indians"},
                    "team2": {"teamName": "Chennai Super Kings"},
                    "venueInfo": {
                        "ground": "Wankhede Stadium",
                        "city": "Mumbai"
                    }
                }
            }
        ],
        "count": 1,
        "search_term": "ipl"
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/crickAlert/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status and API connectivity.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Cricbuzz API service is available"
    }

Search Capabilities
-----------------

The agent supports searching by:

- Series name (e.g., "IPL", "World Cup")
- Team names
- Venue information (ground, city)
- Match format (T20, ODI, Test)
- Match description

Error Handling
-------------

The agent handles various error scenarios including:

- Missing API key
- Invalid API credentials
- API connection errors
- Invalid response format
- Search term not found

Each error scenario returns an appropriate error message in the response.

Contributing
------------

Contributions to improve or enhance the agent are welcome. Follow these steps:

1. Fork the repository
2. Create a new branch for your changes
3. Submit a pull request with a detailed description of your changes

Please ensure that all tests pass before submitting a pull request.

Requirements
-----------

- Python 3.6 or higher
- requests library
- RapidAPI key with access to Cricbuzz API
- Internet connection for API access

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.

Notes
-----

1. API rate limits may apply based on your RapidAPI subscription
2. Match availability depends on Cricbuzz API data updates
3. Search results are case-insensitive

Support
-------

For issues, questions, or suggestions:

1. Open an issue in the repository
2. Check existing issues for similar problems
3. Include API response details when reporting issues (excluding API keys)

Rate Limiting
------------

Please be aware of the following rate limits:

1. Respect the RapidAPI rate limits based on your subscription
2. Implement appropriate error handling for rate limit responses
3. Consider caching frequently requested data

Configuration
------------

The agent can be configured through:

1. API key configuration during initialization
2. Custom endpoints for different types of match data
3. Search term filtering for specific match information

For additional configuration options, refer to the Cricbuzz API documentation on RapidAPI.