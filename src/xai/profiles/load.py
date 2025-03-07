import csv

from src.xai.profiles.extract import extract_profile_info
from src.xai.xai_client import XAIClient

# Initialize XAIClient once at the beginning
xai_client = XAIClient()
def load_startup_profiles(tweet_handles: []):
    startup_profiles = []


    for handle in tweet_handles:
        profile_data = extract_profile_info(handle,xai_client)
        if profile_data:
            startup_profiles.append([
                handle,
                ", ".join(profile_data.get("Industry_Keywords_Hashtags", [])),
                profile_data.get("Number_of_Founders", "null"),
                ", ".join(profile_data.get("Name_of_Founders", []) or []),
                profile_data.get("Grants_or_Funding_Won", 0),
                ", ".join(profile_data.get("Investor_Ecosystem_Engagement", []) or []),
                profile_data.get("Reasoning", {}).get("Number_of_Steps", "null"),
                " | ".join(profile_data.get("Reasoning", {}).get("Steps_Involved", []))
            ])

    # Save to CSV
    headers = [
        "X_Handle", "Industry_Keywords_Hashtags", "Number_of_Founders", "Name_of_Founders",
        "Grants_or_Funding_Won", "Investor_Ecosystem_Engagement", "Reasoning_Number_of_Steps",
        "Reasoning_Steps_Involved"
    ]

    with open('../../../data/profiles/startup_profiles.csv', mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow(headers)
        writer.writerows(startup_profiles)

    print(f"Data successfully saved to ../../../profiles")
