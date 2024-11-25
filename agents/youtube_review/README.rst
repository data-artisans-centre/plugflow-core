YouTube Review Plugin
=====================

The **YouTube Review Plugin** is designed to fetch comments from a YouTube video. It supports fetching a configurable number of comments sorted by popularity.

Features
--------

- Fetch comments from any YouTube video using its URL.
- Retrieve a specified number of comments.
- Simple integration with the PlugFlow framework.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    youtube-comment-downloader

Install the dependencies using pip:

.. code-block:: bash

    pip install youtube-comment-downloader

Parameters
----------

The plugin accepts the following parameters:

- ``video_url`` (str): The URL of the YouTube video.
- ``max_comments`` (int): The maximum number of comments to fetch (default: 10).

Example Usage
-------------

To execute the plugin, use the PlugFlow CLI:

.. code-block:: bash

    python main.py execute youtube-review --params '{"video_url": "https://www.youtube.com/watch?v=abc123", "max_comments": 10}'

Output
------

The plugin returns the fetched comments as a list of JSON objects. Each comment contains the following fields:

- ``author``: The name of the commenter.
- ``comment``: The text of the comment.
- ``likes``: The number of likes the comment has received.
- ``time``: The timestamp when the comment was posted.

Example:

.. code-block:: json

    [
        {
            "author": "TestUser",
            "comment": "This is a great video!",
            "likes": 42,
            "time": "2 days ago"
        },
        {
            "author": "AnotherUser",
            "comment": "Amazing content!",
            "likes": 15,
            "time": "1 week ago"
        }
    ]

Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest plugins/youtube_review/tests

Health Check
------------

The plugin includes a ``health_check`` method to verify its operational status. The method attempts to fetch comments from a known dummy video and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is available"
    }

Contributing
------------

Contributions to improve or enhance the plugin are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

License
-------

This plugin is distributed under the MIT License. See the LICENSE file for more information.

