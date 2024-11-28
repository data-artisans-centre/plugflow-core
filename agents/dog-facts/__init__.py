from core.base import AgentBase
from core.log import logger


class DogFactsAgent(AgentBase):

    def execute(self, endpoint, service):
        try:
            result = self.http.get(f"{endpoint}/{service}")
            print(result.json())
            return result.json()

        except Exception as e:
            logger.error(f"Something went wrong DogFacts {e}")


    def health(self):
        pass
