import requests
import os
from dotenv import load_dotenv

try:
    load_dotenv("/secrets/x-startup-secrets")
except Exception as e:
    print("❌ Failed to load .env secret:", e)

# Load environment variables from .env file


def fetch_twitter_data():
    """
    Fetch recent tweets based on the query parameters using Twitter API.

    Returns:
        dict: The JSON response from the Twitter API.
    """
    bearer_token = os.environ.get("BEARER_TOKEN")
    if not bearer_token:
        raise ValueError("Bearer token not found. Ensure it is set in the environment variables.")

    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        'query': '( (Grant Program) OR grant OR grants OR (Builder Grants) OR (grant round) OR Funding OR (received '
                 'grant) OR (content grant) )'
                 '(Announcing OR startup OR launch '
                 'OR '
                 'Launching OR #launch OR Base OR Circle OR Alliance OR Superteam OR Superteam OR SolanaFndn OR '
                 'Polygon OR Coinbase)'
                 '(-breaking -news -meme -is:retweet -is:quote)',
        'tweet.fields': 'author_id,created_at,article,public_metrics,note_tweet',
        'max_results': '100',
        'expansions': 'author_id,referenced_tweets.id,referenced_tweets.id.author_id'
    }

    def bearer_oauth(r):
        """
        Method required by bearer token authentication.
        """
        r.headers["Authorization"] = f"Bearer {bearer_token}"
        r.headers["User-Agent"] = "v2RecentSearchPython"
        return r

    def connect_to_endpoint(url, params):
        response = requests.get(url, auth=bearer_oauth, params=params)
        if response.status_code != 200:
            raise Exception(f"Error: {response.status_code}, {response.text}")
        return response.json()

    # Fetch the data
    return connect_to_endpoint(search_url, query_params)
