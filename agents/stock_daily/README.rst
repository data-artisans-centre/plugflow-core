Stock Daily Fetcher
=================

The **Stock Daily Fetcher** is designed to fetch daily stock price data using the Alpha Vantage API. It supports fetching detailed stock information, including open, high, low, close prices, and volume for a given stock symbol.

Features
--------

- Fetch daily stock prices for any valid stock symbol.
- Retrieve data in both JSON format.
- Supports configurable output sizes (compact or full).
- Includes health check functionality to verify API connectivity.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

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
- ``symbol`` (str): The stock ticker symbol (e.g., TSCO.LON).
- ``outputsize`` (str): The size of the output data, either ``compact`` (recent data) or ``full`` (historical data).
- ``datatype`` (str): The format of the data will be ``json``.

Example Usage
-------------

To execute the agent, use the following command:

.. code-block:: bash

    python main.py execute stock-daily --params '{"apikey": "your_api_key", "symbol": "your_symbol", "outputsize": "full", "datatype": "json"}'

Replace `"your_api_key"` with your actual Alpha Vantage API key and update other parameters as needed.
Replace `"your_symbol"` with symbols like IBM,META,AAPL,etc. 

For further details please refer the API documentation provided below.



Output
------

The agent returns the fetched stock data as a JSON object or CSV string. For JSON, the object contains:

- ``Meta Data``: Metadata about the request.
- ``Time Series (Daily)``: A dictionary with daily stock price data.

Example JSON output:

.. code-block:: json

    {
        "Meta Data": {
            "1. Information": "Daily Prices (open, high, low, close) and Volumes",
            "2. Symbol": "TSCO.LON",
            "3. Last Refreshed": "2024-12-09",
            "4. Output Size": "Full size",
            "5. Time Zone": "US/Eastern"
        },
        "Time Series (Daily)": {
            "2024-12-09": {
                "1. open": "367.2000",
                "2. high": "368.1110",
                "3. low": "363.9000",
                "4. close": "364.8000",
                "5. volume": "7332541"
            }
        }
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/stock_daily/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method makes a test API call and returns a status message.

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

References
----------

- Alpha Vantage Website: https://www.alphavantage.co
- API Documentation: https://www.alphavantage.co/documentation/

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.
