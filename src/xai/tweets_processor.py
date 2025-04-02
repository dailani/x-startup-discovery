import pandas as pd
from pandas import DataFrame

from .tweets_analyzer import TweetAnalyzer


class TweetProcessor:
    def __init__(self, analyzer: TweetAnalyzer) -> DataFrame:
        self.analyzer = analyzer

    def process_file(self, input_df: DataFrame, output_csv: str):
        """
        Processes a DataFrame with tweets and author info, analyzes each tweet, and saves
        the results (including computed category, relevance score, and reasoning)
        to a new CSV.

        The DataFrame is expected to have at least the following columns:
          - "text": the text content of the tweet.
        """
        try:
            df = input_df.copy()  # Create a copy to avoid modifying the original
            df.dropna(subset=["text"], inplace=True)
        except Exception as e:
            print(f"Failed to process DataFrame: {e}")
            return

        categories = []
        scores = []
        reasonings = []

        for index, row in df.iterrows():
            text = row["text"].strip() if isinstance(row["text"], str) else ""
            print(f"------------<<<< Processing tweet {index} >>>>>>---------")

            if not text:
                categories.append("N/A")
                scores.append(0)
                reasonings.append("No text available")
                continue

            category, score, reasoning = self.analyzer.analyze_tweet(text)
            categories.append(category)
            scores.append(score)
            reasonings.append(reasoning)
            print(f"Processed tweet {index}: Category='{category}', Score={score}")

        df["category"] = categories
        df["score"] = scores
        df["reasoning"] = reasonings

        try:
            df.to_csv(output_csv, index=False)
            print(f"Results saved to {output_csv}")
            return df
        except Exception as e:
            print(f"Failed to write CSV: {e}")