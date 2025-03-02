=========================
Formula 1 API Sports Agent
=========================

Overview
========
This module provides a **SportsAgent** class for interacting with the Formula 1 API-Sports service. It enables fetching various Formula 1-related data, including team rankings, driver standings, circuit details, and race results.

Installation
============
To use this agent, ensure you have the required dependencies installed:

.. code-block:: bash

   pip install requests

Usage
=====

1. Create an instance of the **SportsAgent** class.
2. Provide your API key to fetch Formula 1 data.
3. Choose the data category and input necessary parameters.
4. Retrieve and display the response from the API.

.. code-block:: python

    python main.py execute formulaone_sports_agent

Classes
=======

Urls
----
A static utility class that defines the various API endpoints.

.. code-block:: python

   class Urls:
       @staticmethod
       def url_dict():
           return {
               "timezone": "https://v1.formula-1.api-sports.io/timezone",
               "seasons": "https://v1.formula-1.api-sports.io/seasons",
               "competitions": "https://v1.formula-1.api-sports.io/competitions",
               "circuit": "https://v1.formula-1.api-sports.io/circuits",
               "teams": "https://v1.formula-1.api-sports.io/teams",
               "drivers": "https://v1.formula-1.api-sports.io/drivers",
               "races": "https://v1.formula-1.api-sports.io/races",
               "rankings_teams": "https://v1.formula-1.api-sports.io/rankings/teams",
               "rankings_drivers": "https://v1.formula-1.api-sports.io/rankings/drivers",
               "rankings_races": "https://v1.formula-1.api-sports.io/rankings/races",
               "rankings_laps": "https://v1.formula-1.api-sports.io/rankings/fastestlaps",
               "rankings_startinggrids": "https://v1.formula-1.api-sports.io/rankings/startinggrid",
               "pitstops": "https://v1.formula-1.api-sports.io/pitstops",
           }

SportsAgent
-----------
A class that interacts with the Formula 1 API, inheriting from `AgentBase`.

Methods:

- **construct_url(base_url, params)**: Constructs a formatted URL with query parameters.
- **fetch_data(url, headers)**: Sends a request and fetches data from the API.
- **health_check(apikey)**: Checks API health status.
- **execute(apikey=None)**: Initiates an interactive API request session.

Example
-------

.. code-block:: python

   pytest agents/formulaone_sports_agent/tests

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
