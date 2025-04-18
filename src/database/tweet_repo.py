# tweet_repo.py

import pandas as pd
import logging
from psycopg2.extras import execute_values
from src.database.connection import get_db_connection


def load_tweets(tweet_df: pd.DataFrame):
    tweet_df = tweet_df.drop_duplicates(subset='id')

    failed_rows = []
    values = []
    tweet_ids = []

    for index, row in tweet_df.iterrows():
        try:
            tweet_id = int(row['id'])
            tweet_ids.append(tweet_id)
            values.append((
                tweet_id,
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

    inserted_count = 0
    tweet_ids = tweet_df['id'].astype(int).tolist()  # Ensure integer IDs

    with get_db_connection() as (conn, cursor):
        if cursor:
            try:
                cursor.execute("""
                                SELECT id FROM tweets WHERE id = ANY(%s);
                            """, (tweet_ids,))
                existing_ids = set(row[0] for row in cursor.fetchall())

                cursor.execute("SELECT COUNT(*) FROM tweets;")
                pre_count = cursor.fetchone()[0]

                # Execute the batch insert
                execute_values(cursor, """
                    INSERT INTO tweets (
                        id, created_at, text, author_id, referenced_tweet_id,
                        tweet_url, author_name, referenced_username, author_url,
                        referenced_author_description, text_ref
                    ) VALUES %s
                    ON CONFLICT (id) DO NOTHING
                """, values)

                conn.commit()
                # After insert
                cursor.execute("SELECT COUNT(*) FROM tweets;")
                post_count = cursor.fetchone()[0]

                inserted_count = post_count - pre_count
                skipped_conflicts = len(values) - inserted_count

                logging.info(f"✅ Attempted to insert {len(values)} tweets.")
                logging.info(f"✅ Successfully inserted {inserted_count} new tweets.")
                logging.info(f"⚠️ Skipped {skipped_conflicts} ")
                logging.info(
                    f"⚠️ {len(existing_ids)} out of {len(tweet_ids)} tweet IDs already exist in the database.)")

            except Exception as e:
                logging.error("❌ Failed to insert tweets.")
                logging.exception(e)
                failed_rows.extend([(None, None, f"DB insert error: {str(e)}")])

    return {
        "status": "success" if inserted_count == len(tweet_df) else "partial",
        "inserted": inserted_count,
        "failed": len(failed_rows) + skipped_conflicts,
        "skipped_conflicts": skipped_conflicts,
        "existing_ids": len(existing_ids),
        "errors": failed_rows if failed_rows else None
    }
