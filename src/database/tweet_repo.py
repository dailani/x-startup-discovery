# tweet_repo.py

import pandas as pd
import logging
from psycopg2.extras import execute_values
from src.database.connection import get_db_connection


def load_tweets(tweet_df: pd.DataFrame):
    inserted_count = 0
    failed_rows = []

    # Prepare the values for batch insert
    values = []
    for index, row in tweet_df.iterrows():
        try:
            values.append((
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
            ))
        except Exception as e:
            failed_rows.append((index, row.get('id'), f"Data prep error: {str(e)}"))

    if not values:
        logging.warning("⚠️ No valid rows to insert.")
        return {
            "status": "fail",
            "inserted": 0,
            "failed": len(failed_rows),
            "errors": failed_rows
        }
    logging.info("Values Count: ",  len(values))
    # Use a single connection and insert in batch
    with get_db_connection() as (conn, cursor):
        if cursor:
            try:
                execute_values(cursor, """
                    INSERT INTO tweets (
                        id, created_at, text, author_id, referenced_tweet_id,
                        tweet_url, author_name, referenced_username, author_url,
                        referenced_author_description, text_ref
                    ) VALUES %s
                    ON CONFLICT (id) DO NOTHING
                """, values)

                conn.commit()
                inserted_count = len(values)
                logging.info(f"✅ Inserted {inserted_count} tweets into the database.")
            except Exception as e:
                logging.error("❌ Failed batch insert into tweets.")
                logging.exception(e)
                failed_rows.extend([(None, None, f"DB insert error: {str(e)}")])

    return {
        "status": "success" if inserted_count == len(tweet_df) else "partial",
        "inserted": inserted_count,
        "failed": len(failed_rows),
        "errors": failed_rows if failed_rows else None
    }
