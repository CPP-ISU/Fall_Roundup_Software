import rclpy
from rclpy.node import Node
from sled_msgs.msg import Sled
import time
class YourNode(Node):
    def __init__(self):
        super().__init__('your_node')
        self.get_logger().info("Your ROS 2 Node is running!")
        self.pull_pub=self.create_publisher(Sled,'sled',10)
        self.pub_timer=self.create_timer(1,self.timer_callback)
        self.i=0.0

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