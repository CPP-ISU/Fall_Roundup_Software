import rclpy
from rclpy.node import Node
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
import time
import rosbag2_py
class YourNode(Node):
    def __init__(self):
        super().__init__('your_node')
        self.get_logger().info("Your ROS 2 Node is running!")
        self.pull_sub=self.create_subscription(Sled,'sled',self.sled_callback,10)
        self.track_sub=self.create_subscription(Currentpull, 'track_state',self.track_state,10)
        self.pull_id_sub=self.create_subscription(Currentpull, 'pull_id',self.current_pull_callback,10)
        self.pub_timer=self.create_timer(1,self.timer_callback)
        self
        self.i=0.0
        self.current_pullid=0
        self.track_state=0
        self.writer=rosbag2_py.SequentialWriter()
        self.pull_active=False
        

    def timer_callback(self):
        sled=Sled()
        sled.speed=((self.i-100)/38)**2+7
        sled.distance=self.i
        self.i+=sled.speed*1.46667/1
        if self.i>200:
            self.i=0.0
            sled.distance=0.0
            self.pull_pub.publish(sled)
            time.sleep(10)
        self.pull_pub.publish(sled)
    
    def sled_callback(self):
        print("Sled callback")
    
    def current_pull_callback(self,msg):
        print("current pull callback")
        self.current_pullid=msg.pullid
    
    def trackstate_callback(self,msg):
        self.track_state=msg.trackstate
        if self.track_state==1 and self.pull_active==False:
            self.storage_options=rosbag2_py.StorageOptions(
                uri=f"pull{self.current_pullid}",
                storage_id='splite3'
            )
            self.converter_options=rosbag2_py.ConverterOptions('','')
            self.writer.open(self.storage_options,self.converter_options)
            




def main(args=None):
    rclpy.init(args=args)
    node = YourNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()