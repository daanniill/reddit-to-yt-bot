import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
from googleapiclient.http import MediaFileUpload
import pickle

SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    credentials = None
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)

    if not credentials or not credentials.valid:
        flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
            "client_secrets.json", SCOPES)
        credentials = flow.run_console()
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

def upload_video(file, title, description, tags=None, privacy="private"):
    youtube = authenticate_youtube()

    request_body = {
        "snippet": {
            "title": title,
            "description": description,
            "tags": tags or ["reddit", "shorts", "viral"],
            "categoryId": "29"  # Comedy
        },
        "status": {
            "privacyStatus": privacy,
            "madeForKids": False
        }
    }

    media = MediaFileUpload(file, mimetype="video/mp4", resumable=True)

    request = youtube.videos().insert(
        part="snippet,status",
        body=request_body,
        media_body=media
    )

    response = request.execute()
    print("✅ Uploaded: https://www.youtube.com/watch?v=" + response['id'])