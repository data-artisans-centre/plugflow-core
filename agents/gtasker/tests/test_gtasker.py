import os
import pytest
from unittest.mock import MagicMock, patch
from typing import Dict, Any
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

# Importing the agent from the specified path
from agents.gtasker import GoogleServicesAgent, GoogleServiceRequest, CalendarEventRequest, EmailRequest

@pytest.fixture
def mock_credentials():
    """Create a mock Google OAuth2 Credentials object."""
    mock_creds = MagicMock(spec=Credentials)
    mock_creds.valid = True
    return mock_creds

@pytest.fixture
def google_services_agent(mock_credentials, tmp_path):
    """
    Fixture to create a GoogleServicesAgent with mocked authentication.
    
    Args:
        mock_credentials: Mocked Google OAuth2 credentials
        tmp_path: Temporary directory for test files
    """
    # Create a mock credentials file
    credentials_path = tmp_path / "credentials.json"
    credentials_path.write_text('{\"installed\":{\"client_id\":\"test_id\"}}')
    
    # Mock configuration
    config = {
        'credentials_path': str(credentials_path),
        'token_path': str(tmp_path / "token.json"),
        'scopes': [
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/gmail.modify'
        ]
    }
    
    # Patch the authentication method
    with patch('agents.gtasker.GoogleServicesAgent._authenticate', return_value=mock_credentials):
        agent = GoogleServicesAgent(config)
        
        # Mock Google API services
        agent.calendar_service = MagicMock()
        agent.gmail_service = MagicMock()
        
        return agent

def test_google_services_agent_initialization(google_services_agent):
    """
    Test the initialization of GoogleServicesAgent.
    
    Args:
        google_services_agent: Fixture providing a mocked agent
    """
    assert google_services_agent is not None, "Agent initialization failed"
    assert hasattr(google_services_agent, 'calendar_service'), "Calendar service not initialized"
    assert hasattr(google_services_agent, 'gmail_service'), "Gmail service not initialized"

def test_create_calendar_event(google_services_agent):
    """
    Test creating a calendar event.
    
    Args:
        google_services_agent: Fixture providing a mocked agent
    """
    # Mock event creation response
    mock_event = {
        'id': 'test_event_123',
        'summary': 'Test Meeting'
    }
    google_services_agent.calendar_service.events().insert.return_value.execute.return_value = mock_event
    
    # Prepare event request
    event_request = {
        'operation_type': 'create_event',
        'summary': 'Test Meeting',
        'start_time': '2024-02-15T10:00:00',
        'end_time': '2024-02-15T11:00:00'
    }
    
    # Execute event creation
    result = google_services_agent.execute(event_request)
    
    assert result['status'] == 'success'
    assert result['event_id'] == 'test_event_123'

def test_send_email(google_services_agent):
    """
    Test sending an email.
    
    Args:
        google_services_agent: Fixture providing a mocked agent
    """
    # Mock email sending response
    mock_email_response = {'id': 'test_email_123'}
    google_services_agent.gmail_service.users().messages().send.return_value.execute.return_value = mock_email_response
    
    # Prepare email request
    email_request = {
        'operation_type': 'send_email',
        'to': 'test@example.com',
        'subject': 'Test Email',
        'body': 'This is a test email.'
    }
    
    # Execute email sending
    result = google_services_agent.execute(email_request)
    
    assert result['status'] == 'success'
    assert result['message_id'] == 'test_email_123'

def test_read_emails(google_services_agent):
    """
    Test reading emails.
    
    Args:
        google_services_agent: Fixture providing a mocked agent
    """
    # Mock email list and details
    mock_messages = {
        'messages': [
            {'id': 'email1'},
            {'id': 'email2'}
        ]
    }
    mock_message_details = {
        'payload': {
            'headers': [
                {'name': 'Subject', 'value': 'Test Subject'},
                {'name': 'From', 'value': 'sender@example.com'},
                {'name': 'Date', 'value': '2024-02-15'}
            ]
        }
    }
    
    google_services_agent.gmail_service.users().messages().list.return_value.execute.return_value = mock_messages
    google_services_agent.gmail_service.users().messages().get.return_value.execute.return_value = mock_message_details
    
    # Prepare read emails request
    read_request = {
        'operation_type': 'read_emails',
        'query': '',
        'max_results': 2
    }
    
    # Execute email reading
    results = google_services_agent.execute(read_request)
    
    assert len(results) == 2
    assert all('id' in email for email in results)
    assert all('subject' in email for email in results)

def test_health_check(google_services_agent):
    """
    Test health check functionality.
    
    Args:
        google_services_agent: Fixture providing a mocked agent
    """
    # Mock health check methods
    google_services_agent.calendar_service.calendarList().list.return_value.execute.return_value = {}
    google_services_agent.gmail_service.users().getProfile.return_value.execute.return_value = {}
    
    # Perform health check
    result = google_services_agent.health_check()
    
    assert result['status'] == 'healthy'
    assert 'operational' in result['message']

def test_invalid_operation_type(google_services_agent):
    """
    Test handling of invalid operation type.
    
    Args:
        google_services_agent: Fixture providing a mocked agent
    """
    with pytest.raises(ValueError, match="Unsupported operation type"):
        google_services_agent.execute({'operation_type': 'invalid_operation'})