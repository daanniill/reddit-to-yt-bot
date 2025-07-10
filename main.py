import praw
import os
import yt_dlp
import moviepy as mp
from moviepy import VideoFileClip
from dotenv import load_dotenv
import time
from pathlib import Path

load_dotenv()

PROCESSED_IDS_FILE = "processed_ids.txt"

def load_processed_ids():
    file_path = Path(PROCESSED_IDS_FILE)
    file_path.touch()
    if not os.path.exists(PROCESSED_IDS_FILE):
        return set()
    with open(PROCESSED_IDS_FILE, "r") as f:
        return set(line.strip() for line in f.readlines())

def save_processed_id(post_id):
    with open(PROCESSED_IDS_FILE, "a") as f:
        f.write(post_id + "\n")

def get_reddit_posts(seen_ids):
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT")
    )
    print(reddit.read_only)  # Should print: True

    posts = []

    sub = reddit.subreddit("MemeVideos")
    for post in sub.hot(limit=5):
        if 'v.redd.it' in post.url and post.id not in seen_ids:
            posts.append((post.title, post.url, post.id))
    return posts

def download_video(url, filename='video.mp4'):
    ydl_opts = {
        'outtmpl': filename,
        'format': 'bv*+ba/best',
        'merge_output_format': 'mp4',
        'quiet': False,  # Set to True to hide logs
        'postprocessors': [{
            'key': 'FFmpegVideoConvertor',
            'preferedformat': 'mp4',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

def make_shorts_video(video_path, output_filename=None):
    video = VideoFileClip(video_path)
    # Resizing vid to 720x1280 while perserving aspect ratio
    video = video.resized(height=1280)
    video = video.cropped(width=720, x_center=video.w/2)

    # directing output folder
    output_folder = "vids"
    isExist = os.path.exists(output_folder)
    if not isExist:
        os.makedirs(output_folder)

    output_path = os.path.join(output_folder, output_filename)

    final = mp.CompositeVideoClip([video])
    final.write_videofile(output_path, fps=30)

def main():
    print("[1] Fetching Reddit video posts...")
    seen_ids = load_processed_ids()
    posts = get_reddit_posts(seen_ids)
    if not posts:
        print("❌ No videos found.")
        return
    
    for i, (title, url, post_id) in enumerate(posts):
        print(f"\n--- Processing video {i+1}/{len(posts)} ---")
        safe_title = "".join(c if c.isalnum() else "_" for c in title[:40])
        base_name = f"{safe_title}"

        try:
            download_video(url, f"{base_name}.mp4")
            make_shorts_video(f"{base_name}.mp4", f"{base_name}.mp4")
            os.remove(f"{base_name}.mp4")
            print(f"✅ Saved: {base_name}.mp4")
            save_processed_id(post_id)
        except Exception as e:
            print(f"⚠️ Failed to process '{title}': {e}")
        time.sleep(2)  # delay to avoid hammering Reddit



if __name__ == "__main__":
    main()
