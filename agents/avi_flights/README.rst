Flight Details Agent
====================

The **Flight Details Agent** is designed to retrieve real-time flight information using the AviationStack API. It fetches details such as flight status, departure, and arrival information, airline details, and more.

Features
--------

- Retrieves real-time flight details, including status, departure, and arrival information.
- Fetches details about the airline, flight number, and airport information.
- Handles error scenarios such as missing or invalid API keys, and invalid JSON responses.
- Easy integration with the PlugFlow framework.
- Configurable API key for secure access.

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

The agent accepts the following parameters:

- ``api_key`` (str, required): Your API access key, which can be found in your account dashboard.
- ``callback`` (str, optional): Use this parameter to specify a JSONP callback function name to wrap your API response in. Learn more about JSONP Callbacks.
- ``limit`` (int, optional): Specify a limit of results to return in your API response. Maximum allowed value is 100 below Professional Plan and 1000 on and above Professional Plan. Default value is 100.
- ``offset`` (int, optional): Specify an offset for pagination. Example: Specifying an offset of 10 in combination with a limit of 10 will show results 10-20. Default offset value is 0, starting with the first available result.
- ``flight_status`` (str, optional): Filter your results by flight status. Available values: scheduled, active, landed, cancelled, incident, diverted.
- ``flight_date`` (str, optional): Filter your results by providing a flight date in the format `YYYY-MM-DD`. Example: 2019-02-31.
- ``dep_iata`` (str, optional): Filter your results by departure city or airport using an IATA code.
- ``arr_iata`` (str, optional): Filter your results by arrival city or airport using an IATA code.
- ``dep_icao`` (str, optional): Filter your results by departure airport using an ICAO code.
- ``arr_icao`` (str, optional): Filter your results by arrival airport using an ICAO code.
- ``airline_name`` (str, optional): Filter your results by airline name.
- ``airline_iata`` (str, optional): Filter your results by airline IATA code.
- ``airline_icao`` (str, optional): Filter your results by airline ICAO code.
- ``flight_number`` (str, optional): Filter your results by providing a flight number. Example: 2557.
- ``flight_iata`` (str, optional): Filter your results by providing a flight IATA code. Example: MU2557.
- ``flight_icao`` (str, optional): Filter your results by providing a flight ICAO code. Example: CES2557.
- ``min_delay_dep`` (int, optional): Filter your results by providing a minimum amount of minutes in departure delay. Example: 7 for seven minutes of delay in departure.
- ``min_delay_arr`` (int, optional): Filter your results by providing a minimum amount of minutes in arrival delay. Example: 7 for seven minutes of delay in arrival.
- ``max_delay_dep`` (int, optional): Filter your results by providing a maximum amount of minutes in departure delay. Example: 60 for one hour of delay in departure.
- ``max_delay_arr`` (int, optional): Filter your results by providing a maximum amount of minutes in arrival delay. Example: 60 for one hour of delay in arrival.
- ``arr_scheduled_time_arr`` (str, optional): Filter your results by providing an arrival date in the format `YYYY-MM-DD`. Example: 2019-02-31.
- ``arr_scheduled_time_dep`` (str, optional): Filter your results by providing a departure date in the format `YYYY-MM-DD`. Example: 2019-02-31.

Example Usage
-------------

To execute the agent, use the PlugFlow CLI. The **`api_key`** is mandatory for all requests, while other parameters are optional and can be used based on the required API endpoint.

Example with API key and additional parameters:

.. code-block:: bash

    python main.py execute avi_flights --params '{"api_key": "YOUR_API_KEY", "flight_code": "AI202", "departure_airport": "DEL"}'

Output
------

The agent returns a JSON object containing the following fields:

- ``flight_number``: The flight number.
- ``status``: The current status of the flight (e.g., "On Time", "Delayed").
- ``departure``: The departure details, including airport and time.
- ``arrival``: The arrival details, including airport and time.
- ``airline``: The airline operating the flight.
- ``aircraft``: The aircraft type used for the flight.
- ``airport_details`` (optional): Additional information about the airports (only when requested).

Example:

.. code-block:: json

    {
        "flight_number": "AI202",
        "status": "On Time",
        "departure": {
            "airport": "Indira Gandhi International Airport",
            "time": "2025-01-28T14:30:00"
        },
        "arrival": {
            "airport": "Chhatrapati Shivaji Maharaj International Airport",
            "time": "2025-01-28T16:30:00"
        },
        "airline": "Air India",
        "aircraft": "Boeing 787 Dreamliner",
        "airport_details": {
            "departure_airport_name": "Indira Gandhi International Airport",
            "arrival_airport_name": "Chhatrapati Shivaji Maharaj International Airport"
        }
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/avi_flights/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method attempts to validate the service availability and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is operational"
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
