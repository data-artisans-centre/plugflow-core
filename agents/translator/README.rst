Translator Agent
=================

The **Translator Agent** is designed to facilitate text translation between languages using a translation library from googletrans. It supports executing translations, health checks, and retrieving supported languages.

Features
--------

- Translate text between supported languages.
- Perform a health check to verify service availability.
- Retrieve a list of supported languages with their codes.
- Simple integration with the PlugFlow framework.

Installation
------------

Ensure that the required dependencies are installed. Add the following to your environment or `requirements.txt`:

.. code-block:: text

    googletrans

Install the dependencies using pip:

.. code-block:: bash

    pip install googletrans

Parameters
----------

The agent accepts the following parameters:

- ``text`` (str): The text to be translated.
- ``target_language`` (str): The language code to translate the text into.

Example Usage
-------------

To execute the agent, use the PlugFlow CLI:

.. code-block:: vscode terminal

    python main.py execute translator --params '{\"text\": \"Hello how are you\", \"target_language\": \"es\"}'

.. code-block:: bash

    python main.py execute translator --params "{\"text\": \"Hello how are you\", \"target_language\": \"es\"}"

Output
------

The agent returns the translation result as a JSON object. The output includes the following fields:

- ``original_text``: The input text provided for translation.
- ``translated_text``: The translated version of the input text.
- ``source_language``: The detected language of the input text.
- ``target_language``: The language code for the translated text.

Example:

.. code-block:: json

    {
        "original_text": "Hello",
        "translated_text": "Hola",
        "source_language": "en",
        "target_language": "es"
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/translator/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method attempts to perform a test translation and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "Translation service is operational"
    }

Supported Languages
-------------------

The agent supports translating text to and from the following languages:

- English (`en`)
- Spanish (`es`)
- French (`fr`)
- German (`de`)
- Chinese (`zh-cn`)
- Japanese (`ja`)
- Arabic (`ar`)
- Russian (`ru`)
- Portuguese (`pt`)
- Italian (`it`)

Example Output:

.. code-block:: json

    {
        "English": "en",
        "Spanish": "es",
        "French": "fr",
        "German": "de",
        "Chinese": "zh-cn",
        "Japanese": "ja",
        "Arabic": "ar",
        "Russian": "ru",
        "Portuguese": "pt",
        "Italian": "it"
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


python main.py execute translator --params '{\"text\": \"Hello how are you\", \"target_language\": \"es\"}'
