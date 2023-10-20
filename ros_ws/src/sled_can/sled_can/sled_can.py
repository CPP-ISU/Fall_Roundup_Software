#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sled_msgs.msg import Sled
from sled_msgs.msg import Currentpull
import can

class MyROSNode(Node):
    def __init__(self):
        super().__init__('my_ros_node')
        self.get_logger().info("My ROS 2 Node is running!")
        self.sled_pub = self.create_publisher(Sled,"sled",10)
        self.sled_timer=self.create_timer(.00001,self.callback_function)
        self.bus = can.Bus(channel='can0', interface='socketcan')
        self.current_pull_pub= self.create_publisher(Currentpull,"current_pull",10)

    def callback_function(self):
        message=self.bus.recv()
        if message.arbitration_id==0x0CFF6607:
            self.pull_state=message.data[0]
            self.distance=message.data[2]+message.data[3]<<8
            self.force=(message.data[4]+message.data[5]<<8)/10
            self.speed=message.data[6]+message.data[7]<<8
            sled=Sled()
            sled.force=self.force
            sled.distance=self.distance
            sled.speed=self.speed
            self.pull_state=message.data[0]
            self.sled_pub.publish(sled)
            current=Currentpull()
            current.trackstate=self.pull_state
            self.current_pull_pub.publish(current)

def main(args=None):
    rclpy.init(args=args)
    node = MyROSNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    # Clean up when the node is shut down
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
