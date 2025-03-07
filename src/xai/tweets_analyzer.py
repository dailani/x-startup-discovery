import json

from src.xai.json_formating import clean_json_text
from xai_client import XAIClient


class TweetAnalyzer:
    def __init__(self, xai_client: XAIClient):
        self.xai_client = xai_client

    def analyze_tweet(self, tweet_text: str) -> (str, int):
        """
        Analyzes a tweet to determine a 1–2-word category and a relevance score.

        Scoring criteria:
         • +2 if the tweet mentions a startup.
         • +2 if it mentions blockchain.
         • +4 if it refers to a blockchain startup or company.

        Returns a JSON {Category, Score,Reasoning}.
        """
        prompt = f"""
        Analyze the following tweet text and determine a 1-2 word category summarizing the tweet's context (for example, "Blockchain Startup").
        Also, assign a relevance score (1-10) based on the following criteria:
          • +2 if the tweet mentions a startup.
          • +2 if it mentions blockchain.
          • +4 if it refers to a blockchain startup or company.
        You may adjust the score based on additional context from the tweet.
        Additionally, provide a brief explanation in 1–2 sentences detailing how you determined the score and category, referencing key elements from the tweet's content.
        Tweet text: "{tweet_text}"
        Respond in JSON format with keys "Score", "Category", and "Reasoning".
        """

        system_message = f""""
        You are an intelligent tweet analysis system. When provided with a tweet's text, analyze it and output a JSON object with exactly three keys: "Score", "Category", and "Reasoning".

            - "Score": An integer (1–10) representing the tweet's relevance.
            
            - "Category": A concise (1–2 word) label.
            
            - "Reasoning": text 1-2 sentences
            
            Please output only the JSON object without any additional text.
        """
        response_text = self.xai_client.ask(system_message, prompt, model="grok-2-latest")

        try:
            # clean the XAI response into proper JSON
            result = clean_json_text(response_text)

            print(f"Response: {result}")

            # extract the category, score, and reasoning from the JSON
            category = result.get("Category", "Unknown")
            score = result.get("Score", 0)
            reasoning = result.get("Reasoning", "N/A")
        except Exception as e:
            print(f"Error parsing response: {e}")
            # Fallback simple analysis: keyword matching
            category = "General"
            score = 0
            reasoning = "Fallback analysis based on keyword matching."
            tweet_lower = tweet_text.lower()
            if "startup" in tweet_lower:
                score += 2
            if "blockchain" in tweet_lower:
                score += 2
            if "blockchain" in tweet_lower and ("startup" in tweet_lower or "company" in tweet_lower):
                score += 4

        return category, score, reasoning
