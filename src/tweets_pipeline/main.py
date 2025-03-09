from datetime import datetime

from src.api.search_recent_tweets import fetch_twitter_data
from src.file_operations.file_operations import save_json_to_file
from src.tweets_pipeline.normalize_tweets import normalise_json_tweets



if __name__ == "__main__":
    timestamp = datetime.now().strftime("%a%m%y%H%M")  # Format: MonMMYYHHMM
    raw_tweets_filename = f"C:/Users/Dajlan/PycharmProjects/x-startup-discover/data/raw/tweets/firebase_{timestamp}.json"

    #1. Search recent twitter data
    json_response = fetch_twitter_data()
    save_json_to_file(json_response,raw_tweets_filename)

    #2. Normalize the Data into a Pandas Dataframe
    normalized_tweets_df = normalise_json_tweets(raw_tweets_filename)
    #analyze_tweets(json_response)

