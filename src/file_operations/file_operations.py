from datetime import datetime

import pandas as pd

import json

# Read the CSV file
raw_filepath = "../../data/raw"
processed_filepath = "../../data/processed"


def get_twitter_ids():
    """
    Get the Twitter IDs from the CSV file. Update Sent
    Returns:
        list: Twitter IDs.
    """

    df = pd.read_csv("../../data/processed/twitter_group_dm.csv")

    # Step 1: Filter rows where status == "valid" and sent == "no"
    filtered_df = df[(df["status"] == "valid") & (df["sent"] == "No")]

    # Step 2: Randomly sample 10 rows
    sampled_rows = filtered_df.sample(n=min(50, len(filtered_df)), random_state=42)

    # Step 3: Extract the 'id' values
    sampled_ids = sampled_rows["id"].tolist()

    # Step 4: Update the 'sent' column for the sampled rows
    df.loc[df["id"].isin(sampled_ids), "sent"] = "Yes"

    # Step 5: Save the updated DataFrame back to the CSV
    df.to_csv("../../data/processed/twitter_group_dm.csv", index=False)

    # Output the resulting array of IDs
    print("Sampled IDs:", sampled_ids)




def save_json_to_file(data):
    """
    Save a Python dictionary as a JSON file.

    Parameters:
        data (dict): The dictionary to save as JSON.
    Returns:
        None
    """
    import os

    # Generate a unique filename with the current timestamp
    timestamp = datetime.now().strftime("%a%m%y%H%M")  # Format: MonMMYYHHMM

    tweets_filename = f"C:/Users/Dajlan/PycharmProjects/x-startup-discover/data/raw/tweets/firebase_{timestamp}.json"

    try:

        with open(tweets_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {raw_filepath}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")



if __name__ == "__main__":
    get_twitter_ids()
