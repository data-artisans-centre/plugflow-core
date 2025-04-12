Lyrics Agent
===========

The **Lyrics Agent** is designed to fetch song lyrics using the Lyrics.ovh API. It provides a simple interface to retrieve lyrics by specifying the artist name and song title.

Features
--------

- Fetch lyrics for any song using artist name and song title
- Simple integration with the agent framework
- Built-in error handling and validation
- Health check functionality

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests
    typing
    logging

Install the dependencies using pip:

.. code-block:: bash

    pip install requests typing logging

Parameters
----------

The agent accepts the following parameters:

- ``artist`` (str): The name of the artist/band
- ``title`` (str): The title of the song

Example Usage
-------------

To execute the agent:

.. code-block:: vscode terminal

    python main.py execute lyricist --params '{\"artist\":\"Kanye\\West\",\"title\":\"Stronger\"}'

Output
------

The agent returns the lyrics as a JSON object containing the following fields:

- ``artist``: The name of the artist
- ``title``: The title of the song
- ``lyrics``: The full lyrics text

Example successful response:

.. code-block:: json

    {
        "artist": "Coldplay",
        "title": "Yellow",
        "lyrics": "Look at the stars\nLook how they shine for you..."
    }

Example error response:

.. code-block:: json

    {
        "error": "No lyrics found for this song."
    }

Error Handling
-------------

The agent handles various error cases:

- Empty artist or title parameters
- Network connectivity issues
- API unavailability
- Lyrics not found for the requested song

Health Check
------------

The agent includes a ``health_check`` method that verifies the API's operational status by attempting to fetch lyrics for a known song.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Lyrics API is operational"
    }

Logging
-------

The agent uses a logging system to track operations and errors. Logs include:

- API request attempts
- Health check status
- Error messages and stack traces

Dependencies
-----------

- ``requests``: For making HTTP requests to the Lyrics.ovh API
- ``typing``: For type hints
- ``logging``: For logging functionality

Contributing
------------

To contribute to this agent:

1. Fork the repository
2. Create a new branch for your changes
3. Add or update tests as needed
4. Submit a pull request with a description of your changes

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.