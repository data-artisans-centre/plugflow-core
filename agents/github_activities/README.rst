GitHub Activities Plugin
=========================

The **GitHub Activities Plugin** is designed to fetch events from a public GitHub repository. It supports fetching a configurable number of events like forking, push, etc sorted by date.

Features
--------

- Fetch events of a GitHub repo using its URL.
- Retrieve a specified number of events.
- Simple integration with the PlugFlow framework.

Installation
------------

The plugin uses an API and thus does not need the Installation of any dependencies.

Parameters
----------

The plugin accepts the following parameters:

- ``repo_url`` (str): The URL of the GitHub repository.
- ``max_events`` (int): The maximum number of events to fetch (default: 10).

Example Usage
-------------

To execute the plugin, use the PlugFlow CLI:

.. code-block:: bash

    python main.py execute github-activities --params '{"repo_url": "https://github.com/data-artisans-centre/plugflow-core", "max_events": 10}'

Output
------

The plugin returns the fetched events as a list of JSON objects. Each event contains the following fields:

- ``id``: A unique identifier for the event.
- ``type``: The type of event, such as PullRequestReviewEvent.
- ``actor``: Details about the user who performed the event:
    - ``id``: Unique identifier of the user.
    - ``login``: Username of the user.
    - ``display_login``: Display name of the user.
    - ``avatar_url``: URL of the user's avatar image.
    - ``repo``: Information about the repository associated with the event:

- ``id``: Unique identifier of the repository.
- ``name``: Name of the repository in the format owner/repo.
- ``url``: API URL of the repository.
- ``payload``: Details specific to the event type:
- ``action``: The action performed, such as created.

The response will have more parts specific to the type of event.

Example:

.. code-block:: json

    
[
  {
    "id": "1234567",
    "type": "PullRequestReviewEvent",
    "actor": {
      "id": 1234567,
      "login": "JaneDoe",
      "display_login": "JaneDoe",
      "avatar_url": "https://avatars.githubusercontent.com/u/123456?"
    },
    "repo": {
      "id": 12345,
      "name": "user/repo",
      "url": "https://api.github.com/repos/user/repo"
    },
    "payload": {
      "action": "created",
      "review": {
        "id": 1234567,
        "state": "changes_requested",
        "html_url": "https://github.com/user/repo/pull/2#pullrequestreview-123456",
        "pull_request_url": "https://api.github.com/repos/user/repo/pulls/2",
        "submitted_at": "2024-11-25T12:51:25Z"
      },
      "pull_request": {
        "id": 324562,
        "html_url": "https://github.com/user/repo/pull/3",
        "title": "Added templates",
        "created_at": "2024-11-25T12:44:43Z",
        "updated_at": "2024-11-25T12:51:25Z",
        "state": "open"
      }
    }
  }
]


Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/github_activities/tests

Health Check
------------

The plugin includes a ``health_check`` method to verify its operational status. The method attempts to fetch events from a known repo and returns a status message.

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

