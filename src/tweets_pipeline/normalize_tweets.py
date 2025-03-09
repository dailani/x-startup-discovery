from datetime import datetime
import json
import pandas as pd

from src.api.requests_templates.get_users import fetch_users, create_url
from src.file_operations.file_operations import get_column_from_df

processed_filename = "../../data/processed/"


def normalise_json_tweets(filename):
    with open(filename, "r", encoding="utf-8") as f:
        twitter_json = json.load(f)

    # 1. Normalize the "data" section (tweets)
    tweets_df = pd.json_normalize(twitter_json, record_path=["data"])
    # 1.1 get referenced tweet id
    tweets_df["referenced_tweet_id"] = tweets_df["referenced_tweets"].apply(
        lambda x: x[0]["id"] if isinstance(x, list) and len(x) > 0 else None)
    # Drop the original 'referenced_tweets' column if no longer needed
    tweets_df.drop(columns=["referenced_tweets"], inplace=True)

    print(" tweets_df referenced_tweet_id", tweets_df["referenced_tweet_id"])
    print("Tweets headers:", tweets_df.columns)

    tweets_df["tweet_url"] = "https://x.com/x/status/" + tweets_df["id"].astype(str)
    print("# 1. Normalized tweets data:", tweets_df.columns)

    # 2. Normalize the "includes.tweets" section (for additional data, such as public metrics)
    if "includes" in twitter_json and "tweets" in twitter_json["includes"]:
        includes_df = pd.json_normalize(twitter_json, record_path=["includes", "tweets"])
        print("# 2. Normalized includes.tweets data:", includes_df.columns)

        includes_df = includes_df[
            ["id",
             "author_id",
             "public_metrics.retweet_count",
             "public_metrics.reply_count",
             "public_metrics.like_count",
             "public_metrics.quote_count",
             "public_metrics.bookmark_count",
             "public_metrics.impression_count",
             "note_tweet.entities.mentions",
             "note_tweet.text",
             "note_tweet.entities.hashtags",
             "note_tweet.entities.urls"
             ]
        ].rename(columns={"id": "tweet_id", "author_id": "referenced_author_id"})

        # 3. Merge with tweets_df based on tweet id
        tweets_df = tweets_df.merge(includes_df, left_on="referenced_tweet_id", right_on="tweet_id", how="outer",
                                    suffixes=("_tweets", "_inc"))
        print("# 3. Merged tweets with includes.tweets public metrics:", tweets_df.columns)

    # 4. Normalize the "includes.users" section (user info)
    if "includes" in twitter_json and "users" in twitter_json["includes"]:
        users_df = pd.json_normalize(twitter_json, record_path=["includes", "users"])
        print("# 4. Normalized includes.users data:", users_df.columns)

        # Rename columns for clarity
        users_df.rename(columns={
            "id": "author_id",
            "name": "author_name",
            "username": "author_username"
        }, inplace=True)

        # Merge with tweets_df on "author_id"
        tweets_df = tweets_df.merge(users_df[["author_id", "author_name", "author_username"]],
                                    on="author_id", how="left")
        print("# 5. Merged tweets with includes.users:", tweets_df.columns)

    # 5. Convert author_username into a link
    tweets_df["author_username"] = "https://x.com/" + tweets_df["author_username"].astype(str)

    # 6. Get X handles from the "includes" part of the json response
    x_referenced_id = get_column_from_df(tweets_df, 'referenced_author_id')
    url = create_url(x_referenced_id)
    x_referenced_handles_response = fetch_users(url)
    referenced_users_df = pd.DataFrame(x_referenced_handles_response["data"])

    referenced_users_df.rename(columns={
        "id": "referenced_author_id",
        "name": "referenced_author_name",
        "created_at": "referenced_author_created_at",
        "description": "referenced_author_description",
        "username": "referenced_username"
    }, inplace=True)

    print("tweets_df: ", tweets_df["referenced_author_id"], "user_df: ", referenced_users_df["referenced_author_id"])
    print("#6. Get X handles from referenced_tweet_ids", tweets_df.columns)
    tweets_df = tweets_df.merge(referenced_users_df,
                                on="referenced_author_id", how="outer")

    # 7. Save to CSV
    timestamp = datetime.now().strftime("%a%m%y%H%M")  # Format: MonMMYYHHMM
    tweets_df.to_csv(processed_filename + f"tweets_with_author_info_{timestamp}.csv", index=False)

    print("CSV file 'tweets_with_author_info.csv' created successfully:.", tweets_df.columns)

    return tweets_df
