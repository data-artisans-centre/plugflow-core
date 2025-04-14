Amazon Product Agent
=====================

The **Amazon Product Agent** is designed to fetch product details from Amazon using the Real-Time Amazon Data API from RapidAPI. It provides search capabilities with various filtering options to find specific products.

Features
--------

- Search for products on Amazon based on keywords
- Filter results by various criteria (Prime eligibility, product condition, etc.)
- Sort results by relevance, price, ratings, and more
- Support for different Amazon country marketplaces
- Health check functionality to verify API service status
- Detailed logging for debugging and monitoring

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: bash

    pip install -r requirements.txt

Parameters
----------

The agent accepts the following parameters:

- ``api_key`` (str, optional): RapidAPI key for Real-Time Amazon Data API.
- ``query`` (str): Search query for products.
- ``page`` (int, optional): Page number for results. Default: 1.
- ``country`` (str, optional): Country code for Amazon marketplace. Default: "US".
- ``sort_by`` (str, optional): Sort results by. Default: "RELEVANCE".
- ``product_condition`` (str, optional): Product condition filter. Default: "ALL".
- ``is_prime`` (bool, optional): Filter for Prime eligible items. Default: false.
- ``deals_and_discounts`` (str, optional): Filter for deals. Default: "NONE".

Example Usage
-------------

To execute the agent via CLI:

.. code-block:: vscode
    
    python main.py execute amazon_product --params '{\"api_key\":\"api_key"\",\"query\":\"Iphone\\16\\pro\"}'  

To use in Python code:

.. code-block:: python

    from agents.amazon_product import AmazonProductAgent

    amazon_agent = AmazonProductAgent(api_key="your_api_key")

    # Basic product search
    result = amazon_agent.execute(query="Phone")
    print(result)

    # Search with advanced filters
    result = amazon_agent.execute(
        query="Gaming Laptop",
        page=1,
        country="US",
        sort_by="PRICE_LOW_TO_HIGH",
        product_condition="NEW",
        is_prime=True,
        deals_and_discounts="TODAYS_DEALS"
    )
    print(result)

Output
------

The agent returns the fetched product details as a dictionary. Example output structure:

.. code-block:: json

    {
        "status": "success",
        "data": {
            "query": "Phone",
            "total_results": 10000,
            "page": 1,
            "total_pages": 20,
            "results": [
                {
                    "position": 1,
                    "title": "Example Phone Product",
                    "asin": "B0AXXXXX",
                    "link": "https://www.amazon.com/product-link",
                    "image": "https://images-na.ssl-images-amazon.com/example-image.jpg",
                    "rating": 4.5,
                    "ratings_total": 1234,
                    "price": {
                        "value": 299.99,
                        "currency": "USD",
                        "symbol": "$",
                        "raw": "$299.99"
                    },
                    "is_prime": true,
                    "delivery": {
                        "price": {
                            "raw": "FREE",
                            "value": 0
                        }
                    }
                },
                // Additional product results...
            ]
        }
    }

Testing
-------

Unit tests for the Amazon Product Agent are included in the ``amazon_product_test.py`` file.

Run all tests:

.. code-block:: bash

    pytest agents/amazon_product/tests/amazon_product_test.py

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method attempts to perform a basic search and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Amazon Product API service is available"
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