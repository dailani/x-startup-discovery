
import pandas as pd

from src.api.search_recent_tweets import  fetch_twitter_data
from src.file_operations.file_operations import save_json_to_file


def analyze_tweets(json_response):
    """
    1. Convert the JSON response into pandas DataFrames.
    2. Perform simple data analysis or classification as an example.
    3. Print or return results.
    """

    # --- Convert "data" field into a tweets DataFrame ---
    if "data" in json_response:
        tweets_df = pd.DataFrame(json_response["data"])
    else:
        print("No 'data' field found in the JSON response.")
        return

    # --- Convert "includes"->"users" field into a users DataFrame (if present) ---
    if "includes" in json_response and "users" in json_response["includes"]:
        users_df = pd.DataFrame(json_response["includes"]["users"])
    else:
        users_df = pd.DataFrame()  # Empty if no user data

    # --- Print basic info ---
    print("\n=== Tweets DataFrame (first 5 rows) ===")
    print(tweets_df.head())

    print("\n=== Users DataFrame (first 5 rows) ===")
    print(users_df.head())

    # --- Example: Count tweets by author ---
    # Some tweets may not have an author_id if the data is incomplete, so we use fillna or a safer approach.
    tweet_counts = tweets_df["author_id"].value_counts(dropna=False)
    print("\n=== Tweet Counts by author_id ===")
    print(tweet_counts)

    # --- Merge tweets and users on ID if you want combined info ---
    # The user DataFrame has "id" = user’s ID, while the tweets_df has "author_id"
    merged_df = pd.merge(tweets_df, users_df, left_on="author_id", right_on="id", how="left")
    print("\n=== Merged Tweet/User DataFrame (first 5 rows) ===")
    print(merged_df.head())

    # --- Simple classification example: Check if tweets mention "crypto" or "ai" in text ---
    tweets_df["mentions_crypto"] = tweets_df["text"].str.lower().str.contains("crypto", na=False)
    tweets_df["mentions_ai"] = tweets_df["text"].str.lower().str.contains("ai", na=False)

    print("\n=== Classification columns ===")
    print(tweets_df[["id", "text", "mentions_crypto", "mentions_ai"]].head())

    # --- Additional Stats (Optional) ---
    # For example, how many mention "crypto" vs. "ai"
    print("\n=== # of Tweets Mentioning 'Crypto' ===")
    print(tweets_df["mentions_crypto"].sum())

    print("\n=== # of Tweets Mentioning 'AI' ===")
    print(tweets_df["mentions_ai"].sum())

if __name__ == "__main__":
    json_response = fetch_twitter_data()
    save_json_to_file(json_response)
    analyze_tweets(json_response)
