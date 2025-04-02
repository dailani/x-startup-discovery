from datetime import datetime

from src.api.search_recent_tweets import fetch_twitter_data
from src.file_operations.file_operations import save_json_to_file, filter_x_handles_with_score
from src.tweets_pipeline.normalize_tweets import normalise_json_tweets
from src.xai.profiles_pipeline.load import load_startup_profiles
from src.xai.tweets_analyzer import TweetAnalyzer
from src.xai.tweets_processor import TweetProcessor
from src.xai.xai_client import XAIClient

if __name__ == "__main__":
    timestamp = datetime.now().strftime("%a%m%y%H%M")  # Format: MonMMYYHHMM
    raw_tweets_filename = f"C:/Users/Dajlan/PycharmProjects/x-startup-discover/data/raw/tweets/firebase_{timestamp}.json"
    ranked_output_csv = f"../../data/ranked/tweets_{timestamp}_ranked.csv"
    #1. Search recent twitter data
    json_response = fetch_twitter_data()
    save_json_to_file(json_response,raw_tweets_filename)

    #2. Normalize the Data into a Pandas Dataframe
    normalized_tweets_df = normalise_json_tweets(raw_tweets_filename)
    #analyze_tweets(json_response)

    xai_client = XAIClient()

    # Instantiate the tweet analyzer using the XAI client
    tweet_analyzer = TweetAnalyzer(xai_client)

    # Create a processor that will read, analyze, and write tweets with their scores
    tweet_processor = TweetProcessor(tweet_analyzer)

    #3.Ranking
    ranked_df = tweet_processor.process_file(normalized_tweets_df, ranked_output_csv)

    #Extracting
    tweet_handles = filter_x_handles_with_score(ranked_df, 6)
    load_startup_profiles(tweet_handles)




