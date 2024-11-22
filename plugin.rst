PlugFlow Plugin Development Guide
=================================

This guide provides a step-by-step walkthrough for creating and integrating a plugin into the **PlugFlow** framework. Plugins in PlugFlow are modular, self-contained components that follow a standardized interface for execution and health monitoring.

Contents
--------

1. Plugin Structure
2. Creating a New Plugin
3. Plugin Files
   - ``__init__.py``
   - ``manifest.json``
   - ``README.md``
4. Testing the Plugin
5. Example Plugin: YouTube Review

Plugin Structure
----------------

Every plugin must follow a specific structure to ensure compatibility with the framework.

.. code-block:: text

    plugins/
    ├── <plugin_name>/
    │   ├── __init__.py       # Main plugin logic
    │   ├── manifest.json     # Plugin metadata
    │   ├── README.md         # Plugin documentation
    │   ├── tests/            # Plugin-specific tests
    │       ├── __init__.py   # Test initialization
    │       └── test_<plugin_name>.py  # Unit tests for the plugin

Creating a New Plugin
---------------------

Step 1: Create the Plugin Directory
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Navigate to the ``plugins`` directory and create a new folder for your plugin.

.. code-block:: bash

    cd plugins
    mkdir <plugin_name>
    cd <plugin_name>

Step 2: Add Required Files
~~~~~~~~~~~~~~~~~~~~~~~~~~

Inside the plugin folder, create the following files:

- ``__init__.py``: Contains the main logic for the plugin.
- ``manifest.json``: Defines the plugin metadata.
- ``README.md``: Provides documentation for the plugin.

Plugin Files
------------

``__init__.py``
~~~~~~~~~~~~~~~

This file contains the main logic of the plugin. It must define a ``Plugin`` class that inherits from the ``PluginBase`` interface. The class must implement two methods:

- ``execute``: Executes the main plugin logic.
- ``health_check``: Checks the plugin's readiness or service availability.

Example: ``__init__.py``
~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    from core.base import PluginBase
    from youtube_comment_downloader import YoutubeCommentDownloader

    class Plugin(PluginBase):
        """YouTube Review Plugin"""

        def execute(self, video_url, max_comments=10):
            """
            Fetch comments from a YouTube video.

            Args:
                video_url (str): The URL of the YouTube video.
                max_comments (int): Maximum number of comments to fetch.

            Returns:
                list: A list of comments.
            """
            try:
                print(f"Fetching comments from video: {video_url}")
                downloader = YoutubeCommentDownloader()
                comments = downloader.get_comments_from_url(video_url)
                return [comment for _, comment in zip(range(max_comments), comments)]
            except Exception as e:
                print(f"An error occurred: {e}")
                raise e

        def health_check(self):
            """
            Check if the plugin is operational.

            Returns:
                dict: Health status of the plugin.
            """
            try:
                print("Performing health check...")
                downloader = YoutubeCommentDownloader()
                dummy_video_url = "https://www.youtube.com/watch?v=ScMzIvxBSi4"
                comments = downloader.get_comments_from_url(dummy_video_url)
                next(comments)
                return {"status": "healthy", "message": "Service is available"}
            except Exception as e:
                return {"status": "unhealthy", "message": str(e)}

``manifest.json``
~~~~~~~~~~~~~~~~~

The ``manifest.json`` file provides metadata about the plugin, including its name and entry point.

Example: ``manifest.json``
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: json

    {
        "name": "youtube-review",
        "entry_point": "__init__"
    }

``README.md``
~~~~~~~~~~~~~

Document the purpose and usage of the plugin.

Example: ``README.md``
~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: markdown

    # YouTube Review Plugin

    This plugin fetches comments from a YouTube video.

    ## Parameters

    - `video_url` (str): The URL of the YouTube video.
    - `max_comments` (int): The maximum number of comments to fetch.

    ## Example Usage

    ```bash
    python main.py execute youtube-review --params '{"video_url": "https://youtu.be/abc123", "max_comments": 10}'
    ```

Testing the Plugin
------------------

Test Directory Structure
~~~~~~~~~~~~~~~~~~~~~~~~

Each plugin must include a ``tests`` folder for its test cases:

.. code-block:: text

    plugins/
    ├── <plugin_name>/
    │   ├── tests/
    │       ├── __init__.py
    │       └── test_<plugin_name>.py

Writing Tests
~~~~~~~~~~~~~

1. Import the plugin class.
2. Use ``pytest`` for testing.
3. Mock dependencies for isolated tests.

Example: ``test_<plugin_name>.py``
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: python

    import pytest
    from plugins.youtube_review import Plugin

    class MockDownloader:
        """Mock class for YoutubeCommentDownloader"""
        def get_comments_from_url(self, url, sort_by=None):
            if "invalid" in url:
                raise ValueError("Invalid URL")
            return [{"author": "TestUser", "comment": "This is a test comment"}]

    @pytest.fixture
    def youtube_review_plugin(monkeypatch):
        """Fixture to initialize the youtube-review plugin with a mock downloader."""
        plugin = Plugin()
        monkeypatch.setattr("plugins.youtube_review.YoutubeCommentDownloader", MockDownloader)
        return plugin

    def test_execute_success(youtube_review_plugin):
        video_url = "https://www.youtube.com/watch?v=valid123"
        response = youtube_review_plugin.execute(video_url, max_comments=1)
        assert any(comment["author"] == "TestUser" for comment in response)

    def test_execute_invalid_url(youtube_review_plugin):
        video_url = "https://www.youtube.com/watch?v=invalid123"
        with pytest.raises(ValueError, match="Invalid URL"):
            youtube_review_plugin.execute(video_url, max_comments=1)

    def test_health_check_success(youtube_review_plugin):
        health = youtube_review_plugin.health_check()
        assert health["status"] == "healthy"

Running Tests
~~~~~~~~~~~~~

Run all tests for the plugin:

.. code-block:: bash

    pytest plugins/<plugin_name>/tests

Example Plugin: YouTube Review
------------------------------

Below is a complete example for a plugin named ``youtube-review`` that fetches YouTube video comments.

### Directory Structure

.. code-block:: text

    plugins/
    ├── youtube_review/
    │   ├── __init__.py
    │   ├── manifest.json
    │   ├── README.md
    │   ├── tests/
    │       ├── __init__.py
    │       └── test_youtube_review.py

This concludes the guide for creating and testing plugins in PlugFlow. Follow this structure to maintain consistency and scalability as your project grows!

