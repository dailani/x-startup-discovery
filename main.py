import csv

from fastapi import FastAPI
from src.api.api_requests import search_multiple_usernames
import pandas as pd

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}


def get_user_info():
    # Read the CSV file
    df = pd.read_csv("data/raw/output_handles.csv")

    # Get Twitter handles as a list
    twitter_handles = df['Twitter Handle'].astype(str).tolist()

    # Prepare output list
    results = []

    # Chunk size (maximum 100 usernames per request)
    chunk_size = 100

    # Process handles in chunks
    for i in range(0, len(twitter_handles), chunk_size):
        # Get the current chunk
        chunk = twitter_handles[i:i + chunk_size]

        # Convert the chunk to a comma-separated string
        usernames = ','.join(chunk)

        print(f"Fetching details for usernames: {usernames}")

        # Call the Twitter API for the current chunk
        user_data = search_multiple_usernames(usernames)

        # Process the response
        if user_data and "data" in user_data:
            for user in user_data["data"]:
                results.append({
                    "id": user.get("id", ""),
                    "name": user.get("name", ""),
                    "username": user.get("username", ""),
                    "status": "valid"
                })

        # Handle errors in the response
        if user_data and "errors" in user_data:
            for error in user_data["errors"]:
                status = "not found" if "Not Found Error" in error.get("title", "") else \
                         "suspended" if "suspended" in error.get("detail", "").lower() else "unknown"
                results.append({
                    "id": error.get("resource_id", ""),
                    "name": "",
                    "username": error.get("value", ""),
                    "status": status
                })

    # Save results to a CSV file
    output_file = "data/processed/twitter_user_info.csv"
    with open(output_file, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=["id", "name", "username", "status"])
        writer.writeheader()
        writer.writerows(results)

    print(f"User information saved to {output_file}")


if __name__ == "__main__":
    get_user_info()
