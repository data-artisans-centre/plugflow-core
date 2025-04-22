CGHS Hospitals Agent
====================

The **CGHS Hospitals Agent** allows you to fetch data about CGHS-empanelled hospitals in India using the Data.gov.in API.  
You can filter hospitals by city, name, or address, and customize the number of records returned.

Features
--------

- Retrieve CGHS empanelled hospitals from Data.gov.in.
- Supports filters like city name, hospital name, and address.
- Paginate through results with offset and limit.
- Input validation using Pydantic for cleaner integration.
- Structured JSON responses.

Installation
------------

Install the required dependencies using pip:

.. code-block:: bash

    pip install requests pydantic

Parameters
----------

The agent accepts the following parameters:

- ``api_key`` (str, required): API key for Data.gov.in. Cannot be blank.
- ``format`` (str, optional): Response format. Default is ``json``. Can also be ``xml`` or ``csv``.
- ``city_name`` (str, optional): Filter hospitals by city.
- ``hospital_name`` (str, optional): Filter hospitals by name.
- ``hospital_address`` (str, optional): Filter hospitals by address.
- ``offset`` (int, optional): Number of records to skip. Default is 0. Must be >= 0.
- ``limit`` (int, optional): Number of records to return. Default is 10. Range is 1–100.

Example Usage
-------------

To execute the agent, run the following command:

.. code-block:: bash

    python main.py execute cghs_hospitals --params '{"api_key": "YOUR_API_KEY", "city_name": "Delhi"}'

Replace ``"YOUR_API_KEY"`` with your actual API key from Data.gov.in.

Output
------

The agent returns a JSON object with hospital data:

Example JSON output:

.. code-block:: json

    {
        "status": "success",
        "data": [
            {
                "hospitalName": "ABC Hospital",
                "address": "123 Main Road",
                "city": "Delhi"
            },
            ...
        ]
    }

If no results are found or an error occurs:

.. code-block:: json

    {
        "status": "error",
        "message": "No hospitals found for the given filters."
    }

Testing
-------

To run the test suite for the agent:

.. code-block:: bash

    pytest agents/cghs_hospitals/tests

This includes tests for successful execution, input validation, and error handling.

Health Check
------------

The agent includes a ``health_check`` method to verify API connectivity.

Example output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "CGHS Hospitals API is reachable"
    }

Validation
----------

The agent uses Pydantic to validate input parameters:

- ``api_key`` must be a non-empty string.
- ``limit`` must be between 1 and 100.
- ``offset`` must be zero or a positive integer.

Invalid input raises a ``ValidationError`` with details.

Contributing
------------

1. Fork this repository.
2. Create a feature branch.
3. Commit your changes and add tests.
4. Submit a pull request.

References
----------

- Data.gov.in: https://data.gov.in
- CGHS API Dataset: https://data.gov.in/catalog/cghs-hospitals
- Pydantic Documentation: https://docs.pydantic.dev/

License
-------

This agent is licensed under the MIT License. See the LICENSE file for more details.
