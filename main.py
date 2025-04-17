import uuid
import psycopg2
from src.api.search_recent_tweets import fetch_twitter_data
from src.database.tweet_repo import load_tweets
from src.tweets_pipeline.normalize_tweets import normalise_json_tweets
from src.xai.tweets_analyzer import TweetAnalyzer
from src.xai.tweets_processor import TweetProcessor
from src.xai.xai_client import XAIClient
from fastapi import FastAPI, BackgroundTasks
from typing import Dict
from dotenv import load_dotenv
import os

try:
    load_dotenv("/secrets/x-startup-secrets")
except Exception as e:
    print("❌ Failed to load .env secret:", e)

app = FastAPI()

# Store status in memory (use Redis or DB for production)
pipeline_status: Dict[str, Dict[str, str]] = {}


def tweets_pipeline(task_id: str):
    try:
        pipeline_status[task_id] = {"step": "Fetching tweets"}
        # 1. Search recent twitter data
        json_response = fetch_twitter_data()

        pipeline_status[task_id] = {"step": "Cleaning tweets"}
        # 2. Normalize the Data into a Pandas Dataframe
        normalized_tweets_df = normalise_json_tweets(json_response)

        pipeline_status[task_id] = {"step": " Pass to DB insertion task"}

        # analyze_tweets(json_response)
        # 3. Pass to DB insertion task and store the result
        db_status = load_tweets(normalized_tweets_df)

        pipeline_status[task_id] = {"step": f"DB Insertion Summary: {db_status}:"}


        return db_status
    except Exception as e:
        pipeline_status[task_id] = {"step": f"❌ Error: {str(e)}"}


def xai_pipeline():
    # analyze_tweets(json_response)
    xai_client = XAIClient()

    # Instantiate the tweet analyzer using the XAI client
    tweet_analyzer = TweetAnalyzer(xai_client)

    # Create a processor that will read, analyze, and write tweets with their scores
    tweet_processor = TweetProcessor(tweet_analyzer)

    # 3.Ranking
    # ranked_df = tweet_processor.process_file(normalized_tweets_df, ranked_output_csv)

    # Extracting


# tweet_handles = filter_x_handles_with_score(ranked_df, 6)
# load_startup_profiles(tweet_handles)


@app.post("/run-tweets-pipeline")
async def run_tweets(background_tasks: BackgroundTasks):
    task_id = str(uuid.uuid4())  # Unique ID for this pipeline run
    print("Status Id", task_id)
    pipeline_status[task_id] = {f"Task: {task_id}": "⏳ Starting..."}
    background_tasks.add_task(tweets_pipeline, task_id)
    return {"status": "Pipeline triggered", "task_id": task_id}


@app.get("/status/{task_id}")
async def get_status(task_id: str):
    status = pipeline_status.get(task_id, {"step": "❓ Not found"})
    return {"task_id": task_id, "status": status}


@app.get("/")
def ping():
    return {"message": "✅ Service is alive"}

@app.get("/debug-db")
def debug_db():
    conn = None
    try:
        conn = psycopg2.connect(
            user=os.getenv("USER"),
            password=os.getenv("POSTGRES_PASS"),
            host=os.getenv("HOST"),
            port='5432',
            dbname=os.getenv("DBNAME"),
            sslmode='require'
        )
        cursor = conn.cursor()
        print("✅ Database connection established.")
        yield conn, cursor
    except Exception as e:
        print("❌ Failed to connect to the database:", e)
        yield None, None
    finally:
        if conn:
            conn.close()
            print("🔒 Connection closed.")


