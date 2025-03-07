import json
import re


def clean_json_text(text: str):
    """
    Extracts and parses the JSON block from the given text.

    Args:
        text (str): The raw text containing the JSON block.

    Returns:
        dict: The parsed JSON as a Python dictionary, or None if parsing fails.
    """
    try:
        # Use a regular expression to find the JSON object (everything between the first '{' and the last '}')
        json_match = re.search(r'\{.*\}', text, re.DOTALL)
        if not json_match:
            raise ValueError("No JSON object found in the text.")
        json_str = json_match.group()

        # Parse the extracted JSON string
        data = json.loads(json_str)
        print("Cleaned & Parsed JSON:", data)
        return data
    except Exception as e:
        print("Error cleaning JSON text:", e)
        return None


# Example usage:
raw_text = '''json
{
  "Score": 4,
  "Category": "Crypto Airdrop",
  "Reasoning": "The tweet does not mention a startup or blockchain directly but refers to a token airdrop campaign involving $WOD tokens and BinanceWallet, which is related to cryptocurrency. The score of 4 is given because the context implies a blockchain-related event, but it lacks direct mention of a startup or the term 'blockchain', hence not qualifying for the higher scores associated with those keywords."
}
'''
