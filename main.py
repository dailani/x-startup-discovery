from datetime import datetime

from prefect import flow

from src.api.search_recent_tweets import fetch_twitter_data
from src.database.tweet_repo import load_tweets
from src.file_operations.file_operations import save_json_to_file, filter_x_handles_with_score
from src.tweets_pipeline.normalize_tweets import normalise_json_tweets
from src.xai.profiles_pipeline.load import load_startup_profiles
from src.xai.tweets_analyzer import TweetAnalyzer
from src.xai.tweets_processor import TweetProcessor
from src.xai.xai_client import XAIClient


@flow(log_prints=True)
def tweets_pipeline():
    timestamp = datetime.now().strftime("%a%m%y%H%M")  # Format: MonMMYYHHMM

    # 1. Search recent twitter data
    json_response = fetch_twitter_data()

    # 2. Normalize the Data into a Pandas Dataframe
    normalized_tweets_df = normalise_json_tweets(json_response)

    # 3. Pass to DB insertion task
    load_tweets(normalized_tweets_df)

    # analyze_tweets(json_response)
    # 3. Pass to DB insertion task and store the result
    db_status = load_tweets(normalized_tweets_df)

    # ✅ Print the returned status for visibility in logs
    print("📝 DB Insertion Summary:", db_status)

    # Optional: you can return it too
    return db_status


def xai_pipeline():


    # analyze_tweets(json_response)
    xai_client = XAIClient()

    # Instantiate the tweet analyzer using the XAI client
    tweet_analyzer = TweetAnalyzer(xai_client)

    # Create a processor that will read, analyze, and write tweets with their scores
    tweet_processor = TweetProcessor(tweet_analyzer)

    # 3.Ranking
    #ranked_df = tweet_processor.process_file(normalized_tweets_df, ranked_output_csv)

    # Extracting
   # tweet_handles = filter_x_handles_with_score(ranked_df, 6)
   # load_startup_profiles(tweet_handles)




if __name__ == "__main__":
    tweets_pipeline()
