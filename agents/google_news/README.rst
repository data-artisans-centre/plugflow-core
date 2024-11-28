NewsFetcher
===========

The **NewsFetcher** agent is designed to fetch news articles from the GNews API. It allows users to specify a category, country, and the number of articles to fetch, providing a flexible way to retrieve top headlines.

Features
--------

- Fetch top news articles by category.
- Specify the country for localized news.
- Retrieve a configurable number of articles.
- Simple integration with the `AgentBase` framework.

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

The agent accepts the following parameters:

- ``apikey`` (str) : Using api key to access the resource (Qnews)
- ``category`` (str): The category of news to fetch (e.g., "technology", "sports", "business").
- ``country`` (str): The ISO Alpha-2 code of the country for which the news is fetched.
- ``max_articles`` (int, optional): The maximum number of news articles to fetch (default: 5).

Example Usage
-------------

Execute the agent directly from the terminal using the following command:

.. code-block:: bash

    >python main.py execute google_news --params "{\"apikey\":\"hidden\",\"category\":\"technology\",\"country\":\"in\",\"max_articles\":5}"

**Note**: When running this command on Windows CMD, ensure to escape the double quotes in the JSON parameter properly as shown.

Output
------

The agent returns the fetched news as a JSON-formatted string. The JSON object contains metadata and article details such as title, description, URL, and publication time.

Example Output:

.. code-block:: json

    {
        "articles": [
            {
                "title": "Tech Giants Leading AI Innovation",
                "description": "A look into how major tech companies are advancing AI research.",
                "url": "https://example.com/tech-news",
                "publishedAt": "2024-11-24T10:00:00Z"
            },
            {
                "title": "The Rise of Quantum Computing",
                "description": "Quantum computing is closer than ever to becoming a reality.",
                "url": "https://example.com/quantum-news",
                "publishedAt": "2024-11-23T08:00:00Z"
            }
        ]
    }

Health Check
------------

The agent includes a ``health`` method to verify its operational status. This method performs a test request to the GNews API using predefined parameters to ensure the service is functional.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Service is available"
    }

Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/google_news/tests

Contributing
------------

Contributions to improve or enhance this agent are welcome. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

Best practices for contributions:
- Ensure adherence to PEP 8 coding standards.
- Include detailed docstrings and comments for new functionality.
- Write appropriate unit tests for any added or modified methods.

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.
