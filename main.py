import csv

from fastapi import FastAPI
from src.api.api_requests import search_multiple_usernames
import pandas as pd

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello Worlds"}


@app.get("/hello/{name}")
async def say_hello(name: str):
    return {"message": f"Hello {name}"}



if __name__ == "__main__":
    print("")