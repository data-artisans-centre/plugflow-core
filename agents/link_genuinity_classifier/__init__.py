import json
import re
import requests
from typing import Dict, Any, Optional, List
from urllib.parse import urlparse
import ssl
import socket
import whois
from datetime import datetime
from pydantic import BaseModel, Field, HttpUrl, ValidationError, field_validator
from core.base import AgentBase
from log import logger

class LinkAnalysisConfig(BaseModel):
    """Configuration model for link analysis."""
    virustotal_api_key: Optional[str] = Field(default=None, description="VirusTotal API key")
    safebrowsing_api_key: Optional[str] = Field(default=None, description="Google Safe Browsing API key")
    links: List[str] = Field(..., description="List of URLs to analyze")
    max_links: int = Field(default=10, ge=1, le=50, description="Maximum number of links to analyze")

class LinkAnalysis(BaseModel):
    """Pydantic model to hold analysis results for a link."""
    url: HttpUrl = Field(..., description="The URL being analyzed")
    is_safe: bool = Field(..., description="Whether the link is considered safe")
    risk_score: float = Field(..., description="Overall risk score (0-100)")
    reasons: Optional[Dict[str, Any]] = Field(default_factory=dict, description="Detailed reasons for safety assessment")

    @field_validator("risk_score")
    @classmethod
    def validate_risk_score(cls, value):
        if not 0 <= value <= 100:
            raise ValueError("Risk score must be between 0 and 100.")
        return value

class LinkGenuinityClassifier(AgentBase):
    """Agent to classify link genuinity and safety."""

    def __init__(self):
        super().__init__()
        self.name = "link-genuinity-classifier"

    def check_ssl_certificate(self, url: str) -> dict:
        """Check the SSL certificate of a given URL."""
        try:
            parsed_url = urlparse(url)
            hostname = parsed_url.netloc  # Corrected method

            # Handle empty hostname
            if not hostname:
                raise ValueError("URL does not contain a valid hostname")

            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = True
            context.verify_mode = ssl.CERT_REQUIRED

            # Establish a secure connection
            with socket.create_connection((hostname, 443), timeout=10) as sock:
                with context.wrap_socket(sock, server_hostname=hostname) as secure_sock:
                    # Retrieve certificate information
                    cert = secure_sock.getpeercert()

                    # Parse issuer and subject safely
                    def parse_cert_field(field):
                        try:
                            return {k: v for item in cert.get(field, []) for k, v in [item]}
                        except Exception:
                            return {}

                    issuer = parse_cert_field("issuer")
                    subject = parse_cert_field("subject")

                    # Extract expiration date and calculate remaining days
                    expiration_str = cert.get("notAfter", None)
                    expiration_date = (
                        datetime.strptime(expiration_str, "%b %d %H:%M:%S %Y GMT")
                        if expiration_str
                        else None
                    )
                    remaining_days = (
                        (expiration_date - datetime.now()).days if expiration_date else None
                    )

                    return {
                        "valid": True,
                        "hostname": hostname,
                        "issuer": issuer,
                        "subject": subject,
                        "version": cert.get("version", "Unknown"),
                        "expiration": expiration_str,
                        "remaining_days": remaining_days,
                    }

        except Exception as e:
            logger.error(f"Unexpected error checking SSL for {url}: {e}")
            return {
                "valid": False,
                "error": "SSL check failed",
                "details": str(e),
            }
    def check_domain_age(self, url: str) -> Dict[str, Any]:
        """Check domain registration details."""
        try:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc

            domain_info = whois.whois(domain)
            creation_date = domain_info.creation_date
            if isinstance(creation_date, list):
                creation_date = creation_date[0]

            age = (datetime.now() - creation_date).days
            return {
                "valid": True,
                "creation_date": creation_date,
                "age_days": age,
            }
        except Exception as e:
            return {
                "valid": False,
                "error": str(e),
            }

    def analyze_link(self, url: str, virustotal_api_key: Optional[str] = None) -> LinkAnalysis:
        """Perform comprehensive link analysis."""
        reasons = {}
        risk_score = 0

        # SSL Certificate Check
        ssl_check = self.check_ssl_certificate(url)
        if not ssl_check['valid']:
            reasons['ssl'] = ssl_check.get('error', 'Invalid or expired SSL certificate')
            risk_score += 30

        # Domain Age Check
        domain_age = self.check_domain_age(url)
        if not domain_age['valid'] or domain_age.get('age_days', 0) < 30:
            reasons['domain_age'] = "Newly registered domain"
            risk_score += 20

        # Determine overall safety
        is_safe = risk_score < 50

        # Create and return LinkAnalysis
        return LinkAnalysis(
            url=url,
            is_safe=is_safe,
            risk_score=min(risk_score, 100),
            reasons=reasons,
        )

    def process_links(self, links: List[str], virustotal_api_key: Optional[str] = None) -> List[Dict]:
        """Process multiple links and return their analysis."""
        results = []
        for link in links:
            try:
                analysis = self.analyze_link(link, virustotal_api_key)
                results.append({
                    "url": str(analysis.url),
                    "is_safe": analysis.is_safe,
                    "risk_score": analysis.risk_score,
                    "reasons": analysis.reasons,
                })
            except Exception as e:
                logger.error(f"Error analyzing link {link}: {e}")
        return results

    def execute(self, params: Dict[str, Any]):
        """Main execution method for link analysis."""
        try:
            # Validate input parameters
            config = LinkAnalysisConfig(**params)

            logger.info(f"Analyzing {len(config.links)} links")

            # Limit number of links if exceeds max
            links = config.links[:config.max_links]

            # Process links with provided API key
            results = self.process_links(
                links,
                virustotal_api_key=config.virustotal_api_key,
            )

            # Log and return results
            results_json = json.dumps(results, indent=4)
            logger.info(f"Link analysis results: {results_json}")
            return results
        except ValidationError as ve:
            logger.error(f"Input validation error: {ve}")
            raise ValueError(f"Invalid input parameters: {ve}") from ve
        except Exception as e:
            logger.error(f"Error in link analysis: {e}")
            raise ValueError("Failed to analyze links.") from e

    def health_check(self):
        """Check if the link classifier is functional."""
        try:
            logger.info("Performing health check for LinkGenuinityClassifier...")
            test_url = "https://www.example.com"
            self.analyze_link(test_url)
            logger.info("Health check passed.")
            return {"status": "healthy", "message": "Service is operational"}
        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
