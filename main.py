import praw
import os
import yt_dlp
import moviepy as mp
from moviepy import VideoFileClip
from dotenv import load_dotenv

load_dotenv()

def get_reddit_post():
    reddit = praw.Reddit(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET"),
        user_agent=os.getenv("USER_AGENT")
    )
    print(reddit.read_only)  # Should print: True

    sub = reddit.subreddit("MemeVideos")
    for post in sub.hot(limit=20):
        if 'v.redd.it' in post.url:
            return post.title, post.url
    return None, None

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

def make_shorts_video(video_path, title, output_filename=None):
    if output_filename is None:
        safe_title = "".join(c if c.isalnum() else "_" for c in title[:30])
        output_filename = f"{safe_title}.mp4"

    video = VideoFileClip(video_path)
    # Resizing vid to 720x1280 while perserving aspect ratio
    video = video.resized(height=1280)
    video = video.cropped(width=720, x_center=video.w/2)

    final = mp.CompositeVideoClip([video])
    final.write_videofile(output_filename, fps=30)
    return output_filename

def main():
    print("[1] Searching for Reddit video...")
    title, url = get_reddit_post()
    if not url:
        print("❌ No video found.")
        return

    print(f"[2] Downloading video: {title}")
    download_video(url, "video.mp4")

    print("[3] Creating Shorts video...")
    final_file = make_shorts_video("video.mp4", title)

    print("✅ Done! Output: short_final.mp4")

if __name__ == "__main__":
    main()
