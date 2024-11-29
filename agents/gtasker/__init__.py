from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field, ValidationError
from core.base import AgentBase
from log import logger

# Google API imports
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import base64
from email.mime.text import MIMEText


class GoogleServiceRequest(BaseModel):
    """Model for Google API service configuration."""
    credentials_path: str = Field(..., description="Path to Google API credentials file")
    scopes: List[str] = Field(
        default=[
            'https://www.googleapis.com/auth/calendar',
            'https://www.googleapis.com/auth/gmail.modify'
        ],
        description="OAuth2 scopes for Google API access"
    )
    token_path: Optional[str] = Field(None, description="Path to store OAuth token")


class CalendarEventRequest(BaseModel):
    """Model for calendar event creation/modification."""
    summary: str = Field(..., description="Event title")
    description: Optional[str] = None
    start_time: str = Field(..., description="Start time in ISO format")
    end_time: str = Field(..., description="End time in ISO format")
    attendees: Optional[List[str]] = None


class EmailRequest(BaseModel):
    """Model for email sending and reading."""
    to: str = Field(..., description="Recipient email address")
    subject: str = Field(..., description="Email subject")
    body: str = Field(..., description="Email body")
    attachments: Optional[List[str]] = None


class GoogleServicesAgent(AgentBase):
    """
    Agent to interact with Google Calendar and Gmail APIs.
    Handles authentication, event management, and email operations.
    """

    def __init__(self, service_config: Dict[str, Any]):
        """
        Initialize Google Services Agent with API configuration.

        Args:
            service_config (Dict[str, Any]): Configuration for Google API services
        """
        try:
            # Validate service configuration
            config = GoogleServiceRequest(**service_config)
            self.credentials = self._authenticate(config)
            
            # Initialize services
            self.calendar_service = build('calendar', 'v3', credentials=self.credentials)
            self.gmail_service = build('gmail', 'v1', credentials=self.credentials)
            
            logger.info("Google Services Agent initialized successfully.")
        except Exception as e:
            logger.error(f"Failed to initialize Google Services Agent: {e}")
            raise

    def _authenticate(self, config: GoogleServiceRequest) -> Credentials:
        """
        Authenticate and obtain OAuth2 credentials for Google APIs.

        Args:
            config (GoogleServiceRequest): Authentication configuration

        Returns:
            Credentials: Authenticated Google API credentials
        """
        creds = None
        token_path = config.token_path or os.path.join(os.path.dirname(__file__), 'token.json')

        if os.path.exists(token_path):
            creds = Credentials.from_authorized_user_file(token_path, config.scopes)

        # Refresh or re-authenticate if needed
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file(
                    config.credentials_path, config.scopes)
                creds = flow.run_local_server(port=0)

            # Save the credentials for next run
            with open(token_path, 'w') as token:
                token.write(creds.to_json())

        return creds

    def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Execute Google service operations based on request type.

        Args:
            request (Dict[str, Any]): Request parameters for Google service operation

        Returns:
            Dict[str, Any]: Operation results
        """
        try:
            operation_type = request.get('operation_type')

            if operation_type == 'create_event':
                return self.create_calendar_event(request)
            elif operation_type == 'delete_event':
                return self.delete_calendar_event(request)
            elif operation_type == 'send_email':
                return self.send_email(request)
            elif operation_type == 'read_emails':
                return self.read_emails(request)
            else:
                raise ValueError(f"Unsupported operation type: {operation_type}")

        except ValidationError as ve:
            logger.error(f"Validation error: {ve}")
            raise ValueError(f"Invalid input: {ve}") from ve
        except Exception as e:
            logger.error(f"Google Services operation failed: {e}")
            raise ValueError(f"Operation failed: {e}") from e

    def create_calendar_event(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create a new calendar event.

        Args:
            request (Dict[str, Any]): Event creation parameters

        Returns:
            Dict[str, Any]: Created event details
        """
        event_request = CalendarEventRequest(**request)
        event = {
            'summary': event_request.summary,
            'description': event_request.description,
            'start': {'dateTime': event_request.start_time},
            'end': {'dateTime': event_request.end_time},
        }

        if event_request.attendees:
            event['attendees'] = [{'email': email} for email in event_request.attendees]

        created_event = self.calendar_service.events().insert(
            calendarId='primary', body=event).execute()

        logger.info(f"Created calendar event: {created_event['id']}")
        return {
            'event_id': created_event['id'],
            'status': 'success',
            'message': 'Event created successfully'
        }

    def delete_calendar_event(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Delete a calendar event by event ID.

        Args:
            request (Dict[str, Any]): Event deletion parameters

        Returns:
            Dict[str, Any]: Deletion status
        """
        event_id = request.get('event_id')
        if not event_id:
            raise ValueError("Event ID is required for deletion")

        self.calendar_service.events().delete(
            calendarId='primary', eventId=event_id).execute()

        logger.info(f"Deleted calendar event: {event_id}")
        return {
            'event_id': event_id,
            'status': 'success',
            'message': 'Event deleted successfully'
        }

    def send_email(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """
        Send an email via Gmail API.

        Args:
            request (Dict[str, Any]): Email sending parameters

        Returns:
            Dict[str, Any]: Email sending status
        """
        email_request = EmailRequest(**request)
        
        message = MIMEText(email_request.body)
        message['to'] = email_request.to
        message['subject'] = email_request.subject
        
        raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
        
        sent_message = self.gmail_service.users().messages().send(
            userId='me', body={'raw': raw_message}).execute()

        logger.info(f"Email sent to {email_request.to}")
        return {
            'message_id': sent_message['id'],
            'status': 'success',
            'message': 'Email sent successfully'
        }

    def read_emails(self, request: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Read emails from Gmail using optional filters.

        Args:
            request (Dict[str, Any]): Email reading parameters

        Returns:
            List[Dict[str, Any]]: List of email details
        """
        query = request.get('query', '')
        max_results = request.get('max_results', 10)

        results = self.gmail_service.users().messages().list(
            userId='me', q=query, maxResults=max_results).execute()
        
        messages = results.get('messages', [])
        email_details = []

        for msg in messages:
            txt = self.gmail_service.users().messages().get(
                userId='me', id=msg['id'], format='metadata').execute()
            
            headers = {h['name']: h['value'] for h in txt['payload']['headers']}
            email_details.append({
                'id': msg['id'],
                'subject': headers.get('Subject', ''),
                'from': headers.get('From', ''),
                'date': headers.get('Date', '')
            })

        return email_details

    def health_check(self) -> Dict[str, str]:
        """
        Perform a health check for Google Services.

        Returns:
            Dict[str, str]: Health status of the agent.
        """
        try:
            logger.info("Performing health check for Google Services Agent...")
            
            # Check Calendar API
            self.calendar_service.calendarList().list().execute()
            
            # Check Gmail API
            self.gmail_service.users().getProfile(userId='me').execute()
            
            logger.info("Health check passed.")
            return {
                "status": "healthy", 
                "message": "Google Services are operational."
            }
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {
                "status": "unhealthy", 
                "message": f"Google Services health check failed: {e}"
            }