import os

from dotenv import load_dotenv
import requests
# Load your mounted .env file
try:
    load_dotenv("/secrets/x-startup-secrets")
except Exception as e:
    print("❌ Failed to load .env secret:", e)

# Replace with your Bearer Token from the Twitter Developer Portal
BEARER_TOKEN = os.getenv('BEARER_TOKEN')
# Set up the headers for authorization
HEADERS = {
    "Authorization": f"Bearer {BEARER_TOKEN}"
}

# Base URL for Twitter API v2
BASE_URL = "https://api.twitter.com/2"


# Print the result

def search_multiple_usernames(usernames):
    """
    Fetch details for multiple usernames from the Twitter API.
    Args:
        usernames (str): Comma-separated usernames (e.g., "user1,user2").
    Returns:
        dict: JSON response from the API containing user details.
    """
    url = f"{BASE_URL}/users/by"
    params = {
        "usernames": usernames  # Comma-separated list of usernames
    }
    response = requests.get(url, headers=HEADERS, params=params)
    if response.status_code == 200:
        return print(response.json())
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None


if __name__ == "__main__":
    search_multiple_usernames("3829831,369966635,19469573")
