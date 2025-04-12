python main.py execute MovieHive --params '{\"api_key\":\"83674f8b\",\"title\":\"Avatar\"}'

MovieHive Agent
===============

The **MovieHive Agent** is designed to fetch movie information using the OMDB API. It allows users to retrieve details about any movie by providing its title and an API key.

Features
--------

- Fetch movie details from the OMDB API using the movie title.
- Retrieve full movie plots, cast, ratings, and other metadata.
- Perform a health check to verify the API's operational status.



Parameters
----------

The agent accepts the following parameters:

- ``title`` (str): The title of the movie to search for.
- ``api_key`` (str): The API key required to access the OMDB API.

Example Usage
-------------

To execute the agent and fetch movie details, use the following Python code:

.. code-block:: vscode

python main.py execute MovieHive --params '{\"api_key\":\"83674f8b\",\"title\":\"Avatar\"}'

Output
------

The agent returns the fetched movie details as a JSON object. Each response contains fields such as:

- ``Title``: The movie title.
- ``Year``: The release year.
- ``Genre``: The movie genre.
- ``Director``: The director's name.
- ``Actors``: The main cast.
- ``Plot``: A detailed plot summary.
- ``Ratings``: Ratings from IMDb, Rotten Tomatoes, etc.
- ``Awards``: How many awards the movie has won


Example:

.. code-block:: json

    {
        "Title": "Inception",
        "Year": "2010",
        "Genre": "Action, Adventure, Sci-Fi",
        "Director": "Christopher Nolan",
        "Actors": "Leonardo DiCaprio, Joseph Gordon-Levitt, Elliot Page",
        "Plot": "A thief who enters the dreams of others to steal secrets is given a task to plant an idea in a target's mind.",
        "Ratings": [
            {"Source": "Internet Movie Database", "Value": "8.8/10"},
            {"Source": "Rotten Tomatoes", "Value": "87%"}
        ]
        "Awards" : "5"
    }

Testing
-------

To test the agent, use the provided test cases located in the `tests` directory.

Run all tests:

.. code-block:: bash

    pytest agents/MovieHive/tests/

Health Check
------------

The agent includes a ``health_check`` method to verify the API’s operational status. It attempts to fetch information about a known movie and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "OMDB API is operational"
    }

Contributing
------------

Contributions to improve or enhance the agent are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your modifications.

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.

