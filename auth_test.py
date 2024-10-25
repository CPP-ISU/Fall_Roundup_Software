import os
import google_auth_oauthlib.flow
import googleapiclient.discovery

# Set up credentials and API scopes
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload"]

def authenticate_youtube():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    youtube = googleapiclient.discovery.build("youtube", "v3", credentials=credentials)
    return youtube

if __name__ == "__main__":
    youtube_service = authenticate_youtube()
    print("YouTube API authenticated successfully!")
