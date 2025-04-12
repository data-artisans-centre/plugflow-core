Ticker Analysis Agent
=====================

Overview
--------
The `Ticker Analysis Agent` is a Python package designed to fetch and analyze stock ticker data using Yahoo Finance (`yfinance`). It provides insights into stock performance, company details, and market trends through easy-to-use interfaces.

Features
--------
- **Ticker Validation**: Validates and parses input data for stock ticker analysis using Pydantic.
- **Current and Historical Prices**: Retrieves the latest closing price, previous close, and calculates the percentage price change.
- **Company Insights**: Fetches company name, sector, market capitalization, P/E ratio, and dividend yield.
- **Error Handling**: Provides clear error messages for invalid tickers or data retrieval issues.
- **Health Check**: Ensures the agent is operational with a built-in health diagnostic.

Installation
------------
Install the package using `pip`:

.. code-block:: bash

    pip install ticker-analysis-agent

Usage
-----
### Example: Analyzing Stock Tickers
The `TickerAgent` can analyze a list of stock tickers and provide detailed insights. Here's how to use it:

.. code-block:: python

    from ticker_analysis_agent import TickerAgent

    agent = TickerAgent()
    
    # Define a request for analysis
    ticker_request = {
        "stock_tickers": "AAPL, GOOGL, MSFT",
        "max_tickers": 3,
        "start_date": "2024-01-01",
        "end_date": "2024-12-01"
    }

    # Execute analysis
    results = agent.execute(ticker_request)
    print(results)

### Health Check
Verify the agent's functionality with the built-in health check:

.. code-block:: python

    health_status = agent.health_check()
    print(health_status)

Modules and Classes
-------------------
### `TickerRequest`
A Pydantic model for validating ticker request inputs.

- **Fields**:
  - `stock_tickers`: A comma-separated string of stock tickers.
  - `max_tickers`: The maximum number of tickers to analyze (default: 5; range: 1–10).
  - `start_date`: Optional start date for historical data (format: `YYYY-MM-DD`).
  - `end_date`: Optional end date for historical data (format: `YYYY-MM-DD`).

### `TickerData`
A Pydantic model representing the output of a ticker analysis.

- **Fields**:
  - `ticker`: Stock ticker symbol.
  - `current_price`: Latest closing price.
  - `previous_close`: Price at the previous close.
  - `price_change_percent`: Percentage price change.
  - `company_name`: The full name of the company.
  - `sector`: The business sector of the company.
  - `market_cap`: Market capitalization of the company.
  - `pe_ratio`: Price-to-Earnings (P/E) ratio.
  - `dividend_yield`: Dividend yield percentage.
  - `error`: Error message if data retrieval fails.

### `TickerAgent`
The primary class to fetch and analyze stock ticker data.

- **Methods**:
  - `execute(ticker_request: Dict[str, Any])`: Validates input and fetches analysis for multiple tickers.
  - `_analyze_single_ticker(ticker: str, start_date: Optional[str], end_date: Optional[str])`: Analyzes a single ticker and returns a `TickerData` object.
  - `health_check()`: Checks the operational status of the agent.

Logging
-------
This package uses a custom logger to track activity and errors. Debug logs provide detailed insights into ticker analysis operations.

Contributing
------------
Contributions are welcome! Please submit pull requests or open issues on the GitHub repository.

License
-------
This project is licensed under the MIT License.
