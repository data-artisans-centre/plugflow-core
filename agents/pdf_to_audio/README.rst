PDF to Audio Agent
=================

The **PDF to Audio Agent** is designed to convert PDF documents to speech using text extraction and text-to-speech capabilities. It processes PDF files, extracts their textual content, and converts it to spoken audio output.

Features
--------

- Extract text from PDF documents
- Convert text to speech with configurable voice settings
- Direct audio playback
- Health check functionality
- Integration with the PlugFlow framework

Installation
------------

Ensure that the required dependencies are installed from `requirements.txt`:

.. code-block:: text

    pypdf
    pyttsx3

Install the dependencies using pip:

.. code-block:: bash

    pip install pypdf pyttsx3

Parameters
----------

The agent accepts the following parameters:

- ``pdf_path`` (str): The file path to the PDF document to be converted to audio.

Example Usage
-------------

To execute the agent, use the PlugFlow CLI:

.. code-block:: vscode terminal

    python main.py execute pdf_to_audio --params '{\"pdf_path\": \"path/to/document.pdf\"}'

.. code-block:: bash

    python main.py execute pdf_to_audio --params "{\"pdf_path\": \"path/to/document.pdf\"}"

Output
------

The agent returns a JSON object containing the execution results. The output includes the following fields:

- ``status``: The execution status ("success" or "error")
- ``message``: A description of the execution result
- ``full_text``: The extracted text from the PDF (on successful execution)

Example:

.. code-block:: json

    {
        "status": "success",
        "message": "PDF text has been converted to speech and played",
        "full_text": "Content of the PDF document..."
    }

Testing
-------

To test the agent, use the provided test suite located in the ``tests`` directory.

Run all tests:

.. code-block:: bash

    pytest agents/pdf_to_audio/tests

Health Check
------------

The agent includes a ``health_check`` method to verify its operational status. The method attempts to perform a test audio playback and returns a status message.

Example health check output:

.. code-block:: json

    {
        "status": "healthy",
        "message": "PDF to audio conversion service is operational"
    }

Audio Configuration
------------------

The agent supports the following audio configuration options:

- Voice selection (default: female voice)
- Speech rate (default: 150)
- Volume level (default: 0.9)

These settings can be modified in the `play_audio` method of the agent.

Error Handling
-------------

The agent handles various error scenarios including:

- Missing PDF path
- Invalid PDF format
- File not found
- Text-to-speech engine errors

Each error scenario returns an appropriate error message in the response.

Contributing
------------

Contributions to improve or enhance the agent are welcome. Follow these steps:

1. Fork the repository
2. Create a new branch for your changes
3. Submit a pull request with a detailed description of your changes

Please ensure that all tests pass before submitting a pull request.

Requirements
-----------

- Python 3.6 or higher
- pypdf library
- pyttsx3 library
- Operating system with audio output capabilities

License
-------

This agent is distributed under the MIT License. See the LICENSE file for more information.

Notes
-----

1. The agent requires a working audio output device for speech playback
2. Large PDF files may take longer to process
3. Text extraction quality depends on the PDF document's format and structure

Support
-------

For issues, questions, or suggestions:

1. Open an issue in the repository
2. Check existing issues for similar problems
3. Provide example PDF files when reporting issues (if possible)
