import csv
from datetime import datetime

from src.xai.profiles_pipeline.extract import extract_profile_info
from src.xai.xai_client import XAIClient

# Initialize XAIClient once at the beginning
xai_client = XAIClient()


def load_startup_profiles(tweet_handles: []):
    startup_profiles = []

    for handle in tweet_handles:
        profile_data = extract_profile_info(handle, xai_client)
        print("Profile Data: ",profile_data)
        if profile_data:
            startup_profiles.append([
                handle,
                profile_data.get("amount", 0),
                profile_data.get("type", "null"),
                profile_data.get("evidence", {}).get("sentence", "null"),
                profile_data.get("evidence", {}).get("post_URL", "null")
            ])
