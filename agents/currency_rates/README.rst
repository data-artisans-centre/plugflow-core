Currency Conversion Rates Plugin
=====================

The **Currency Conversion Rates Plugin** is designed to fetch the live currency exchange rates from one currency to another.

Features
--------

- Fetch currency exchange rate from one currency(base currency) to another(target_currency).
- Simple integration with the PlugFlow framework.

Installation
------------

The plugin uses an API and thus does not need the Installation of any dependencies.

Parameters
----------

The plugin accepts the following parameters:

- ``api_key`` (str): The API key used to authenticate and access the API.
- ``base_currency`` (int): The ISO 4217 three-letter currency code representing the currency to convert from.  
- ``target_currency`` (int): The ISO 4217 three-letter currency code representing the currency to convert to.

Example Usage
-------------

To execute the plugin, use the PlugFlow CLI:

.. code-block:: bash

    python main.py execute currency_rates --params '{"api_key": "hidden", "base_currency":"USD", "target_currency":"GBP"}'

**Note:** When running this command on Windows CMD, ensure to escape the double quotes in the JSON parameter properly as shown.

Output
------

The plugin returns the fetched rates as a JSON-formatted string. The JSON object includes metadata, such as the time of the last update in both Unix and UTC formats.    

Example Output:

.. code-block:: json

    {
        "result": "success",
        "documentation": "https://www.exchangerate-api.com/docs",
        "terms_of_use": "https://www.exchangerate-api.com/terms",
        "time_last_update_unix": 1733184002,
        "time_last_update_utc": "Tue, 03 Dec 2024 00:00:02 +0000",
        "time_next_update_unix": 1733270402,
        "time_next_update_utc": "Wed, 04 Dec 2024 00:00:02 +0000",
        "base_code": "EUR",
        "target_code": "GBP",
        "conversion_rate": 0.8294
    }

Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/currency_rates/tests

Health Check
------------

The plugin includes a ``health_check`` method to verify its operational status. The method performs a test request to the currency rates API using predefined parameters to ensure the service is functional.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is available"
    }

Contributing
------------

Contributions to improve or enhance the plugin are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

License
-------

This plugin is distributed under the MIT License. See the LICENSE file for more information.

