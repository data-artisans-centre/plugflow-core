NBA API Agent
=============

Overview
--------
The `SportsAgent` class interacts with the NBA API to retrieve various basketball-related data, such as team statistics, player information, game schedules, and standings.

Modules
-------
- `requests`: Handles HTTP requests to the NBA API.
- `json`: Parses and formats JSON data.
- `logging`: Logs API interactions and errors.
- `urllib.parse.urlencode`: Encodes query parameters for API requests.
- `core.base.AgentBase`: Base class for agents.

Usage
=====

1. Create an instance of the **SportsAgent** class.
2. Provide your API key to fetch Formula 1 data.
3. Choose the data category and input necessary parameters.
4. Retrieve and display the response from the API.

.. code-block:: python

    python main.py execute nba_ports_agent

Classes
-------

Urls
^^^^
A helper class that provides a dictionary mapping API endpoints to their corresponding URLs.

.. code-block:: python

    class Urls:
        @staticmethod
        def url_dict():
            return {
                "seasons": "https://v2.nba.api-sports.io/seasons",
                "leagues": "https://v2.nba.api-sports.io/leagues",
                "games": "https://v2.nba.api-sports.io/games",
                "games_statistics": "https://v2.nba.api-sports.io/games/statistics",
                "teams": "https://v2.nba.api-sports.io/teams",
                "teams_statistics": "https://v2.nba.api-sports.io/teams/statistics",
                "players": "https://v2.nba.api-sports.io/players",
                "players_statistics": "https://v2.nba.api-sports.io/players/statistics",
                "standings": "https://v2.nba.api-sports.io/standings"
            }

SportsAgent
^^^^^^^^^^^
A class that facilitates interaction with the NBA API.

.. code-block:: python

    class SportsAgent(AgentBase):
        BASE_HEADERS = {
            "x-rapidapi-host": "v2.nba.api-sports.io"
        }

SportsAgent
-----------
A class that interacts with the NBA API, inheriting from `AgentBase`.

Methods:

- **construct_url(base_url, params)**: Constructs a formatted URL with query parameters.
- **fetch_data(url, headers)**: Sends a request and fetches data from the API.
- **health_check(apikey)**: Checks API health status.
- **execute(apikey=None)**: Initiates an interactive API request session.

Example
-------

.. code-block:: python

   pytest agents/nba_sports_agent/tests

Logging
=======
This module includes logging functionality for error handling and debugging:

- **Logging Levels**: INFO, ERROR
- **Error Handling**: Catches request failures and invalid API key issues.

.. code-block:: python

   logger = logging.getLogger(__name__)
   logger.error("Invalid API key provided.")

Exception Handling
==================
The agent includes exception handling for:

- HTTP request failures
- Invalid API key errors
- Invalid user input (category selection errors, missing API key)

To modify exception handling, edit the `fetch_data()` and `execute()` methods.
