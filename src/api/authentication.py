import os
import webbrowser
from dotenv import load_dotenv
import time
import requests

load_dotenv()

client_id = os.getenv("CLIENT_ID")
redirect_uri = "http://127.0.0.1"
scope = "tweet.read users.read follows.read dm.write offline.access "
state = "state"
code_challenge = "challenge"
code_challenge_method = "plain"

auth_url = (
    f"https://twitter.com/i/oauth2/authorize"
    f"?response_type=code"
    f"&client_id={client_id}"
    f"&redirect_uri={redirect_uri}"
    f"&scope={scope.replace(' ', '%20')}"
    f"&state={state}"
    f"&code_challenge={code_challenge}"
    f"&code_challenge_method={code_challenge_method}"
)

print(f"Open this URL in a browser to authorize the app:\n{auth_url}")

authorization_code = "VHJNVkFYdlZVanY2bkJqdVdjdzdzR2daQXdUaHQ1eFJZd0tNaUdzemFOUFEtOjE3MzY5NDk0MTM0NTQ6MTowOmFjOjE"
code_verifier = "challenge"
# Twitter API endpoint
url = "https://api.twitter.com/2/oauth2/token"
# Headers
headers = {
    "Content-Type": "application/x-www-form-urlencoded",
}

# Data
data = {
    "code": authorization_code,
    "grant_type": "authorization_code",
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "code_verifier": code_verifier,
}


def make_oauth_request():
    try:
        # Timing the request to ensure it's within the 30-second window
        start_time = time.time()
        response = requests.post(url, headers=headers, data=data)
        elapsed_time = time.time() - start_time

        # Check for a successful response
        if response.status_code == 200:
            print("Access token retrieved successfully!")
            print(response.json())
        else:
            print(f"Failed to retrieve access token. Status code: {response.status_code}")
            print(response.text)

        # Print the elapsed time to verify it's within 30 seconds
        print(f"Elapsed time: {elapsed_time:.2f} seconds")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    make_oauth_request()
    print("make_oauth_request()")
    print("webbrowser.open(auth_url)")




