import json
from abc import ABC, abstractmethod
from typing import Optional, Dict
from dataclasses import dataclass
from core.base import AgentBase
from log import logger

# Metadata for the package
__version__ = "1.0.0"
__longname__ = "Sherlock Username Analysis Module"
__shortname__ = "Sherlock"
__forge_api_latest_release__ = "https://api.github.com/repos/sherlock-project/sherlock/releases/latest"

@dataclass
class SiteInformation:
    """Data structure to hold information about a single site."""
    name: str
    url: str
    username_pattern: str
    active: bool = True


class SitesInformation:
    """Class to manage information about all supported sites."""
    
    def __init__(self, data_file_path: Optional[str] = None):
        """
        Initialize sites information, optionally loading from a file.

        Args:
            data_file_path (str, optional): Path to JSON file with site data.
        """
        self.sites = {}
        if data_file_path:
            self.load_sites(data_file_path)

    def load_sites(self, data_file_path: str):
        """
        Load site information from a JSON file.

        Args:
            data_file_path (str): Path to the JSON file.

        Raises:
            ValueError: If file cannot be loaded or has invalid format.
        """
        try:
            with open(data_file_path, 'r') as f:
                data = json.load(f)
                for site_name, site_data in data.items():
                    self.sites[site_name] = SiteInformation(
                        name=site_name,
                        url=site_data['url'],
                        username_pattern=site_data['pattern'],
                        active=site_data.get('active', True)
                    )
        except Exception as e:
            logger.error(f"Failed to load sites data: {e}")
            raise ValueError(f"Failed to load sites data from {data_file_path}") from e

    def __len__(self) -> int:
        """Return the number of active sites."""
        return len([site for site in self.sites.values() if site.active])


class QueryStatus:
    """Enumeration of possible query statuses."""
    CLAIMED = "claimed"
    AVAILABLE = "available"
    UNKNOWN = "unknown"
    ERROR = "error"


@dataclass
class QueryResult:
    """Data structure to hold results of a username query."""
    site_name: str
    status: str
    url: Optional[str] = None
    error_message: Optional[str] = None


class QueryNotify:
    """Base class for query notification handling."""
    
    def notify(self, result: QueryResult):
        """
        Handle notification of a query result.

        Args:
            result (QueryResult): The result to notify about.
        """
        pass


class QueryNotifyPrint(QueryNotify):
    """Implementation of QueryNotify that prints to console."""
    
    def notify(self, result: QueryResult):
        """
        Print query results to console.

        Args:
            result (QueryResult): The result to print.
        """
        if result.status == QueryStatus.CLAIMED:
            print(f"[+] {result.site_name}: Profile found - {result.url}")
        elif result.status == QueryStatus.AVAILABLE:
            print(f"[-] {result.site_name}: Profile not found")
        elif result.status == QueryStatus.ERROR:
            print(f"[!] {result.site_name}: Error - {result.error_message}")


class SherlockAgent(AgentBase):
    """Agent for performing Sherlock username searches."""
    
    def __init__(self):
        super().__init__()
        self.name = "sherlock-username-analyzer"
        self.sites_info = None

    def execute(self, username: str, sites_data_path: Optional[str] = None) -> Dict:
        """
        Search for username across various sites.

        Args:
            username (str): Username to search for.
            sites_data_path (str, optional): Path to sites data JSON file.

        Returns:
            dict: Analysis results for the username across different sites.

        Raises:
            ValueError: If an error occurs during analysis.
        """
        try:
            logger.info(f"Analyzing username: {username}")
            
            # Initialize sites information if not already done
            if not self.sites_info:
                self.sites_info = SitesInformation(sites_data_path)
            
            # For this example, we'll return a sample result
            # Replace with actual site checking logic
            results = {
                "username": username,
                "total_sites": len(self.sites_info),
                "results": []
            }
            
            # Log results
            results_json = json.dumps(results, indent=4)
            logger.info(f"Analysis results: {results_json}")
            return results
            
        except Exception as e:
            logger.error(f"Error analyzing username: {e}")
            raise ValueError("Failed to analyze username.") from e

    def health_check(self) -> Dict:
        """
        Check if the analyzer is functional.

        Returns:
            dict: Health status of the agent.
        """
        try:
            logger.info("Performing health check for SherlockAgent...")
            self.sites_info = SitesInformation()
            if len(self.sites_info) > 0:
                logger.info("Health check passed.")
                return {"status": "healthy", "message": "Service is operational"}
            else:
                return {"status": "unhealthy", "message": "No site data found"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}