# user_repository.py

class TweetRepository:
    def __init__(self, db):
        self.db = db

    def load_tweet(self):
        result = self.db.execute_query("SELECT NOW();")
        if result:
            return result[0][0]
        return None
