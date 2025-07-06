import os
import schedule
import time
from upload_to_yt import upload_video

VIDEO_FOLDER = "vids"
LOG_FILE = "log.txt"

def load_uploaded():
    if not os.path.exists(LOG_FILE):
        return set()
    with open(LOG_FILE, "r") as f:
        return set(line.strip() for line in f)
    
def mark_uploaded(filename):
    with open(LOG_FILE, "a") as f:
        f.write(filename + "\n")

def upload_next_vid():
    uploaded = load_uploaded()
    videos = [f for f in os.listdir(VIDEO_FOLDER) if f.endswith(".mp4") and f not in uploaded]
    if not videos:
        print("No videos currently to uploaded. Check vids directory")
        return
    
    video_file = videos[0]
    title = os.path.splitext(video_file)[0].replace("_", " ").capitalize()
    upload_video()
    mark_uploaded(video_file)