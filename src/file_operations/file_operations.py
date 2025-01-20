import pandas as pd

# Read the CSV file
file_path = "../../data/processed/twitter_user_info.csv"
output_file_path = "../../data/processed/twitter_group_dm.csv"


def get_twitter_ids():
    """
    Get the Twitter IDs from the CSV file. Update Sent
    Returns:
        list: Twitter IDs.
    """

    df = pd.read_csv("../../data/processed/twitter_group_dm.csv")

    # Step 1: Filter rows where status == "valid" and sent == "no"
    filtered_df = df[(df["status"] == "valid") & (df["sent"] == "No")]

    # Step 2: Randomly sample 10 rows
    sampled_rows = filtered_df.sample(n=min(10, len(filtered_df)), random_state=42)

    # Step 3: Extract the 'id' values
    sampled_ids = sampled_rows["id"].tolist()

    # Step 4: Update the 'sent' column for the sampled rows
    df.loc[df["id"].isin(sampled_ids), "sent"] = "Yes"

    # Step 5: Save the updated DataFrame back to the CSV
    df.to_csv("twitter_group_dm.csv", index=False)

    # Output the resulting array of IDs
    print("Sampled IDs:", sampled_ids)


if __name__ == "__main__":
    get_twitter_ids()
