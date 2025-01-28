from datetime import datetime
import json
import pandas as pd

filename = "../../data/raw/tweets/firebase_Sun01252042.json"
proccessed_filename = "../../data/processed/"
def normalise_json_tweets(filename):

    with open(filename, "r", encoding="utf-8") as f:
        twitter_json = json.load(f)

    # 2. Normalize the "data" section (tweets)
    tweets_df = pd.json_normalize(twitter_json, record_path=["data"])
    tweets_df["tweet_url"] = "https://x.com/x/status/" + tweets_df["id"].astype(str)

    # 3. Normalize the "includes.users" section (user info)
    users_df = pd.json_normalize(twitter_json, record_path=["includes", "users"])

    # 4. Rename columns in users_df so we can merge easily and have descriptive names
    #    We want:
    #       - 'id' -> 'author_id'
    #       - 'name' -> 'author_name'
    #       - 'username' -> 'author_username'
    users_df.rename(
        columns={
            "id": "author_id",
            "name": "author_name",
            "username": "author_username"
        },
        inplace=True
    )


    # 5. Merge tweets with user info on "author_id"
    merged_df = pd.merge(
        tweets_df,
        users_df[["author_id", "author_name", "author_username"]],
        on="author_id",
        how="left"
    )
    # 6. Flatten public_metrics into separate columns (optional, but often useful)
    if "public_metrics" in merged_df.columns:
        public_metrics_df = pd.json_normalize(merged_df["public_metrics"])
        # Concatenate flattened metrics back to merged_df
        merged_df = pd.concat(
            [merged_df.drop(columns=["public_metrics"]), public_metrics_df],
            axis=1
        )

    # 7. Convert author_username into a link
    #    Instead of showing just "bob_abc", we show "https://x.com/bob_abc"
    merged_df["author_username"] = "https://x.com/" + merged_df["author_username"].astype(str)

    # 8. Select columns you want in the final CSV
    desired_columns = [
        "author_id",
        "author_name",
        "author_username",
        "created_at",
        "retweet_count",
        "reply_count",
        "like_count",
        "quote_count",
        "tweet_url"
        "text",
    ]


    # Make sure the columns exist (in case some columns are missing)
    final_columns = [col for col in desired_columns if col in merged_df.columns]
    final_df = merged_df[final_columns].copy()

    # 9. Save to CSV
    timestamp = datetime.now().strftime("%a%m%y%H%M")  # Format: MonMMYYHHMM
    final_df.to_csv(proccessed_filename + f"tweets_with_author_info_{timestamp}.csv", index=False)

    print("CSV file 'tweets_with_author_url.csv' created successfully.")

if __name__ == "__main__":
    normalise_json_tweets(filename)