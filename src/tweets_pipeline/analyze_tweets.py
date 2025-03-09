import pandas as pd


def get_referenced_tweet_ids(file_path):
    """
    Reads 'referenced_tweet_id' column from a file and returns an array of strings

    Parameters:
    file_path (str): Path to the file (CSV, Excel, etc.) containing the data

    Returns:
    numpy.ndarray: Array of strings containing referenced_tweet_id values
    """
    try:
        # Read the file into a pandas DataFrame
        # Assuming CSV format, adjust read method based on your file type
        df = pd.read_csv(file_path)

        # Check if 'referenced_tweet_id' column exists
        if 'referenced_tweet_id' not in df.columns:
            raise ValueError("Column 'referenced_tweet_id' not found in the file")

        # Convert to string and return as numpy array
        tweet_ids = df['referenced_tweet_id'].astype(str).values

        return tweet_ids

    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
        return None
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return None

# Example usage:
# file_path = 'your_data.csv'
# tweet_ids = get_referenced_tweet_ids(file_path)
# if tweet_ids is not None:
#     print(tweet_ids)