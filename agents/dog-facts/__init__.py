import requests
from core.base import AgentBase
from log import logger 


class DogFactAgent(AgentBase):


    def health(self):
        pass 


    def execute(self):
        
        result = requests.get("https://dogapi.dog/api/v2/breeds")
        print(result.json())
        return result.json()


