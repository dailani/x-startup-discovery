from src.file_operations.file_operations import filter_x_handles_with_score
from src.xai.profiles_pipeline.load import load_startup_profiles

tweet_handles = filter_x_handles_with_score('../../../data/ranked/tweets_test_ranked.csv', 6)

if __name__ == "__main__":
    load_startup_profiles(['iAgentProtocol','StarknetLM','WolfNationNFT'])
