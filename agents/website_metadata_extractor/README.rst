Website Metadata Extractor Plugin
=================================

The **Website Metadata Extractor Plugin** is designed to fetch metadata (such as title, description, and keywords) from a website. This plugin allows you to extract relevant metadata from a webpage for further analysis or processing.

Features
--------
- Extract metadata from any website using its URL.
- Retrieve the **title**, **meta description**, and **meta keywords**.
- Simple integration with the **PlugFlow** framework.
- Handles error cases such as invalid URLs or network issues.

Installation
------------
Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    requests
    beautifulsoup4

Install the dependencies using pip:

.. code-block:: bash

    pip install requests beautifulsoup4

Parameters
----------
The plugin accepts the following parameters:

- `url` (str): The URL of the website to extract metadata from.
- `max_comments` (int): Maximum number of comments to fetch (default: 10). (If this plugin is modified to also include comments, this could be relevant.)

Example Usage
-------------
To execute the plugin, use the **PlugFlow CLI**:

.. code-block:: bash

    python main.py execute website-metadata-extractor --params '{"url": "https://example.com"}'

Output
------
The plugin returns the fetched metadata as a JSON object with the following fields:

- `Title`: The title of the webpage.
- `Meta Description`: The content of the meta description tag.
- `Meta Keywords`: The content of the meta keywords tag.

Example:

.. code-block:: json

    {
        "Title": "Example Domain",
        "Meta Description": "This domain is established to be used for illustrative examples in documents.",
        "Meta Keywords": "example, domain, illustrative"
    }

Health Check
-------------
The plugin includes a `health_check` method to verify its operational status. The method attempts to fetch metadata from a known dummy website and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is operational"
    }

Testing
-------
To test the plugin, use the provided test suite located in the `tests` directory.

Run all tests:

.. code-block:: bash

    pytest plugins/website_metadata_extractor/tests

Contributing
------------
Contributions to improve or enhance the plugin are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

License
-------
This plugin is distributed under the MIT License. See the LICENSE file for more information.
