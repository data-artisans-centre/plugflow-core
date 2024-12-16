Weather Agent
==============

The **Weather Agent** is designed to fetch real-time weather data using the Weatherbit API. It supports fetching weather details based on a city name or geographic coordinates.

Features
--------

- Fetch real-time weather details using the Weatherbit API.
- Supports input by city name or latitude/longitude coordinates.
- Customizable output with options for units (Metric/Imperial) and language.
- Health check functionality to verify the API service status.
- Detailed logging for debugging and monitoring.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: bash

    pip install -r requirements.txt

Parameters
----------

The agent accepts the following parameters:

- ``api_key`` (str, optional): Weatherbit API key.
- ``location`` (str, optional): Name of the city.
- ``lat`` (float, optional): Latitude of the location.
- ``lon`` (float, optional): Longitude of the location.
- ``units`` (str, optional): Measurement units ("M" for Metric, "I" for Imperial). Default: "M".
- ``language`` (str, optional): Language code for the response. Default: "en".

Example Usage
-------------

To execute the agent:

.. code-block:: bash
    python main.py execute weather --params "{\"api_key\":\"********************\",\"location\":\"Coimbatore,IN\"}"


.. code-block:: python

    from agents.weather import WeatherAgent

    weather_agent = WeatherAgent(api_key="your_api_key")

    # Fetch weather by city name
    result = weather_agent.execute(location="New York")
    print(result)

    # Fetch weather by coordinates
    result = weather_agent.execute(lat=40.7128, lon=-74.0060)
    print(result)

Output
------

The agent returns the fetched weather details as a dictionary. Example output:

.. code-block:: json

    {
        "location": {
            "name": "New York",
            "country": "US",
            "latitude": 40.7128,
            "longitude": -74.0060
        },
        "temperature": {
            "current": 22.5,
            "feels_like": 25.0
        },
        "weather": {
            "description": "Partly cloudy",
            "code": 802,
            "icon": "c02d"
        },
        "wind": {
            "speed": 3.1,
            "direction": 180,
            "direction_full": "South"
        },
        "humidity": 65,
        "pressure": {
            "station": 1015.2,
            "sea_level": 1016.5
        },
        "clouds": 40,
        "visibility": 10,
        "solar_radiation": 500,
        "uv_index": 5,
        "air_quality_index": 50
    }

Testing
-------

Unit tests for the Weather Agent are included in the ``weather_test.py`` file.

Run all tests:

.. code-block:: bash

    pytest weather_test.py

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method attempts to fetch weather data for a default location and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Weatherbit API service is available"
    }

Contributing
------------

Contributions to improve or enhance the agent are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.

