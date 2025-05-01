# tweet_repo.py

import pandas as pd
import logging
from psycopg2.extras import execute_values, execute_batch
from src.database.connection import get_db_connection
from src.database.connection import get_db_connection_local
import csv




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


def insert_tweets_from_csv(csv_path):
    """
    Inserts rows into the 'tweets' table from a CSV file.
    If the 'id' already exists, it skips (does nothing).
    """
    with get_db_connection_local() as (conn, cursor):
        if cursor:
            try:
                inserts = []

                # Read the CSV
                with open(csv_path, newline='', encoding='utf-8') as csvfile:
                    reader = csv.DictReader(csvfile)
                    for row in reader:
                        inserts.append((
                            row['id'],
                            row['created_at'] or None,
                            row['text'] or None,
                            safe_int(row['author_id']) or None,
                            row['referenced_tweet_id'] or None,
                            row['tweet_url'] or None,
                            row['like_count_ref'] or None,
                            row['reply_count_ref'] or None,
                            row['retweet_count_ref'] or None,
                            row['impression_count_ref'] or None,
                            row['author_name'] or None,
                            row['referenced_username'] or None,
                            row['author_url'] or None,
                            row['referenced_author_description'] or None,
                            row['text_ref'] or None,
                            row['label_text'] or None,
                            row['label_textref'] or None
                        ))

                if inserts:
                    # Insert all with ON CONFLICT (id) DO NOTHING
                    execute_values(cursor, """
                        INSERT INTO tweets (
                            id, created_at, text, author_id, referenced_tweet_id,
                            tweet_url, like_count_ref, reply_count_ref, retweet_count_ref, impression_count_ref,
                            author_name, referenced_username, author_url, referenced_author_description,
                            text_ref, label_text, label_textref
                        ) VALUES %s
                        ON CONFLICT (id) DO NOTHING
                    """, inserts)
                    conn.commit()

                    print(f"Successfully inserted {cursor.rowcount} rows (skipped duplicates).")
                else:
                    print("No inserts found in CSV.")

            except Exception as e:
                print("Error during insert:", e)
                conn.rollback()

def safe_int(value):
    try:
        # Remove quotes if any
        value = str(value).strip()
        # Convert scientific notation to int
        if 'e' in value.lower():
            return int(float(value))
        return int(value)
    except:
        return None



if __name__ == "__main__":
    # Example usage
    csv_path = "../../data/backup_tweets_original_27April25.csv"
    insert_tweets_from_csv(csv_path)