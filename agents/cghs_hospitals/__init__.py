import requests
from pydantic import BaseModel, Field, field_validator,ConfigDict
from typing import Optional
from core.base import AgentBase
from log import logger


class CGHSHospitalsParams(BaseModel):
    api_key: str = Field(..., alias="api-key", description="API key for data.gov.in", min_length=1)
    format: str = Field(default="json", description="Response format (json/xml/csv)")
    city_name: Optional[str] = Field(default=None, validate_default=True)
    hospital_name: Optional[str] = Field(default=None)
    hospital_address: Optional[str] = Field(default=None)
    offset: int = Field(default=0, ge=0)
    limit: int = Field(default=10, ge=1, le=100)

    model_config = ConfigDict(
        populate_by_name=True
    )

    @field_validator("api_key")
    def api_key_must_not_be_blank(cls, v):
        if not v.strip():
            raise ValueError("Missing API Key. [Required format: api_key=YOUR_API_KEY]")
        return v
    
    @field_validator("city_name")
    @classmethod
    def validate_city_name(cls, v):
        if v and len(v.strip()) == 0:
            raise ValueError("City name cannot be empty.")
        return v


class CGHSHospitalsAgent(AgentBase):
    """Agent to fetch CGHS empanelled hospitals using the data.gov.in API."""

    API_URL = "https://api.data.gov.in/resource/de59e770-2333-4eaf-9088-a3643de040c8"

    def execute(self, **kwargs):
        """
        Fetch CGHS empanelled hospitals using validated input parameters.

        Args:
            kwargs: Dictionary of request parameters matching CGHSHospitalsParams

        Returns:
            dict: Status and list of hospitals or error message.
        """
        try:
            params = CGHSHospitalsParams(**kwargs)
            query_params = {
                "api-key": params.api_key,
                "format": params.format,
                "offset": params.offset,
                "limit": params.limit
            }

            if params.city_name:
                query_params["filters[cityName]"] = params.city_name
            if params.hospital_name:
                query_params["filters[hospitalName]"] = params.hospital_name
            if params.hospital_address:
                query_params["filters[hospitalAddress]"] = params.hospital_address

            logger.info(f"Fetching CGHS hospitals with parameters: {query_params}")
            response = requests.get(self.API_URL, params=query_params)

            if response.status_code == 200:
                data = response.json()
                logger.info(f"Retrieved {len(data.get('records', []))} hospital(s).")
                return {"status": "success", "data": data.get("records", [])}
            elif response.status_code == 401:
                logger.error("Unauthorized: Invalid API key.")
                raise ValueError("Unauthorized: Invalid API key.")
            elif response.status_code == 400:
                logger.error("Bad request: Invalid parameters or URL.")
                raise ValueError("Bad request: Invalid parameters or URL.")
            else:
                logger.error(f"API returned error: {response.status_code}, {response.text}")
                raise ValueError(f"API Error: {response.status_code} - {response.text}")

        except ValueError as ve:
            logger.error(f"Value error: {ve}")
            raise ve
        except Exception as e:
            logger.error(f"An unexpected error occurred: {e}")
            raise ValueError(f"An unexpected error occurred: {str(e)}") from e

    def health_check(self):
        """
        Check if the CGHS hospitals API is reachable and functional.

        Returns:
            dict: Health status of the plugin.
        """
        try:
            dummy_key = "579b464db66ec23bdd0000"  # sample/test key
            logger.info("Performing health check...")

            response = requests.get(
                self.API_URL,
                params={
                    "api-key": dummy_key,
                    "format": "json",
                    "limit": 1
                }
            )

            if response.status_code == 200:
                logger.info("Health check passed: API reachable.")
                return {"status": "healthy", "message": "API is reachable and responsive."}
            elif response.status_code == 401:
                logger.info("Health check passed (received expected unauthorized response).")
                return {"status": "healthy", "message": "API reachable (unauthorized without valid key)"}
            else:
                logger.warning("Unexpected health check response.")
                return {"status": "unhealthy", "message": f"Unexpected status: {response.status_code}"}

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return {"status": "unhealthy", "message": str(e)}
