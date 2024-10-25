import rclpy
from rclpy.node import Node
from iqs_msgs.msg import Camera
from std_msgs.msg import String
from sensor_msgs.msg import Joy
from sled_msgs.msg import Currentpull
from std_srvs.srv import Empty
import threading
class MyNode(Node):
    def __init__(self):
       
        super().__init__('content_node')
        self.task_flag=threading.Event()
        self.camera_pubs=[self.create_publisher(Camera,f"Camera_{0}",10)]
        self.obs_pub=self.create_publisher(String,"obs_command_topic",10)
        self.joy_sub=self.create_subscription(Joy,"joy",self.joy_callback,10)
        self.timer=self.create_timer(.01,self.timer_callback)
        self.track_state_sub=self.create_subscription(Currentpull,"/track_state",self.track_state_callback,10)
        self.previous_track_state=99
        self.gopro_start_client=self.create_client(Empty,"Start_Recording_GoPro")
        self.gopro_stop_client=self.create_client(Empty,"Stop_Recording_GoPro")
        self.gopro_transfer_client=self.create_client(Empty,"Transfer_Footage")
        self.pull_task=0
        print("init thread")
        self.pull_thread=threading.Thread(target=self.pull_thread_func,daemon=True)
        self.pull_thread.start()
        print("init done")
        
    
    def timer_callback(self):
        pass

    def track_state_callback(self,msg):
        print(f"Track State {msg.trackstate} Previous {self.previous_track_state}")
        if msg.trackstate!=self.previous_track_state:
            if msg.trackstate!=1 and self.previous_track_state==1:
                self.pull_task=1
                self.task_flag.set()
            elif msg.trackstate==1:
                self.pull_task=2
                self.task_flag.set()
        self.previous_track_state=msg.trackstate
    
    def end_pull(self):
        pass

    def pull_thread_func(self):
        while True:
            self.task_flag.wait()
            if self.pull_task==1:
                print("Stopping")
                self.gopro_stop_client.call(Empty.Request())
                self.gopro_transfer_client.call(Empty.Request())
                scene=String()
                scene.data="replay"
                self.obs_pub.publish(scene)
            elif self.pull_task==2:
                print("Starting")
                self.gopro_start_client.call(Empty.Request())
            self.task_flag.clear()


    def joy_callback(self,msg):
        pan_cmd=msg.axes[0]*-12
        tilt_cmd=msg.axes[1]*12
        if msg.buttons[4]:
            pan_cmd=pan_cmd*2
            tilt_cmd=tilt_cmd*2
        zoom_cmd=msg.axes[4]
        cam_msg=Camera()
        cam_msg.control_mode=1
        cam_msg.pan_speed_cmd=pan_cmd
        cam_msg.tilt_speed_cmd=tilt_cmd
        cam_msg.zoom_speed_cmd=zoom_cmd
        self.camera_pubs[0].publish(cam_msg)

    
def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
