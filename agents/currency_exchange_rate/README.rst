Currency Exchange Rate Agent
============================

The **Currency Exchange Rate Agent** is designed to fetch real-time exchange rate data using the Alpha Vantage API. 
It supports converting between valid currency pairs and provides exchange rate details in a JSON format.

Features
--------

- Fetch real-time exchange rates for any valid currency pair.
- Retrieve detailed currency conversion data in JSON format.
- Includes input validation for currency codes.
- Includes health check functionality to verify API connectivity.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or ``requirements.txt``:

.. code-block:: text

    requests
    pydantic

Install the dependencies using pip:

.. code-block:: bash

    pip install requests pydantic

Parameters
----------

The agent accepts the following parameters:

- ``apikey`` (str): The API key for accessing Alpha Vantage.
- ``from_currency`` (str): The currency to convert from (e.g., USD, BTC).
- ``to_currency`` (str): The currency to convert to (e.g., EUR, INR).

Example Usage
-------------

To execute the agent, use the following command:

.. code-block:: bash

    python main.py execute currency_exchange_rate --params '{"apikey": "your_api_key", "from_currency": "USD", "to_currency": "EUR"}'

Replace ``"your_api_key"`` with your actual Alpha Vantage API key. 
Update ``"from_currency"`` and ``"to_currency"`` as needed (e.g., USD, EUR, BTC).

For further details, please refer to the Alpha Vantage API documentation provided below.

Output
------

The agent returns the fetched exchange rate data as a JSON object. The object contains:

- ``Realtime Currency Exchange Rate``: A dictionary with detailed exchange rate information.

Example JSON output:

.. code-block:: json

    {
        "Realtime Currency Exchange Rate": {
            "1. From_Currency Code": "USD",
            "2. From_Currency Name": "United States Dollar",
            "3. To_Currency Code": "EUR",
            "4. To_Currency Name": "Euro",
            "5. Exchange Rate": "0.9312",
            "6. Last Refreshed": "2024-12-09 16:00:00",
            "7. Time Zone": "UTC",
            "8. Bid Price": "0.9310",
            "9. Ask Price": "0.9314"
        }
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/currency_exchange_rate/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method makes a test API call and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is operational"
    }

Validation
----------

The agent validates the input parameters to ensure correct usage:

- ``from_currency`` and ``to_currency`` must be valid currency codes (exactly 3 uppercase letters).
- Any invalid input will raise a ``ValueError`` with appropriate details.

Contributing
------------

Contributions to improve or enhance the agent are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

References
----------

- Alpha Vantage Website: https://www.alphavantage.co
- API Documentation: https://www.alphavantage.co/documentation/

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.
