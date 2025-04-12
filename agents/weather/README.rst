Weather Agent
==============

The **Weather Agent** is designed to fetch real-time weather data using the Open Weather API from RapidAPI. It supports fetching weather details based on a city name and optional country code.

Features
--------

- Fetch real-time weather details using the Open Weather API.
- Supports input by city name with optional country code.
- Detailed weather information including temperature, wind, humidity, and more.
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

- ``api_key`` (str, optional): RapidAPI key for Open Weather API.
- ``city`` (str): Name of the city.
- ``country_code`` (str, optional): Two-letter country code.

Example Usage
-------------

To execute the agent via CLI:

.. code-block:: bash
    
    python main.py execute weather --params "{\"api_key\":\"your_api_key\",\"city\":\"Coimbatore\",\"country_code\":\"IN\"}"

To use in Python code:

.. code-block:: python

    from agents.weather import WeatherAgent

    weather_agent = WeatherAgent(api_key="your_api_key")

    # Fetch weather by city name
    result = weather_agent.execute(city="New York")
    print(result)

    # Fetch weather by city name and country code
    result = weather_agent.execute(city="London", country_code="GB")
    print(result)

Output
------

The agent returns the fetched weather details as a dictionary. Example output:

.. code-block:: json

    {
        "location": {
            "name": "New York",
            "country": "US"
        },
        "temperature": {
            "current": 22.5,
            "feels_like": 25.0,
            "min": 20.0,
            "max": 24.0
        },
        "weather": {
            "description": "Partly cloudy",
            "main": "Clouds",
            "icon": "02d"
        },
        "wind": {
            "speed": 3.1,
            "direction": 180
        },
        "humidity": 65,
        "pressure": 1015.2,
        "clouds": 40,
        "visibility": 10000
    }

Testing
-------

Unit tests for the Weather Agent are included in the ``weather_test.py`` file.

Run all tests:

.. code-block:: bash

    pytest agents/weather/tests/weather_test.py

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method attempts to fetch weather data for London, GB and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Open Weather API service is available"
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