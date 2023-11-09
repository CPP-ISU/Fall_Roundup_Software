import rclpy
from rclpy.node import Node
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull

class YourNode(Node):
    def __init__(self):
        super().__init__('echo_node')
        self.get_logger().info("Your ROS 2 Node is running!")
        self.track_sub=self.create_subscription(Currentpull, 'track_state',self.trackstate_callback,10)
        self.current_sub=self.create_subscription(Currentpull, "current_pull",self.current_pull_callback,10)
        self.sled_sub=self.create_subscription(Sled, "sled",self.sled_callback,10)

        self.current_pub=self.create_publisher(Currentpull, "current_pull_echo",10)
        self.track_pub=self.create_publisher(Currentpull, "track_state_echo",10)
        self.sled_pub=self.create_publisher(Sled,"sled_echo",10)
        

    def current_pull_callback(self,msg):
        self.current_pub.publish(msg)
    
    def trackstate_callback(self,msg):
        self.track_pub.publish(msg)
    
    def sled_callback(self,msg):
        self.sled_pub.publish(msg)
    





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