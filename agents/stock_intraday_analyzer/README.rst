Stock Intraday Analyzer Agent
=============================

The Stock Intraday Analyzer Agent is a Python-based utility for fetching and analyzing stock market intraday data using the Alpha Vantage API. It allows users to query intraday stock prices for a specific interval and perform health checks to verify API functionality.

Key Features
------------
- Fetch intraday stock data for intervals like 1min, 5min, 15min, 30min, and 60min.
- Validate request parameters using Pydantic models.
- Health check functionality to ensure service operability.
- Handles API errors and validates stock symbols.

Installation
------------
To install and set up the Stock Intraday Analyzer Agent:

1. Clone the repository:
   .. code-block:: bash

      git clone <repository_url>

2. Navigate to the project directory:
   .. code-block:: bash

      cd agents/stock_intraday_analyzer

3. Install the dependencies:
   .. code-block:: bash

      pip install -r requirements.txt

Dependencies
------------
The following dependencies are required to run the Stock Intraday Analyzer Agent:
- `requests`: For making HTTP requests to the Alpha Vantage API.
- `pydantic`: For validating input parameters.
- `core.base`: Custom base class for agents.
- `log`: Logging utility for error handling and debugging.

Usage
-----
**1. Executing the Agent**

To fetch intraday stock data, use the `execute` method of the `StockDataFetcher` class. Here is an example usage:

.. code-block:: python

   from agents.stock_intraday_analyzer.stock_data_fetcher import StockDataFetcher

   # Initialize the agent
   agent = StockDataFetcher()

   # Execute the agent to fetch stock data
   try:
       data = agent.execute(
           apikey="your_alpha_vantage_api_key",
           symbol="META",
           interval="1min",
           outputsize="compact",
           month=None
       )
       print(data)
   except ValueError as e:
       print(f"Error: {e}")

**2. Health Check**

Perform a health check to ensure the agent and API are operational:

.. code-block:: python

   health_status = agent.health(apikey="your_alpha_vantage_api_key")
   print(health_status)

Tests
-----
Unit tests are available in the `tests` directory. The tests cover:
- Successful execution with valid inputs.
- Error handling for invalid stock symbols.
- API health checks.

**Running Tests**

Run the tests using `pytest`:

.. code-block:: bash

   pytest agents/stock_intraday_analyzer/tests/

**Example Test**

A sample test case for the `StockDataFetcher`:

.. code-block:: python

   import pytest
   from unittest.mock import patch
   from agents.stock_intraday_analyzer.stock_data_fetcher import StockDataFetcher

   @patch("requests.get")
   def test_execute_success(mock_get):
       # Mock successful API response
       mock_get.return_value.status_code = 200
       mock_get.return_value.json.return_value = {
           "Meta Data": {"2. Symbol": "META"},
           "Time Series (1min)": {"2020-01-31 19:59:00": {"1. open": "200.6479"}}
       }

       agent = StockDataFetcher()
       result = agent.execute(
           apikey="test_api_key", 
           symbol="META", 
           interval="1min", 
           outputsize="compact", 
           month=None
       )
       assert result["Meta Data"]["2. Symbol"] == "META"

Contributing
------------
Contributions are welcome! To contribute:
1. Fork the repository.
2. Create a feature branch:
   .. code-block:: bash

      git checkout -b feature/your-feature

3. Commit your changes:
   .. code-block:: bash

      git commit -m "Add your feature description"

4. Push the branch:
   .. code-block:: bash

      git push origin feature/your-feature

5. Create a pull request.

License
-------
This project is licensed under the MIT License. See the LICENSE file for details.

Contact
-------
For issues or inquiries, please contact the project maintainer at <your_email>.

