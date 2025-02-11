URL to PDF Converter
====================

The **URL to PDF Converter** is an agent designed to convert web pages into PDF documents using the ConvertAPI service. This agent takes a URL as input and generates a PDF file that can be downloaded or saved locally.

Features
--------

- Converts any valid URL into a PDF document.
- Supports custom file names for the output PDF.
- Provides detailed responses, including the file URL, conversion cost, and status.
- Includes error handling for scenarios like invalid API keys, rate limits, or connectivity issues.
- Built-in health check to verify service availability.

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

- ``url`` (str, required): The URL to convert to a PDF.
- ``output_dir`` (str, required): Directory to save the converted PDF.
- ``api_key`` (str, required): Your API key for the ConvertAPI service.
- ``file_name`` (str, optional): Desired name of the output PDF file. Defaults to "output".

Example Usage
-------------

To execute the agent, use the PlugFlow CLI. The **`api_key`** is mandatory for all requests, while other parameters are optional and can be used based on the required API endpoint.

Example with API key and additional parameters:

.. code-block:: bash

    python main.py execute url_to_pdf_converter --params '{"url": "https://example.com", "output_dir": "/path/to/output", "api_key": "YOUR_API_KEY", "file_name": "example"}'


Output
------

The agent returns a JSON object containing the following fields:

- ``conversion_cost``: The cost of the conversion in API credits.
- ``file_name``: Name of the output PDF file.
- ``file_url``: URL to download the converted PDF.
- ``status``: Status of the conversion (e.g., success or error).
- ``error``: Error message in case of failure.

Example:

.. code-block:: json

    {
    "ConversionCost": 1,
    "Files": [
        {
            "FileName": "docs_google_com.pdf",
            "FileExt": "pdf",
            "FileSize": 4043950,
            "FileId": "3bi1bsqscqsz7t7oaq5os35cbhdlsdy3",
            "Url": "https://v2.convertapi.com/d/3bi1bsqscqsz7t7oaq5os35cbhdlsdy3/docs_google_com.pdf"
        }
    ]
}


Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/url2pdf/tests

Health Check
------------

The agent includes a ``health_check`` method to verify the operational status of the ConvertAPI service. The method attempts to validate the API key and service availability, returning a status message.

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

