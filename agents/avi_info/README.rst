Aviation Data Agent
====================

The **Aviation Data Agent** retrieves real-time and historical aviation-related data using the AviationStack API. It fetches details about airports, airlines, aircraft, aircraft types, and more.
The documentation is available here : https://aviationstack.com/documentation

Features
--------

- Fetches data on airports, airlines, airplanes, aircraft types, aviation taxes, cities, and countries.
- Supports filtering using parameters such as API key, search queries, limits, and offsets.
- Handles error scenarios, including missing API keys, invalid parameters, rate limits, and server errors.
- Seamless integration with the PlugFlow framework.
- Secure API key configuration.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests
    pytest

Install the dependencies using pip:

.. code-block:: bash

    pip install -r requirements.txt

Parameters
----------

The agent supports the following parameters:

- ``api_key`` (str, required): Your API access key, found in your AviationStack account.
- ``category`` (str, required): Specifies the type of aviation data to fetch. Available categories:
  - ``airports``: Retrieves airport details.
  - ``airlines``: Retrieves airline details.
  - ``airplanes``: Retrieves airplane details.
  - ``aircraft_types``: Retrieves aircraft type details.
  - ``taxes``: Retrieves aviation tax details.
  - ``cities``: Retrieves city details related to aviation.
  - ``countries``: Retrieves country details related to aviation.

Example Usage
-------------

To execute the agent, use the PlugFlow CLI. The **`api_key`** is mandatory for all requests, while other parameters are optional and can be used based on the required API endpoint.

Example request:

.. code-block:: bash

    python main.py execute aviation_agent --params '{"api_key": "YOUR_API_KEY", "category": "airports", "search": "London"}'

Output
------

The agent returns a JSON object containing the requested aviation data.
Please note that the entire output is too long to be printed here. Hence just a snippet is given below for category airports :

.. code-block:: json

    {
      "id": "2880535",
      "gmt": "-10",
      "airport_id": "1",
      "iata_code": "AAA",
      "city_iata_code": "AAA",
      "icao_code": "NTGA",
      "country_iso2": "PF",
      "geoname_id": "6947726",
      "latitude": "-17.05",
      "longitude": "-145.41667",
      "airport_name": "Anaa",
      "country_name": "French Polynesia",
      "phone_number": null,
      "timezone": "Pacific/Tahiti"
    }

Testing
-------

The project includes a comprehensive test suite using `pytest` to ensure robustness and reliability.

**Features tested:**

- Successful data fetching.
- Handling of missing API keys.
- API errors (e.g., invalid API key, bad requests, rate limits).
- HTTP errors and exceptions.
- JSON parsing errors.
- Health check validation.

Run all tests:

.. code-block:: bash

    pytest agents/aviation_agent/tests

To run a specific test:

.. code-block:: bash

    pytest agents/aviation_agent/tests/test_aviation_fetcher.py::test_execute_success

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
