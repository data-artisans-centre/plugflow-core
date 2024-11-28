from core.base import AgentBase
from core.log import logger
from openai import OpenAI
import json

class ChatGPT(AgentBase):

    def __init__(self):
        self.api_key = None
        self.messages = []
        self.client = None 

    def execute(self, api_key:str, role:str, prompt:str):
        """
        ChatGPT Agent execute method takes the prompt and respond with the choice which
        was generated from OpenAI chat completion service

        params:
            api_key: Used for authentication purposes.
            role: Assistant, System, User
            prompt: For starting the conversation

        Return:
            prompt completition from the OpenAI Service
        """
        self.client = OpenAI(api_key=api_key)
        self.api_key = api_key

        # Get the roles and set the initial message in self.messages list
        self.messages.append({
            "role": 'system',
            "content": f"You are a helpful {role} who can answer my all questions"
        })

        # Now take the prompt and set the role type as user and append into self.messages 
        self.messages.append({
            "role": "user",
            "content": prompt
        })

        result = self.client.chat.completions.create(
            model="gpt-4o",
            messages=self.messages
        )

        # Use the self.messages to call the chat completions API.

        # Print the response and update the self.messages with response as well.
        print(json.dumps({'data': result.choices[0].message.content}))

    def health(self):
        pass

