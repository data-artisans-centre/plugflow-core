Stock Intraday Analyzer Agent
=============================

The **Stock Intraday Analyzer** agent is designed to fetch intraday stock data from Alpha Vantage. It supports retrieving real-time stock price information with configurable parameters, including stock symbol, time interval, and output size.

Features
--------

- Fetch intraday stock data from Alpha Vantage API.
- Supports multiple time intervals for intraday data (1min, 5min, 15min, 30min, 60min).
- Retrieve data in either compact or full output size.
- Integration with the PlugFlow framework.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests
    pydantic
    log

Install the dependencies using pip:

.. code-block:: bash

    pip install -r requirements.txt

Parameters
----------

The agent accepts the following parameters:

- ``symbol`` (str): The stock ticker symbol (e.g., "META", "IBM").
- ``interval`` (str): The time interval between data points (valid options: "1min", "5min", "15min", "30min", "60min").
- ``apikey`` (str): Your Alpha Vantage API key.
- ``outputsize`` (str): The size of the output data. It can either be "compact" (default) or "full".
- ``month`` (str, optional): The specific month to fetch data for in the format YYYY-MM (optional).

Example Usage
-------------

To execute the agent, use the PlugFlow CLI:

.. code-block:: bash

    python main.py execute stock_intraday_analyzer --params '{"symbol": "META", "interval": "1min", "apikey": "your_api_key", "outputsize": "compact", "month": "2020-01"}'

Output
------

The agent returns the intraday stock data as a JSON object containing various fields such as open, high, low, close prices, and volume for each time point.

Example:

.. code-block:: json

    {
        "Meta Data": {
            "1. Information": "Intraday (1min) open, high, low, close prices and volume",
            "2. Symbol": "META",
            "3. Last Refreshed": "2020-01-31 19:59:00",
            "4. Interval": "1min",
            "5. Output Size": "Compact",
            "6. Time Zone": "US/Eastern"
        },
        "Time Series (1min)": {
            "2020-01-31 19:59:00": {
                "1. open": "200.6479",
                "2. high": "200.6479",
                "3. low": "200.6479",
                "4. close": "200.6479",
                "5. volume": "100"
            }
        }
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/stock_intraday_analyzer/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. It attempts to fetch intraday data for a sample stock and returns a status message.

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
