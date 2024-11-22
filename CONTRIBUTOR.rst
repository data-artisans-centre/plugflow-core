Contributing to PlugFlow
========================

Thank you for your interest in contributing to **PlugFlow**! Contributions are what make this project an amazing tool for modular plugin-based development. Whether you are fixing bugs, proposing new features, or enhancing documentation, we welcome your input and effort.

This document provides guidelines for contributing to the project, ensuring consistency and ease of collaboration.

How Can You Contribute?
------------------------

1. **Reporting Bugs**: If you encounter any bugs, please file an issue with detailed reproduction steps.
2. **Feature Requests**: Propose new features or enhancements by creating a feature request issue.
3. **Improving Documentation**: Help us improve the project documentation.
4. **Developing Plugins**: Create and contribute new plugins to extend PlugFlow's functionality.
5. **Fixing Bugs**: Submit fixes for any open issues or bugs.
6. **Writing Tests**: Add or improve test coverage for the project or specific plugins.

Getting Started
---------------

### 1. Fork the Repository

Fork the repository to your own GitHub account:

.. code-block:: bash

    git clone https://github.com/<your-username>/PlugFlow.git
    cd PlugFlow

### 2. Set Up Your Environment

Create a virtual environment to work on the project:

.. code-block:: bash

    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate

Install the required dependencies:

.. code-block:: bash

    pip install -r requirements.txt

### 3. Run Tests Locally

Before making any changes, ensure all existing tests pass:

.. code-block:: bash

    pytest

Contributing Workflow
----------------------

1. **Create a Branch**: Create a branch for your changes:

   .. code-block:: bash

       git checkout -b feature/my-feature

2. **Make Your Changes**: Edit the necessary files, write code, and add tests.

3. **Run Tests**: Verify that all tests pass and add tests for new functionality:

   .. code-block:: bash

       pytest

4. **Commit Changes**: Commit your changes with a descriptive commit message:

   .. code-block:: bash

       git add .
       git commit -m "Add feature: my-feature"

5. **Push Changes**: Push your branch to your forked repository:

   .. code-block:: bash

       git push origin feature/my-feature

6. **Create a Pull Request**: Submit a pull request to the main repository and include:
   - A description of your changes.
   - The issue number (if applicable).
   - Any necessary screenshots or references.

Code Style and Standards
------------------------

Follow these guidelines to ensure consistency:

1. **PEP 8 Compliance**: All Python code must comply with the PEP 8 style guide.
2. **Type Annotations**: Use type hints in function definitions and method signatures.
3. **Docstrings**: Write detailed docstrings for all classes and methods using Google or NumPy style.
4. **Testing**: Ensure all features are covered by unit tests.

To check code style, run:

.. code-block:: bash

    pip install flake8
    flake8

Branch Naming Convention
------------------------

Use the following naming conventions for branches:

- **Feature**: `feature/<feature-name>`
- **Bug Fix**: `fix/<bug-name>`
- **Documentation**: `docs/<documentation-name>`

Testing Guidelines
------------------

Write unit tests for all new features or bug fixes. Place tests in the appropriate `tests/` directory.

Run tests locally before submitting a pull request:

.. code-block:: bash

    pytest

Writing Plugin Tests
--------------------

Each plugin must include a `tests` directory with unit tests. The tests should validate:

1. **Execute Logic**: Ensure the `execute` method behaves as expected.
2. **Health Check**: Test the `health_check` method for operational status.
3. **Error Handling**: Validate that the plugin handles invalid inputs gracefully.

Example Test:

.. code-block:: python

    def test_execute_success(plugin_instance):
        video_url = "https://www.youtube.com/watch?v=valid123"
        response = plugin_instance.execute(video_url, max_comments=1)
        assert any(comment["author"] == "TestUser" for comment in response)

Community Guidelines
--------------------

- Be respectful and inclusive to all contributors.
- Ensure discussions remain constructive and professional.
- Provide meaningful feedback when reviewing pull requests.

Issues and Bug Reports
-----------------------

When submitting an issue or bug report, include:

1. A clear and descriptive title.
2. Detailed steps to reproduce the issue.
3. The expected behavior and observed behavior.
4. Any relevant logs or screenshots.

License
-------

By contributing to PlugFlow, you agree that your contributions will be licensed under the project's **MIT License**.

Thank You
---------

We appreciate your contributions to PlugFlow. Together, we can make this project even better!

