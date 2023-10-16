import rclpy
from rclpy.node import Node
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
from rclpy.serialization import serialize_message
import time
import csv
class YourNode(Node):
    def __init__(self):
        super().__init__('your_node')
        self.get_logger().info("Your ROS 2 Node is running!")
        self.pull_pub=self.create_publisher(Sled,'sled',10)
        self.track_sub=self.create_subscription(Currentpull, 'track_state',self.trackstate_callback,10)
        self.pull_id_sub=self.create_subscription(Currentpull, 'current_pull',self.current_pull_callback,10)
        self.sled_sub = self.create_subscription(Sled, 'sled', self.sled_callback, 10)
        
        self.i=0.0
        self.current_pullid=0
        self.track_state=0
        
        self.pull_active=False
        
    
    def sled_callback(self,msg):
        
        if self.pull_active:
            row=[msg.distance,msg.force,msg.speed]
            for data in msg.data:
                row.append(data)
            self.writer.writerow(row)
            
    
    def current_pull_callback(self,msg):
        print("current pull callback")
        self.current_pullid=msg.pullid
    
    def trackstate_callback(self,msg):
        self.track_state=msg.trackstate
        print(self.track_state)
        if self.track_state==1 and self.pull_active==False:
            self.csv=open(f"{self.current_pullid}",mode='w',newline='')
            self.writer=csv.writer(self.csv)
            self.pull_active=True
            print(f"opened csv for pull {self.current_pullid}")
        
        if self.track_state!=1 and self.pull_active:
            self.csv.flush()
            self.csv.close()
            self.pull_active=False
            print(f"closed csv for pull {self.current_pullid}")


            






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