import requests
import os
import json

# To set your enviornment variables in your terminal run the following line:
# export 'BEARER_TOKEN'='<your_bearer_token>'
bearer_token = os.environ.get("BEARER_TOKEN")


def create_url():
    # Specify the usernames that you want to lookup below
    # You can enter up to 100 comma-separated values.
    usernames = "usernames=TwitterDev,TwitterAPI"
    user_fields = "user.fields=description,created_at"
    # User fields are adjustable, options include:
    # created_at, description, entities, id, location, name,
    # pinned_tweet_id, profile_image_url, protected,
    # public_metrics, url, username, verified, and withheld
    url = "https://api.twitter.com/2/users/by?{}&{}".format(usernames, user_fields)
    return url


def create_url(user_ids=None):
    """
    Create a URL to lookup users by either username or ID.
    """
    user_fields = "user.fields=description,created_at"

    if user_ids is not None and len(user_ids) > 0:
        # Remove None values
        user_ids = [user_id for user_id in user_ids if
                    user_id != 'nan' and user_id != 'None']
        # Lookup users by ID
        ids = f"ids={','.join(user_ids)}"
        url = f"https://api.twitter.com/2/users?{ids}&{user_fields}"
    else:
        # Default lookup by username
        usernames = "usernames=TwitterDev,TwitterAPI"
        url = f"https://api.twitter.com/2/users/by?{usernames}&{user_fields}"

    return url


def bearer_oauth(r):
    """
    Method required by bearer token authentication.
    """

    r.headers["Authorization"] = f"Bearer {bearer_token}"
    r.headers["User-Agent"] = "v2UserLookupPython"
    return r


def fetch_users(url):
    response = requests.request("GET", url, auth=bearer_oauth, )
    print(response.status_code)
    if response.status_code != 200:
        raise Exception(
            "Request returned an error: {} {}".format(
                response.status_code, response.text
            )
        )
    return response.json()


def main():
    url = create_url(['1898393632245190699'])
    json_response = fetch_users(url)
    print(json.dumps(json_response, indent=4, sort_keys=True))


if __name__ == "__main__":
    main()
