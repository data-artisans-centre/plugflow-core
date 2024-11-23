Testing Guidelines for PlugFlow
===============================

This document provides detailed guidelines for writing and running tests for the PlugFlow project. Proper testing ensures the framework is reliable, scalable, and extensible.

Overview
--------

The testing framework for PlugFlow is built using `pytest`. Each agent must include its own dedicated tests, and global tests are provided for core components like discovery and execution.

Testing Scope
-------------

The following components should be thoroughly tested:

1. **Agent Logic**:
   - Each agent must implement unit tests for its `execute` and `health_check` methods.
   - Mock external dependencies (e.g., APIs) to simulate various scenarios.

2. **Core Framework**:
   - Test the discovery process to ensure agents are dynamically loaded correctly.
   - Validate that agents adhere to the `AgentBase` interface.

3. **Integration**:
   - Test workflows involving multiple agents to ensure proper execution order and parameter passing.

Directory Structure
-------------------

The `tests/` directory contains global tests, while each agent has its own test directory.

.. code-block:: text

    plugflow-core/
    ├── agents/
    │   ├── youtube_review/
    │   │   ├── tests/
    │   │   │   ├── __init__.py
    │   │   │   └── test_youtube_review.py
    ├── core/
    │   ├── tests/
    │   │   ├── __init__.py
    │   │   └── test_discovery.py
    ├── tests/
    │   ├── __init__.py
    │   ├── test_workflows.py  # Integration tests

Writing Tests
-------------

### Unit Tests for Agents

Each agent must include unit tests under its `tests/` directory.

#### Example: `test_youtube_review.py`

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

### Core Tests

Core tests validate the framework's core components, such as agent discovery and execution.

#### Example: `test_discovery.py`

.. code-block:: python

    import pytest
    from core.discovery import discover_agents

    def test_discover_agents():
        agents = discover_agents()
        assert "youtube-review" in agents
        assert callable(agents["youtube-review"])

### Integration Tests

Integration tests validate workflows involving multiple agents.

#### Example: `test_workflows.py`

.. code-block:: python

    import pytest
    from core.discovery import discover_agents
    from core.execution import execute_agent_flow

    def test_workflow_execution():
        agents = discover_agents()
        flow = ["youtube-review"]
        params = '{"video_url": "https://www.youtube.com/watch?v=abc123", "max_comments": 10}'
        results = execute_agent_flow(flow, agents, params)
        assert "youtube-review" in results

Running Tests
-------------

To run all tests:

.. code-block:: bash

    pytest

To run tests for a specific agent:

.. code-block:: bash

    pytest agents/<agent_name>/tests

To run a specific test file:

.. code-block:: bash

    pytest agents/<agent_name>/tests/test_<agent_name>.py

To run a specific test function:

.. code-block:: bash

    pytest -k "<test_function_name>"

Test Conditions
---------------

### 1. Agent Testing Conditions

**Execute Method**:
- Valid inputs should return expected results.
- Invalid inputs should raise appropriate exceptions.
- Edge cases (e.g., empty parameters, malformed URLs) should be handled gracefully.

**Health Check Method**:
- Should return `"healthy"` when the service is available.
- Should return `"unhealthy"` with a detailed error message when the service is unavailable.

### 2. Discovery Testing Conditions

- Agents with valid `manifest.json` files should be discovered.
- Agents with missing or invalid `manifest.json` files should be skipped gracefully.
- Discovered agents should implement the `AgentBase` interface.

### 3. Integration Testing Conditions

- Workflows involving multiple agents should execute in the correct order.
- Parameters should be passed correctly to each agent.
- Errors in one agent should not affect the execution of other agents.

### 4. Code Coverage

Ensure at least 90% code coverage by including tests for:
- All branches and edge cases in methods.
- Exception handling scenarios.

Best Practices
--------------

- **Mocking**: Mock all external dependencies (e.g., APIs, databases) to ensure isolated and repeatable tests.
- **Fixtures**: Use `pytest` fixtures to set up reusable test data and environments.
- **Assertions**: Write clear and specific assertions to validate test outcomes.
- **Descriptive Names**: Use descriptive names for test functions (e.g., `test_execute_invalid_url`).
- **Documentation**: Document the purpose and expected behavior of each test.

Continuous Integration
----------------------

The repository is integrated with GitHub Actions to automatically run tests on every push or pull request. Ensure all tests pass locally before committing your changes.

To check the CI status, visit the GitHub Actions page: https://github.com/data-artisans-centre/plugflow-core/actions

Conclusion
----------

By following these guidelines, you can ensure the reliability and robustness of the PlugFlow framework. Always write tests for new features and bugfixes, and keep existing tests up-to-date.

