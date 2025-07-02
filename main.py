import praw
import os
import yt_dlp
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

def download_video(url, filename='video.mp4'):
    ydl_opts = {
        'outtmpl': filename,
        'format': 'bv+ba/best',
        'merge_output_format': 'mp4',
        'quiet': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

