# tweet_repo.py
from prefect import task
import pandas as pd
from src.database.connection import execute_query


@task(log_prints=True)
def load_tweets(tweet_df: pd.DataFrame):
    inserted_count = 0
    failed_rows = []

    for index, row in tweet_df.iterrows():
        try:
            result = execute_query(
                """
                INSERT INTO tweets (
                    id, created_at, text, author_id, referenced_tweet_id,
                    tweet_url, author_name, referenced_username, author_url,
                    referenced_author_description, text_ref
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                (
                    row['id'],
                    row['created_at'],
                    row['text'],
                    row['author_id'],
                    row.get('referenced_tweet_id'),
                    row['tweet_url'],
                    row['author_name'],
                    row.get('referenced_username'),
                    row['author_username'],
                    row.get('referenced_author_description'),
                    row.get('note_tweet.text_inc')
                )
            )
            if result:
                inserted_count += 1
            else:
                failed_rows.append((index, row['id'], str(result)))
        except Exception as e:
            return {"failed": ("failed", e)}

    return {
        "status": "success" if inserted_count == len(tweet_df) else "partial",
        "inserted": inserted_count,
        "failed": len(failed_rows),
        "errors": failed_rows if failed_rows else None
    }
