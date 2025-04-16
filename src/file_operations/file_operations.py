from datetime import datetime

import pandas as pd
import re
import json

from pandas import DataFrame


from prefect import task  # Prefect flow and task decorators


def get_column_from_df(df, column):
    try:
        if column not in df.columns:
            raise ValueError(f"Column {column} not found in DataFrame")
        tweet_ids = df[column].astype(str).values
        return tweet_ids
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None


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


@task(log_prints=True)
def save_json_to_file(data, tweets_filename):
    """
    Save a Python dictionary as a JSON file.

    Parameters:
        data (dict): The dictionary to save as JSON.
    Returns:
        None
    """
    import os

    # Generate a unique filename with the current timestamp

    try:

        with open(tweets_filename, 'w') as json_file:
            json.dump(data, json_file, indent=4)
        print(f"Data successfully saved to {tweets_filename}")
    except Exception as e:
        print(f"An error occurred while saving the file: {e}")


def filter_x_handles_with_score(ranked_df: DataFrame, score: int) -> list:
    """
    Reads a CSV file, filters a specific column based on a condition, and returns the filtered values.

    :param ranked_df:
    :param score:
    :return: A list of filtered column values
    """
    # Read the CSV file
    df = ranked_df.copy()

    filtered_df = df[df['score'] >= score]

    # Extract usernames from URLs
    usernames = filtered_df['author_username'].apply(
        lambda url: re.search(r"https://x.com/([^/]+)", url).group(1) if isinstance(url, str) and re.search(
            r"https://x.com/([^/]+)", url) else None)

    # Return the list of usernames (excluding None values)
    return usernames.dropna().tolist()


if __name__ == "__main__":
    get_twitter_ids()
