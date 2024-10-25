import rclpy
from rclpy.node import Node
from iqs_msgs.msg import Camera
from std_msgs.msg import String
from sensor_msgs.msg import Joy
import os
import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors
import googleapiclient.http
import json
import time
import mysql.connector
import datetime
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


SQL_IP="localhost"
SQL_USER="software"
SQL_PASSWORD="D@rkcyde15"

class MyNode(Node):
    def __init__(self):
       
        super().__init__('youtube_uploader')

        self.camera_pubs=[self.create_publisher(Camera,f"Camera_{0}",10)]
        self.obs_pub=self.create_publisher(String,"obs_scene",10)
        self.joy_sub=self.create_subscription(Joy,"joy",self.joy_callback,10)
        self.timer=self.create_timer(10,self.track_state_callback)
        self.youtube= get_authenticated_service()
        self.teams={}
        self.tractors={}
        localdb = mysql.connector.connect(
            host=SQL_IP,
            user=SQL_USER,
            password=SQL_PASSWORD,
            database='fall_roundup'
            )
        localcursor=localdb.cursor()
        sql=f"SELECT team_id, team_name FROM teams"
        localcursor.execute(sql)
        results=localcursor.fetchall()
        for result in results:
            team_id,team_name=result
            self.teams[team_id]=team_name

        sql=f"SELECT tractor_id, tractor_num, tractor_name FROM tractors"
        localcursor.execute(sql)
        results=localcursor.fetchall()
        for result in results:
            tractor_id,tractor_num,tractor_name=result
            self.tractors[tractor_id]={"name":tractor_name,"number":tractor_num}
        


    def timer_callback(self):
        pass

    def track_state_callback(self):
        print("Track State Callback")
        files=os.listdir("videos/new")
        if len(files)==0:
            return

        localdb = mysql.connector.connect(
            host=SQL_IP,
            user=SQL_USER,
            password=SQL_PASSWORD,
            database='fall_roundup'
            )
        localcursor=localdb.cursor()

        for file in files:
            dt=file.split(" ")
            date_ar=dt[0].split("-")
            time_ar=dt[1].split("-")
            secs=time_ar[2][:-4]
            print(date_ar)
            print(time_ar)
            epoch_vid=datetime.datetime(int(date_ar[0]),int(date_ar[1]),int(date_ar[2]),int(time_ar[0]),int(time_ar[1]),int(secs)).timestamp()
            print(epoch_vid)
            sql=f"SELECT pull_id, team_id, tractor_id FROM all_pull_results WHERE start_time < {epoch_vid+10} AND end_time > {epoch_vid}"
            localcursor.execute(sql)
            results=localcursor.fetchone()
            if results is not None:
                pull_id,team_id,tractor_id=results

                title=f"2024 Fall Roundup {self.teams[team_id]} {self.tractors[tractor_id]['number']}{self.tractors[tractor_id]['name']} pull"
                print(title)
                full_file=f"videos/new/{file}"
                upload_video(self.youtube,full_file,title,"",[])
                os.rename(full_file,f"videos/old/raw/{file}")
                

        
        

        

    def joy_callback(self,msg):
        pass
    
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
