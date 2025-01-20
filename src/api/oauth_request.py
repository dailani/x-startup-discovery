import os
from dotenv import load_dotenv
from requests_oauthlib import OAuth1Session

load_dotenv()


def send_group_message(api, participant_ids, message_text):
    url = "https://api.twitter.com/2/dm_conversations"

    # Construct the payload
    payload = {
        "conversation_type": "Group",
        "participant_ids": participant_ids,
        "message": {
            "text": message_text
        }
    }

    # Make the request
    response = api.get(url, params=payload)
    print("Response status code:", response.status_code)
    print("Response text:", response.text)

    # Check for errors and return response
    if response.status_code == 200:
        print("Message sent successfully.")
    else:
        print(f"Failed to send message. Status code: {response.status_code}, Response: {response.text}")

    return response.json()


if __name__ == "__main__":
    api = OAuth1Session(
        client_key=os.getenv("consumer_id"), client_secret=os.getenv("consumer_secret"),
        resource_owner_key=os.getenv("access_token"),
        resource_owner_secret=os.getenv("token_secret")
    )
    try:
        participant_ids = ["1369627941710290946", "1465607856040943616,1585648096520069121"]
        message_text = "hello to you two, this is a new group conversation."
        send_group_message(api, participant_ids, message_text)

    except Exception as e:
        print(e)
