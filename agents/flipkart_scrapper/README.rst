Flipkart Scrapper Agent
=======================

The **Flipkart Scrapper Agent** is designed to fetch product details from Flipkart based on a search query. It supports fetching a configurable number of product results.

Features
--------

- Fetch product details from Flipkart using a search term.
- Retrieve a specified number of product results.
- Returns product details such as name, price, rating, offers, and delivery charges.
- Simple integration with the PlugFlow framework.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests
    beautifulsoup4

Install the dependencies using pip:

.. code-block:: bash

    pip install requests beautifulsoup4
    pip install pydantic

Parameters
----------

The agent accepts the following parameters:

- ``item_name`` (str): The name of the product to search for.
- ``max_products`` (int): The maximum number of products to fetch (default: 10).

Example Usage
-------------

To execute the agent, use the PlugFlow CLI:

.. code-block:: bash

    python main.py execute flipkart-scrapper --params '{"item_name": "laptop", "max_products": 5}'

Output
------

The agent returns the fetched product details as a list of JSON objects. Each product contains the following fields:

- ``product_name``: The name of the product.
- ``category``: The category of the product (currently set to "N/A").
- ``sub_category``: The sub-category of the product (currently set to "N/A").
- ``price``: The price of the product.
- ``offers``: The available offers for the product (if any).
- ``delivery_charge``: The delivery charge (or "Free delivery" if applicable).
- ``rating``: The rating of the product (if available).
- ``customers_bought``: Information on the number of customers who bought the product (currently set to "N/A").

Example:

.. code-block:: json

    [
        {
            "product_name": "HP Laptop 15s",
            "category": "N/A",
            "sub_category": "N/A",
            "price": "₹55,999",
            "offers": "10% off on ICICI Credit Cards",
            "delivery_charge": "Free delivery",
            "rating": "4.5",
            "customers_bought": "N/A"
        },
        {
            "product_name": "Dell Inspiron 14",
            "category": "N/A",
            "sub_category": "N/A",
            "price": "₹65,499",
            "offers": "No offers",
            "delivery_charge": "₹99",
            "rating": "4.3",
            "customers_bought": "N/A"
        }
    ]

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/flipkart_scrapper/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method performs a basic connectivity test and returns a status message.

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
