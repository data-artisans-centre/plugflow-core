import pytest
import json
import os
from agents.sherlock_module import SherlockAgent, SitesInformation, QueryResult, QueryStatus


@pytest.fixture
def sample_sites_data(tmp_path):
    """Create a temporary JSON file with sample site data."""
    sample_data = {
        "GitHub": {
            "url": "https://github.com/{username}",
            "pattern": r"^[a-zA-Z0-9-]+$",
            "active": True
        },
        "Twitter": {
            "url": "https://twitter.com/{username}",
            "pattern": r"^[a-zA-Z0-9_]+$",
            "active": True
        }
    }
    data_path = tmp_path / "sites.json"
    with open(data_path, 'w') as f:
        json.dump(sample_data, f)
    return str(data_path)


@pytest.fixture
def sherlock_agent():
    """Fixture to create a SherlockAgent instance."""
    return SherlockAgent()


def test_sites_information_initialization(sample_sites_data):
    """Test initialization of SitesInformation with sample data."""
    sites_info = SitesInformation(sample_sites_data)
    assert len(sites_info.sites) == 2
    assert "GitHub" in sites_info.sites
    assert "Twitter" in sites_info.sites
    assert len(sites_info) == 2


def test_sites_information_empty_initialization():
    """Test SitesInformation initialization without data."""
    sites_info = SitesInformation()
    assert len(sites_info.sites) == 0
    assert len(sites_info) == 0


def test_sherlock_agent_execute(sherlock_agent, sample_sites_data):
    """Test successful execution of SherlockAgent."""
    username = "testuser123"
    results = sherlock_agent.execute(username, sample_sites_data)
    
    assert "username" in results
    assert results["username"] == username
    assert "total_sites" in results
    assert results["total_sites"] > 0
    assert "results" in results


def test_sherlock_agent_health_check(sherlock_agent, sample_sites_data):
    """Test health check functionality."""
    # Ensure sites data is loaded
    sherlock_agent.execute("testuser", sample_sites_data)
    
    health_status = sherlock_agent.health_check()
    assert health_status["status"] == "healthy"
    assert "Service is operational" in health_status["message"]


def test_sherlock_agent_health_check_no_sites():
    """Test health check with no sites data."""
    agent = SherlockAgent()
    health_status = agent.health_check()
    assert health_status["status"] == "unhealthy"
    assert "No site data found" in health_status["message"]


def test_invalid_sites_data_file(sherlock_agent):
    """Test handling of invalid sites data file."""
    with pytest.raises(ValueError, match="Failed to load sites data"):
        sherlock_agent.execute("testuser", "/path/to/nonexistent/file.json")


def test_query_result_creation():
    """Test creation of QueryResult."""
    result = QueryResult(
        site_name="GitHub", 
        status=QueryStatus.CLAIMED, 
        url="https://github.com/testuser"
    )
    assert result.site_name == "GitHub"
    assert result.status == QueryStatus.CLAIMED
    assert result.url == "https://github.com/testuser"


def test_query_notify_print(capsys):
    """Test QueryNotifyPrint output."""
    from agents.sherlock_module import QueryNotifyPrint
    
    notify = QueryNotifyPrint()
    
    # Test claimed profile
    claimed_result = QueryResult(
        site_name="GitHub", 
        status=QueryStatus.CLAIMED, 
        url="https://github.com/testuser"
    )
    notify.notify(claimed_result)
    captured = capsys.readouterr()
    assert "[+] GitHub: Profile found" in captured.out

    # Test available profile
    available_result = QueryResult(
        site_name="Twitter", 
        status=QueryStatus.AVAILABLE
    )
    notify.notify(available_result)
    captured = capsys.readouterr()
    assert "[-] Twitter: Profile not found" in captured.out