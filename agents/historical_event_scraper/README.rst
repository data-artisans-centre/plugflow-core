Day Events Plugin
==================

The **Day Events Plugin** fetches historical events for the current date from the "On This Day" API. It integrates seamlessly with the PlugFlow framework to provide easy access to interesting historical data.

Features
--------

- Fetch historical events for the current day.
- Retrieves data from the "On This Day" API.
- Simple integration with the PlugFlow framework.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests

Install the dependencies using pip:

.. code-block:: bash

    pip install requests

Parameters
----------

The plugin does not require any external input. It automatically determines the current date and fetches the corresponding historical events.

Example Usage
-------------

To execute the plugin, use the PlugFlow CLI:

.. code-block:: bash

    python main.py execute day-events

Output
------

The plugin returns the historical events for the current date as a list of JSON objects. Each event contains the following fields:

- ``year``: The year the event occurred.
- ``description``: A brief description of the event.
- ``wikipedia`` (optional): Links to related Wikipedia articles (if available).

Example:

.. code-block:: json

    [
        {
            "year": "1922",
            "description": "Howard Carter and Lord Carnarvon enter the tomb of Pharaoh Tutankhamun.",
            "wikipedia": [
                {
                    "title": "Howard Carter",
                    "wikipedia": "https://en.wikipedia.org/wiki/Howard_Carter"
                },
                {
                    "title": "Tutankhamun",
                    "wikipedia": "https://en.wikipedia.org/wiki/Tutankhamun"
                }
            ]
        },
        {
            "year": "1942",
            "description": "The movie Casablanca premieres in New York City.",
            "wikipedia": [
                {
                    "title": "Casablanca",
                    "wikipedia": "https://en.wikipedia.org/wiki/Casablanca_(film)"
                }
            ]
        }
    ]

Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest plugins/day_events/tests

Health Check
------------

The plugin includes a ``health_check`` method to verify its operational status. The method queries a known valid API endpoint (`/1/1/events.json`) and checks for the presence of event data.

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
