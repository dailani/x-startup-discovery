import requests
import os
from dotenv import load_dotenv
from prefect import  task  # Prefect flow and task decorators

# Load environment variables from .env file
load_dotenv()


@task
def fetch_twitter_data():
    """
    Fetch recent tweets based on the query parameters using Twitter API.

    Returns:
        dict: The JSON response from the Twitter API.
    """
    bearer_token = os.environ.get("bearer_token")
    if not bearer_token:
        raise ValueError("Bearer token not found. Ensure it is set in the environment variables.")

    search_url = "https://api.twitter.com/2/tweets/search/recent"
    query_params = {
        'query': '(#crypto OR #blockchain OR crypto OR blockchain OR Defi OR #defi OR Web3 OR #Web3)  '
                 '(#startup OR company OR build OR Building OR Project OR #Project OR startup OR We\'re OR launch OR '
                 'Launching OR #launch)  '
                 '(-breaking -news -meme -is:retweet)',
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
