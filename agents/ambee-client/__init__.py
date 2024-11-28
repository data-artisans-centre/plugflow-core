import requests
from core.log import logger
from core.base import AgentBase


class AmbeeClient(AgentBase):

    def execute(self, endpoint, api_key, service, latitude, longitude ):
        try:

            headers = {
                'x-api-key': api_key,
                'Content-type': "application/json"
            }

            result = requests.get(f"https://{endpoint}/{service}/latest/by-lat-lng?lat={latitude}&lng={longitude}", headers=headers)
            
            print(result.json())
            return result.json()

        except Exception as e:
            logger.error(f"Something went wrong with AmbeeClient {e}")
            return None

    def health(self):
        pass
