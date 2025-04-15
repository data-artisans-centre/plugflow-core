import json
from itertools import islice
from core.base import AgentBase
from log import logger
import requests

class GitHubActivitiesAgent(AgentBase):
    """Agent to fetch recent activities of a public GitHub repository."""

    def execute(self, repo_url, max_events = 10):
        """
        Fetch recent events associated with a public repository on GitHub

        Args:
            repo_url (str): The url of github repository

        Returns:
            list: A list of dictionaries containing event data.

        Raises:
        ValueError: If:
            - The `repo_url` is invalid or improperly formatted.
            - The GitHub API response cannot be parsed.
            - The GitHub API returns data in an unexpected format.
            - Serialization of events to JSON fails.
        ConnectionError: If there is a network connectivity issue.
        Timeout: If the request to the GitHub API times out.
        InvalidURL: If the repository URL is malformed.
        HTTPError: If the GitHub API returns a non-2xx status code.
        JSONDecodeError: If the GitHub API response is not valid JSON.
        IndexError: If the URL does not contain enough components to extract the repository owner and name.
        Exception: For any other unexpected errors.
        """
        try:
            # Validate repo_url
            if not isinstance(repo_url, str) or "github.com" not in repo_url:
                raise ValueError("Invalid repository URL format.")
            
            split_url = str(repo_url).split("/")
            if len(split_url) < 5:
                raise ValueError("Repository URL must include owner and repo name.")
            repo_name = split_url[4]
            repo_owner = split_url[3]
            logger.info(f"Fetching events of repository: {repo_name}")
            url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/events"
            headers = {
                "Accept": "application/vnd.github+json"
            }
            response = requests.get(url, headers=headers)
            # check HTTP response status
            response.raise_for_status() 
            try:
                events = response.json()
            except json.JSONDecodeError as e:
                raise ValueError("Invalid JSON response from GitHub API.") from e
            
            if not isinstance(events, list):
                raise ValueError("Unexpected data format received from GitHub API.")
            limited_events = list(islice(events, max_events))
            # Convert the list of comments to a JSON-formatted string
            try:
                events_json = json.dumps(limited_events, indent=4)
            except TypeError as e:
                raise ValueError("Failed to serialize events to JSON.") from e
           
            return events_json
        
        except requests.exceptions.ConnectionError as e:
            logger.error("Connection error: Unable to reach GitHub API.")
            raise ValueError("Network issue. Please check your internet connection.") from e

        except requests.exceptions.Timeout as e:
            logger.error("Request timed out.")
            raise ValueError("GitHub API request timed out. Try again later.") from e

        except requests.exceptions.InvalidURL as e:
            logger.error(f"Invalid URL: {repo_url}")
            raise ValueError("The repository URL is malformed.") from e


        except IndexError as e:
            logger.error("URL splitting failed.")
            raise ValueError("Invalid repository URL format.") from e

        except ValueError as e:
            logger.error(f"Value error: {e}")
            raise


        except Exception as e:
            logger.error(f"An error occurred: {e}")
            raise ValueError("Failed to fetch events. Please check the repository URL and try again.") from e

    def health_check(self):
        """
        Check if the Github API is functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            logger.info("Performing health check...")
            
            # Test with a known valid repo URL
            
            
            logger.info(f"Fetching events of repository: plugflow-core")
            url = f"https://api.github.com/repos/data-artisans-centre/plugflow-core/events"
            headers = {
                "Accept": "application/vnd.github+json"
            }
            response = requests.get(url, headers=headers)
            response.raise_for_status()  
            events = response.json()
            if not isinstance(events, list) or not events:
                raise ValueError("Unexpected or empty response data.")
            logger.info("Health check passed.")
            return {"status": "healthy", "message": "Service is available"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
