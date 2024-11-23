Creating an Agent in PlugFlow
=============================

This guide walks you through the process of creating a new agent in PlugFlow, from directory structure to implementation and integration.

Step 1: Directory Structure
---------------------------
Each agent must have its own folder under the `agents` directory. The folder should contain:

.. code-block:: text

    agents/
    ├── <agent_name>/
    │   ├── __init__.py       # Main logic for the agent
    │   ├── manifest.json     # Metadata for the agent
    │   ├── README.md         # Documentation for the agent
    │   ├── tests/            # Test cases for the agent
    │       ├── __init__.py   # Test initialization
    │       └── test_<agent_name>.py  # Unit tests for the agent

Example for `youtube-review` agent:

.. code-block:: text

    agents/
    ├── youtube_review/
    │   ├── __init__.py
    │   ├── manifest.json
    │   ├── README.md
    │   ├── tests/
    │       ├── __init__.py
    │       └── test_youtube_review.py

Step 2: Implementing the Agent
------------------------------
Create the `__init__.py` file to implement the agent class. Every agent must inherit from the `AgentBase` class and implement the required methods: `execute` and `health_check`.

Example: `__init__.py` for `youtube-review` agent:

.. code-block:: python

    from core.base import AgentBase
    from youtube_comment_downloader import YoutubeCommentDownloader
    import logging

    logger = logging.getLogger(__name__)

    class YoutubeReviewAgent(AgentBase):
        """Agent to fetch YouTube comments."""

        def execute(self, video_url, max_comments=10):
            """
            Fetch comments from a YouTube video.

            Args:
                video_url (str): The URL of the YouTube video.
                max_comments (int): Maximum number of comments to fetch.

            Returns:
                list: A list of dictionaries containing comment data.
            """
            try:
                logger.info(f"Fetching comments from: {video_url}")
                downloader = YoutubeCommentDownloader()
                comments = downloader.get_comments_from_url(video_url)
                return list(comments)[:max_comments]
            except Exception as e:
                logger.error(f"Error fetching comments: {e}")
                raise ValueError("Failed to fetch comments.") from e

        def health_check(self):
            """
            Check the health of the agent.

            Returns:
                dict: Health status of the agent.
            """
            try:
                dummy_url = "https://www.youtube.com/watch?v=ScMzIvxBSi4"
                downloader = YoutubeCommentDownloader()
                next(downloader.get_comments_from_url(dummy_url))
                return {"status": "healthy", "message": "Agent is operational"}
            except Exception as e:
                logger.error(f"Health check failed: {e}")
                return {"status": "unhealthy", "message": str(e)}

Step 3: Define Metadata in `manifest.json`
------------------------------------------
Create a `manifest.json` file in the agent's directory to define its metadata.

Example `manifest.json` for `youtube-review`:

.. code-block:: json

    {
        "name": "youtube-review",
        "entry_point": "__init__",
        "class_name": "YoutubeReviewAgent"
    }

- **name**: The unique name of the agent.
- **entry_point**: The module path relative to the agent folder.
- **class_name**: The name of the main class in the agent module.

Step 4: Writing Tests
---------------------
Every agent must include unit tests in a `tests/` subdirectory. Use the `pytest` framework for writing and running tests.

Example test suite: `test_youtube_review.py`

.. code-block:: python

    import pytest
    from agents.youtube_review import YoutubeReviewAgent

    class MockDownloader:
        def get_comments_from_url(self, url, sort_by=None):
            if "invalid" in url:
                raise ValueError("Invalid URL")
            yield {"author": "TestUser", "comment": "This is a test comment"}

    @pytest.fixture
    def youtube_review_agent(monkeypatch):
        agent = YoutubeReviewAgent()
        monkeypatch.setattr("agents.youtube_review.YoutubeCommentDownloader", MockDownloader)
        return agent

    def test_execute_success(youtube_review_agent):
        video_url = "https://www.youtube.com/watch?v=valid123"
        response = youtube_review_agent.execute(video_url, max_comments=1)
        assert response[0]["author"] == "TestUser"

    def test_execute_invalid_url(youtube_review_agent):
        video_url = "https://www.youtube.com/watch?v=invalid123"
        with pytest.raises(ValueError):
            youtube_review_agent.execute(video_url)

    def test_health_check_success(youtube_review_agent):
        health = youtube_review_agent.health_check()
        assert health["status"] == "healthy"

    def test_health_check_failure(monkeypatch):
        def mock_get_comments(*args, **kwargs):
            raise Exception("Mock failure")
        monkeypatch.setattr("agents.youtube_review.YoutubeCommentDownloader.get_comments_from_url", mock_get_comments)
        agent = YoutubeReviewAgent()
        health = agent.health_check()
        assert health["status"] == "unhealthy"

Run the tests using:

.. code-block:: bash

    pytest agents/youtube_review/tests

Step 5: Integration with Discovery
-----------------------------------
Once the agent is created, it will be automatically discovered by the `discover_agents` function if the `manifest.json` is correctly defined.

Example discovery test script:

.. code-block:: python

    from core.discovery import discover_agents

    if __name__ == "__main__":
        agents = discover_agents()
        for name, cls in agents.items():
            print(f"Discovered agent: {name}, Class: {cls}")

Step 6: Adding Documentation
----------------------------
Add a `README.md` file in the agent's directory to document its purpose, usage, and configuration.

Example `README.md` for `youtube-review`:

.. code-block:: markdown

    # YouTube Review Agent

    The YouTube Review Agent fetches comments from YouTube videos.

    ## Usage

    Parameters:
    - `video_url`: The URL of the YouTube video.
    - `max_comments`: Maximum number of comments to fetch.

    ### Example

    ```bash
    python main.py execute youtube-review --params '{"video_url": "https://www.youtube.com/watch?v=abc123", "max_comments": 10}'
    ```

Conclusion
----------
By following these steps, you can create and integrate a new agent into the PlugFlow system. Ensure proper testing and documentation to maintain high-quality standards.

