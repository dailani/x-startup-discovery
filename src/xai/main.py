from xai_client import XAIClient
from tweets_analyzer import TweetAnalyzer
from tweets_processor import TweetProcessor


def main():
    # Create an instance of the XAI client (API key is pulled from environment variables)
    xai_client = XAIClient()

    # Instantiate the tweet analyzer using the XAI client
    tweet_analyzer = TweetAnalyzer(xai_client)

    # Create a processor that will read, analyze, and write tweets with their scores
    tweet_processor = TweetProcessor(tweet_analyzer)

    # Define input and output CSV paths
    input_csv = "../../data/processed/tweets_with_author_info_Wed02251312.csv"
    output_csv = "../../data/ranked/tweets_Wed02251312_ranked.csv"

    # Process the tweets
    tweet_processor.process_file(input_csv, output_csv)


if __name__ == "__main__":
    main()
