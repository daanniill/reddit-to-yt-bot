import os
import schedule
import time
import emoji
from upload_to_yt import upload_video

VIDEO_FOLDER = "vids"
LOG_FILE = "log.txt"

def format_title(title):
    short_title = title.strip().capitalize()
    return f"{short_title} 😂 #Shorts"

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
    title = format_title(os.path.splitext(video_file)[0].replace("_", " ").capitalize())
    upload_video(os.path.join(VIDEO_FOLDER, video_file), title=title)
    mark_uploaded(video_file)

    schedule.every().day.at("10:00").do(upload_next_vid)
    schedule.every().day.at("15:00").do(upload_next_vid)
    schedule.every().day.at("20:00").do(upload_next_vid)

print("Upload scheduler started...")
while True:
    schedule.run_pending()
    time.sleep(30)