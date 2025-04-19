 Valid Email Agent
=================

The **Valid Email Agent** validates email addresses using the Abstract Email Validation API. It checks the format, domain, MX records, and other attributes to determine if an email is valid and reachable.
The documentation is available here: https://www.abstractapi.com/email-verification-api

Features
--------

- Verifies if an email address is valid, properly formatted, and active.
- Provides domain insights, local-part checks, and more.
- Handles various error scenarios including missing or invalid API keys.
- Seamless integration with the PlugFlow framework.
- Secure API key handling and validation.

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

- ``api_key`` (str, required): Your API key from the Abstract API dashboard.
- ``email`` (str, required): The email address to validate.

Example Usage
-------------

To execute the agent, use the PlugFlow CLI. Both **`api_key`** and **`email`** are mandatory parameters.

Example request:

.. code-block:: bash

    python main.py execute valid_email --params '{"api_key": "YOUR_API_KEY", "email": "info@example.com"}'

Output
------

The agent returns a JSON object indicating whether the email is valid, along with detailed metadata.

Example output:

.. code-block:: json

    {
      "status": "success",
      "data": {
        "is_valid": true,
        "email": "info@example.com",
        "domain": "example.com",
        "local_part": "info"
      }
    }

Testing
-------

The project includes a comprehensive test suite using `pytest` to ensure reliability and correctness.

**Features tested:**

- Successful email validation.
- Handling of missing or invalid API keys.
- Invalid email formats.
- API error responses.
- Health check responses.

Run all tests:

.. code-block:: bash

    pytest agents/valid_email/tests

To run a specific test:

.. code-block:: bash

    pytest agents/valid_email/tests/test_valid_email_agent.py::test_execute_valid_email

Health Check
------------

The agent includes a ``health_check`` method to verify service availability and API connectivity.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "API reachable"
    }

Contributing
------------

Contributions are welcome to improve the Valid Email Agent.

1. Fork the repository.
2. Create a new branch for your updates.
3. Submit a pull request with clear documentation of your changes.

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more details.

