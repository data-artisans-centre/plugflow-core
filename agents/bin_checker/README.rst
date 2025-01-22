BIN Checker Plugin
===================

The **BIN Checker Plugin** is designed to retrieve and validate information about Bank Identification Numbers (BINs). It uses an API to fetch details about the BIN, including the card type, issuing bank, country, and more.

Features
--------

- Retrieves detailed information about a given BIN code.
- Provides card type, issuing bank, and country information.
- Handles error scenarios such as invalid API keys, missing BINs, or rate limits.
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

The plugin accepts the following parameters:

- ``bin_code`` (str, required): The 6-digit BIN code to fetch information for.
- ``api_key`` (str, required): Your API key to access the BIN Checker API.

Example Usage
-------------

To execute the plugin, use the PlugFlow CLI. You can either pass the API key as a parameter or set it as an environment variable.

Example with API key as a parameter:

.. code-block:: bash

    python main.py execute bin_checker --params '{"bin_code": "302596", "api_key": "YOUR_API_KEY"}'

Output
------

The plugin returns a JSON object containing the following fields:

- ``bank_name``: The name of the issuing bank.
- ``bin``: The bank identification number is the first 6 digits of the issuer card.
- ``country``: The country where the card was issued.
- ``scheme``: The payment scheme (e.g., Visa, Mastercard).
- ``type``: The type of card (e.g., credit, debit).
- ``url``: The website of the bank.

Example:

.. code-block:: json

    {
        "bank_name": "Diners Club International",
        "bin": "302596",
        "country": "United States Of America",
        "scheme": "Discover",
        "type": "Credit",
        "url": "www.dinersclub.com"
    }

Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/bin_checker/tests

Health Check
------------

The plugin includes a ``health_check`` method to verify its operational status. The method attempts to validate the service availability and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is operational"
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

