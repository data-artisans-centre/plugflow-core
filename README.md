
# PlugFlow

**PlugFlow** is a Python-based CLI framework designed to enable dynamic plugin execution. It allows developers to create modular, self-contained plugins with ease, ensuring scalability and extensibility for complex workflows.

---

## Features

- **Dynamic Plugin Discovery**: Automatically discover and load plugins from the `plugins` directory.
- **Standardized Plugin Interface**: Every plugin adheres to a predefined structure for consistency.
- **Health Monitoring**: Built-in health checks to ensure service availability for all plugins.
- **Extensibility**: Easily add new plugins without modifying the core CLI.
- **JSON Output**: Supports structured output for easy integration with other tools.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Installation](#installation)
3. [Creating a Plugin](#creating-a-plugin)
4. [Plugin Structure](#plugin-structure)
5. [Plugin Interface](#plugin-interface)
6. [Example Plugin: YouTube Review](#example-plugin-youtube-review)
7. [Commands](#commands)
8. [Testing and Debugging](#testing-and-debugging)
9. [Contributing](#contributing)

---

## Getting Started

### Prerequisites

- Python 3.7 or higher
- `pip` (Python package manager)

### Clone the Repository

```bash
git clone https://github.com/your-repo/PlugFlow.git
cd PlugFlow



### Install Dependencies

Install the global dependencies defined in `requirements.txt`:

    `pip install -r requirements.txt`

## Installation

PlugFlow is a framework; to use it, you can either:

1.  Clone the repository and customize it for your use case.
2.  Install it as a library and extend its functionality.

----------

## Creating a Plugin

Follow these steps to create a new plugin:

### Step 1: Create a Plugin Directory

Create a new folder inside the `plugins` directory with the plugin name, e.g., `my_plugin`:

bash

Copy code

`mkdir plugins/my_plugin` 

### Step 2: Add Plugin Files

Inside the new plugin folder, create the following files:

1.  `__init__.py`: The main entry point for the plugin.
2.  `manifest.json`: Metadata for the plugin.
3.  `README.md`: Documentation for the plugin.

### Step 3: Implement Plugin Code

Define your plugin logic in `__init__.py`. Ensure the plugin implements the `PluginBase` interface.

----------

## Plugin Structure

A plugin should follow this structure:


    `plugins/
    ├── my_plugin/
    │   ├── __init__.py     # Main plugin logic
    │   ├── manifest.json   # Plugin metadata
    │   ├── README.md       # Plugin documentation` 

### Example: `manifest.json`



`{
    "name": "my_plugin",
    "entry_point": "__init__"
}` 

----------

## Plugin Interface

All plugins must implement the `PluginBase` interface, which defines two methods:

### `execute`

The core method where the plugin logic resides.


    `def execute(self, **kwargs):
        """
        Execute the plugin logic.
    
        Args:
            kwargs: Arbitrary keyword arguments for plugin execution.
        """
        raise NotImplementedError("Each plugin must implement the 'execute' method")` 

### `health_check`

Checks the availability or readiness of the plugin.


    `def health_check(self):
        """
        Check the health of the plugin.
    
        Returns:
            dict: A dictionary containing the health status and message.
        """
        raise NotImplementedError("Each plugin must implement the 'health_check' method")` 
    

## Example Plugin: YouTube Review

Here’s an example of a plugin that fetches comments from a YouTube video:

### 1. `plugins/youtube_review/manifest.json`


    `{
        "name": "youtube-review",
        "entry_point": "__init__"
    }` 

### 2. `plugins/youtube_review/README.md`


    ``# YouTube Review Plugin

This plugin fetches comments from a YouTube video given its URL.

## Parameters

- `video_url` (str): The URL of the YouTube video.
- `max_comments` (int): The maximum number of comments to fetch.

## Example Usage`` 

python main.py execute youtube-review --params '{"video_url": "[https://youtu.be/abc123](https://youtu.be/abc123)", "max_comments": 10}'

Copy code

### 3. `plugins/youtube_review/__init__.py`



`from core.base import PluginBase
from youtube_comment_downloader import YoutubeCommentDownloader, SORT_BY_POPULAR
from itertools import islice
import json

class Plugin(PluginBase):
    """YouTube Review Plugin"""

    def execute(self, video_url, max_comments=10):
        """
        Fetch comments from a YouTube video and return as JSON.

        Args:
            video_url (str): The URL of the YouTube video.
            max_comments (int): Maximum number of comments to fetch.

        Returns:
            JSON: The comments data in JSON format.
        """
        downloader = YoutubeCommentDownloader()
        comments = downloader.get_comments_from_url(video_url, sort_by=SORT_BY_POPULAR)
        limited_comments = list(islice(comments, max_comments))
        return json.dumps(limited_comments, indent=4)

    def health_check(self):
        """Check if the plugin's dependencies and service are available."""
        try:
            downloader = YoutubeCommentDownloader()
            # Basic health check using a dummy video
            next(downloader.get_comments_from_url("https://www.youtube.com/watch?v=ScMzIvxBSi4"))
            return {"status": "healthy", "message": "Service is available"}
        except Exception as e:
            return {"status": "unhealthy", "message": str(e)}` 

----------

## Commands

### `health`

Check the health of all plugins:

    `python main.py health` 

**Output:**


    `youtube-review: {'status': 'healthy', 'message': 'Service is available'}` 

### `execute`

Run a plugin:

    `python main.py execute <plugin_name> --params '<json_params>'` 

**Example:**

    `python main.py execute youtube-review --params '{"video_url": "https://youtu.be/abc123", "max_comments": 10}'` 

----------

## Testing and Debugging

-   Test plugin functionality individually by invoking the `execute` method in isolation.
-   Use the `health` command to verify plugin readiness before execution.
-   Add logging to capture runtime information.

----------

## Contributing

1.  Fork the repository.
2.  Create a feature branch: `git checkout -b feature-name`.
3.  Commit your changes: `git commit -m "Add new feature"`.
4.  Push to the branch: `git push origin feature-name`.
5.  Submit a pull request.


