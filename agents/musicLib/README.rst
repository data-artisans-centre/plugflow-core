python main.py execute musicLib --params '{\"query\": \"Kendrick Lamar\", \"api_key\": \"043ca59f1fmsh4888cbf47d4856bp1a242ajsn9fbcf042a9b0\", \"limit\": 5, \"type\": \"tracks\"}'

SpotifySearch Agent
=================

The **SpotifySearch Agent** is designed to search and retrieve music information from Spotify using the RapidAPI platform. It provides flexible search capabilities for albums, artists, tracks, and playlists with comprehensive filtering options.

Features
--------

- Search Spotify music catalog
- Filter results by various criteria
- Album information retrieval
- Artist data access
- Health check functionality
- Integration with the PlugFlow framework

Installation
------------

Ensure that the required dependencies are installed from `requirements.txt`:

.. code-block:: text

    http.client
    json
    urllib.parse

Dependencies are part of Python's standard library, so no additional installation is required.

Parameters
----------

The agent accepts the following parameters:

- ``api_key`` (str): RapidAPI key for authentication (required)
- ``query`` (str): Search term for Spotify content (required)
- ``type`` (str, optional): Content type to search (default: 'multi')
- ``offset`` (int, optional): Results offset (default: 0)
- ``limit`` (int, optional): Maximum results (default: 10)
- ``top_results`` (int, optional): Number of top results (default: 5)

Example Usage
-------------

To execute the agent, use the PlugFlow CLI:

.. code-block:: vscode terminal

    python main.py execute musicLib --params '{\"query\": \"Kendrick Lamar\", \"api_key\": \"api_key\", \"limit\": 5, \"type\": \"tracks\"}'

With additional parameters:

.. code-block:: bash

    python main.py execute musicLib --params "{\"query\": \"Kendrick Lamar\", \"api_key\": \"api_key\", \"limit\": 5, \"type\": \"tracks\"}"

Output
------

The agent returns a JSON object containing the search results. The output includes the following fields:

- ``total_count``: Total number of results found
- ``albums``: Array of album objects (when searching albums)
- Each album contains:
  - ``uri``: Spotify URI
  - ``name``: Album name
  - ``artist``: Artist name
  - ``year``: Release year

Example:

.. code-block:: json

    {
        "total_count": 1,
        "albums": [
            {
                "uri": "spotify:album:123456",
                "name": "Abbey Road",
                "artist": "The Beatles",
                "year": 1969
            }
        ]
    }

Testing
-------

To test the agent, use the provided test suite:

.. code-block:: bash

    pytest musicLib_test.py

The test suite covers:
- Initialization tests
- API execution tests
- Error handling tests
- Health check verification
- Data filtering validation

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status:

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Spotify API service is available"
    }

Search Capabilities
-----------------

The agent supports searching by:

- Album name
- Artist name
- Track title
- Multiple content types simultaneously
- Year ranges
- Popularity metrics

Error Handling
-------------

The agent handles various error scenarios including:

- Missing API key
- Invalid API credentials
- Empty search query
- API connection errors
- Invalid response format
- Rate limiting errors

Each error returns a structured response with status "failed" and an error message.

Contributing
------------

Contributions are welcome. Please follow these steps:

1. Fork the repository
2. Create a feature branch
3. Add tests for new functionality
4. Submit a pull request

Ensure all tests pass before submitting your changes.

Requirements
-----------

- Python 3.10
- RapidAPI key with Spotify API access
- Internet connection
- Standard library modules (http.client, json, urllib.parse)

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more details.

