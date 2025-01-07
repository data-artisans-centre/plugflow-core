Profanity Checker Plugin
========================

The **Profanity Checker Plugin** is designed to detect bad words, swear words, and profanity in a given text. It allows you to censor detected words and provides useful information about the profane words in the input content.
The documentation is given here : https://apilayer.com/marketplace/bad_words-api

- 
Features
--------

- Detects bad words, profanity, and swear words in any given text.
- Censors detected words using a specified character.
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

- ``text`` (str, required): The text to check for profanity.
- ``censor_character`` (str, optional): The character used to censor bad words (default: `*`).
- ``api_key`` (str, required): Your API key to access the Bad Words API.

Example Usage
-------------

To execute the plugin, use the PlugFlow CLI. You can either pass the API key as a parameter or set it as an environment variable.

Example with API key as a parameter:

.. code-block:: bash

    python main.py execute profanity_checker --params '{"text": "This is a shitty sentence", "censor_character": "*", "api_key": "YOUR_API_KEY"}'


Output
------

The plugin returns a JSON object containing the following fields:

- ``bad_words_list``: A list of detected bad words with their position and length in the text.
- ``bad_words_total``: The total number of bad words detected.
- ``censored_content``: The content with bad words replaced by the censor character.
- ``content``: The original content.

Example:

.. code-block:: json

    {
        "bad_words_list": [
            {
                "deviations": 0,
                "end": 16,
                "info": 2,
                "original": "shitty",
                "replacedLen": 6,
                "start": 10,
                "word": "shitty"
            }
        ],
        "bad_words_total": 1,
        "censored_content": "this is a ****** sentence",
        "content": "this is a shitty sentence"
    }

Testing
-------

To test the plugin, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/profanity_checker/tests

Health Check
------------

The plugin includes a ``health_check`` method to verify its operational status. The method attempts to check the status of the profanity checking service and returns a status message.

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
