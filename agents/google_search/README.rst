SearchAgent
===========

The **SearchAgent** is a powerful tool designed to fetch search results using the SerpAPI. It provides users with the flexibility to specify query parameters such as location, language, and region while retrieving results seamlessly.

Features
--------

- Execute search queries with customizable parameters.
- Specify location, language, and country for localized search results.
- Health check to validate API connectivity.
- Integrated with the ``AgentBase`` framework for easy deployment.

Installation
------------

To use **SearchAgent**, ensure the required dependencies are installed. Add the following to your environment or ``requirements.txt``:

.. code-block:: text

    requests
    pydantic

Install the dependencies using pip:

.. code-block:: bash

    pip install requests pydantic

Parameters
----------

The agent accepts the following parameters for execution:

- ``query`` (str): The search query string.
- ``location`` (str, optional): The geographical location to originate the search (e.g., "New York").
- ``gl`` (str, optional): The country for the Google search (ISO Alpha-2 code, e.g., "us").
- ``hl`` (str, optional): The language for the Google search (e.g., "en" for English).
- ``apikey`` (str): The API key for accessing SerpAPI resources.

Example Usage
-------------

Execute the agent directly from the terminal using the following command:

.. code-block:: bash

    python main.py execute google_search --params "{\"query\":\"latest technology trends\",\"location\":\"New York\",\"gl\":\"us\",\"hl\":\"en\",\"apikey\":\"hidden\"}"

**Note**: For Windows CMD, escape the double quotes in the JSON parameter properly as shown.

Output
------

The agent returns search results as a JSON-formatted string. The JSON object contains metadata and detailed results for the query.

Example Output:

.. code-block:: json

    {
        "search_metadata": {
            "status": "Success",
            "id": "12345",
            "processing_time": "1.2s"
        },
        "search_information": {
            "total_results": 2600000000,
            "time_taken": "1.44s"
        },
        "organic_results": [
            {
                "title": "Coffee - Wikipedia",
                "link": "https://en.wikipedia.org/wiki/Coffee",
                "snippet": "Coffee is a brewed drink prepared from roasted coffee beans..."
            },
            {
                "title": "21 Excellent Coffee Shops in Austin",
                "link": "https://austin.eater.com/maps/best-coffee-shops-in-austin",
                "snippet": "Explore the top coffee spots in Austin with our curated list."
            }
        ],
        "local_map": {
            "image": "https://maps.google.com/map_image.png",
            "location": "Austin, Texas"
        },
        "local_results": [
            {
                "name": "Houndstooth Coffee",
                "address": "401 Congress Ave",
                "rating": 4.6
            },
            {
                "name": "Starbucks",
                "address": "600 Congress Ave",
                "rating": 4.3
            }
        ],
        "related_questions": [
            "Is it healthy to drink coffee every day?",
            "What coffee does to your body?",
            "Is coffee good for you or bad for you?"
        ],
        "knowledge_graph": {
            "title": "Coffee",
            "description": "A brewed drink prepared from roasted coffee beans...",
            "nutrition_facts": {
                "calories": 1,
                "total_fat": "0g",
                "sodium": "5mg",
                "caffeine": "95mg"
            }
        },
        "recipes_results": [
            {
                "name": "Bulletproof Coffee Recipe",
                "link": "https://example.com/bulletproof-coffee",
                "rating": 4.5,
                "prep_time": "5 mins"
            },
            {
                "name": "Whipped Coffee",
                "link": "https://example.com/whipped-coffee",
                "rating": 4.8,
                "prep_time": "10 mins"
            }
        ],
        "discover_more_places": [
            {
                "name": "Austin Java",
                "image": "https://example.com/austin-java-image.jpg"
            },
            {
                "name": "Coffee Bar",
                "image": "https://example.com/coffee-bar-image.jpg"
            }
        ],
        "related_searches": [
            "coffee brands",
            "types of coffee",
            "coffee maker",
            "coffee recipe"
        ],
        "pagination": {
            "current_page": 1,
            "total_pages": 10,
            "next_page_link": "https://example.com/search?page=2"
        },
        "search_parameters": {
            "location_used": "Austin, Texas",
            "query": "Coffee"
        }
    }


Health Check
------------

The agent includes a ``health_check`` method to validate the API's operational status. It performs a test request to SerpAPI and checks the ``search_metadata.status`` field.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "API is operational."
    }

Testing
-------

To test the agent, use the test suite provided in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/google_search/tests

Contributing
------------

Contributions are welcome to improve the functionality of this agent. Follow these steps:

1. Fork the repository.
2. Create a new branch for your changes.
3. Submit a pull request with a detailed description of your changes.

**Best practices for contributions:**

- Ensure adherence to PEP 8 coding standards.
- Provide detailed docstrings and comments for new functionality.
- Write appropriate unit tests for added or modified methods.

License
-------

This agent is distributed under the MIT License. Refer to the LICENSE file for more information.
