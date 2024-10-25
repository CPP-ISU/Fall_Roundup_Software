import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import json
import time

# API credentials and scopes
CLIENT_SECRETS_FILE = "client_secrets.json"
SCOPES = ["https://www.googleapis.com/auth/youtube.upload",
          "https://www.googleapis.com/auth/youtube.force-ssl"]

# Get the authenticated API client
def get_authenticated_service():
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_local_server(port=0)
    return googleapiclient.discovery.build("youtube", "v3", credentials=credentials)

# Upload video to YouTube
def upload_video(youtube, video_file, title, description, tags, category_id="22", privacy_status="unlisted"):
    body = {
        'snippet': {
            'title': title,
            'description': description,
            'tags': tags,
            'categoryId': category_id
        },
        'status': {
            'privacyStatus': privacy_status
        }
    }

    request = youtube.videos().insert(
        part="snippet,status",
        body=body,
        media_body=googleapiclient.http.MediaFileUpload(video_file, chunksize=-1, resumable=True)
    )

    response = None
    while response is None:
        status, response = request.next_chunk()
        if 'id' in response:
            print(f"Video uploaded successfully, Video ID: {response['id']}")
        else:
            print(f"Upload failed with response: {response}")
    return response['id']

# Add video to playlist
def add_video_to_playlist(youtube, video_id, playlist_id):
    request = youtube.playlistItems().insert(
        part="snippet",
        body={
            'snippet': {
                'playlistId': playlist_id,
                'resourceId': {
                    'kind': 'youtube#video',
                    'videoId': video_id
                }
            }
        }
    )
    response = request.execute()
    print(f"Video added to playlist, Playlist Item ID: {response['id']}")
    return response

if __name__ == "__main__":
    youtube = get_authenticated_service()

    # Set your video and playlist details
    video_file = "2024-10-16 23-01-41.mkv"  # path to the video file
    title = "Your Video Title"
    description = "Your Video Description"
    tags = ["tag1", "tag2"]
    playlist_id = "YOUR_PLAYLIST_ID"  # YouTube Playlist ID

    # Step 1: Upload the video
    video_id = upload_video(youtube, video_file, title, description, tags)

    # Step 2: Add the video to the playlist
    time.sleep(5)  # Just to ensure video is processed before adding to playlist
    #add_video_to_playlist(youtube, video_id, playlist_id)
