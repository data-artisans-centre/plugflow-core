Contributing to PlugFlow
========================

Thank you for your interest in contributing to **PlugFlow**! We welcome contributions from the community to improve this modular agent framework. This guide outlines the process for contributing to the project.

Getting Started
---------------

### 1. Fork the Repository

Fork the repository to your GitHub account:

.. code-block:: bash

    git clone https://github.com/<your-username>/plugflow-core.git
    cd plugflow-core

### 2. Set Up a Development Environment

Create a virtual environment and install dependencies:

.. code-block:: bash

    python -m venv env
    source env/bin/activate  # On Windows: env\Scripts\activate
    pip install -r requirements.txt

### 3. Run the Tests

Ensure that all tests pass before making changes:

.. code-block:: bash

    pytest

### 4. Set Up Pre-commit Hooks (Optional)

To ensure consistent code style, set up pre-commit hooks:

.. code-block:: bash

    pip install pre-commit
    pre-commit install

How to Contribute
-----------------

### Reporting Issues

If you find a bug or have a feature request, open an issue on GitHub:

- Provide a clear and concise description of the issue.
- Include steps to reproduce the problem, if applicable.
- Suggest potential solutions, if you have any.

### Making Changes

1. **Create a New Branch**:
   Create a branch for your feature or bugfix:

   .. code-block:: bash

       git checkout -b feature/<feature-name>
       # or
       git checkout -b bugfix/<bug-name>

2. **Write Clear and Modular Code**:
   Follow the repository's coding conventions:
   - Adhere to PEP 8 for Python code.
   - Include docstrings for all classes and methods.
   - Write clean and modular code.

3. **Write Tests**:
   Add or update tests in the `tests/` directory for your changes. Ensure that all agents have dedicated tests under their `tests/` subdirectory.

4. **Run Tests Locally**:
   Verify that all tests pass:

   .. code-block:: bash

       pytest

5. **Document Your Changes**:
   If your changes introduce a new feature or modify an existing one:
   - Update the agent's `README.md` if applicable.
   - Add or update documentation in the `docs/` directory.

6. **Commit Your Changes**:
   Write a clear and concise commit message:

   .. code-block:: bash

       git add .
       git commit -m "Add feature: <feature-name>"

### Submitting Changes

1. **Push Your Branch**:
   Push your changes to your forked repository:

   .. code-block:: bash

       git push origin feature/<feature-name>

2. **Open a Pull Request**:
   - Go to the original repository on GitHub.
   - Click on "New Pull Request."
   - Provide a detailed description of the changes and link to any related issues.

Review Process
--------------

Once you submit a pull request:

1. **Automated Checks**:
   - The CI pipeline will run tests and style checks on your branch.
   - Ensure that all checks pass before requesting a review.

2. **Code Review**:
   - A maintainer will review your changes and provide feedback.
   - Address any requested changes promptly.

3. **Merge**:
   - Once approved, your changes will be merged into the `main` branch.

Contribution Guidelines
-----------------------

- **Code Style**: Follow PEP 8 for Python code.
- **Modularity**: Ensure your code is modular and reusable.
- **Testing**: Add tests for all new features and bugfixes.
- **Documentation**: Update relevant documentation for your changes.

Adding a New Agent
------------------

To add a new agent, follow these steps:

1. Create a folder for the agent under `agents/`.
2. Add the required files: `__init__.py`, `manifest.json`, and `README.md`.
3. Implement the agent logic in `__init__.py`, adhering to the `AgentBase` interface.
4. Write tests for the agent in a `tests/` subdirectory.
5. Add the agent to the repository using the discovery process.

Refer to `docs/Creating_Agent.rst` for detailed instructions.

Community Standards
-------------------

- Be respectful and inclusive.
- Provide constructive feedback.
- Collaborate to build a better framework for everyone.

Contact
-------

For questions or discussions about contributing, open an issue on GitHub or join the discussion forum:

- GitHub Issues: https://github.com/data-artisans-centre/plugflow-core/issues
- GitHub Discussions: https://github.com/data-artisans-centre/plugflow-core/discussions

Thank you for your contributions! 🚀

