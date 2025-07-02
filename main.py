import praw
import os
from dotenv import load_dotenv

load_dotenv()

def get_reddit_post():
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRRET"),
        user_agent=os.getenv("USER_AGENT")
    )
    sub = reddit.subreddit("MemeVideos")
    for post in sub.hot(limit=20):
        if 'v.redd.it' in post.url:
            return post.title, post.url
    return None, None
    