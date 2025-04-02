import os
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()


class XAIClient:
    def __init__(self, api_key=None, base_url="https://api.x.ai/v1"):
        # Use provided API key or retrieve from environment variable
        self.api_key = api_key or os.getenv("XAI_API_KEY")
        if not self.api_key:
            raise ValueError("XAI_API_KEY must be set either as a parameter or in the environment.")
        self.client = OpenAI(api_key=self.api_key, base_url=base_url)

    def ask(self, system_message, user_message, model="grok-2-latest"):
        """
        Send a chat completion request with a system and user message.
        Returns the assistant's response as a string.
        """
        completion = self.client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": system_message},
                {"role": "user", "content": user_message},
            ],
        )
        print(f"Completion choices: {completion.choices}")
        return completion.choices[0].message.content
