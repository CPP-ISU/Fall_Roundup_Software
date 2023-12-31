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
        self.current_pull_pub= self.create_publisher(Currentpull,"track_state",10)

    def callback_function(self):
        message=self.bus.recv()
        #print(message.arbitration_id)
        if message.arbitration_id==0x0CFF6507:
            #print("msg")
            self.pull_state=message.data[0]
            self.distance=(message.data[2]|message.data[3]<<8)/12.0
            self.force=(message.data[4]|message.data[5]<<8)/10.0
            self.speed=((message.data[6]|message.data[7]<<8)/12.0)*0.681818
            sled=Sled()
            sled.header.stamp=self.get_clock().now().to_msg()
            sled.force=self.force
            sled.distance=self.distance
            sled.speed=self.speed
            self.pull_state=message.data[0]
            if self.pull_state==1:
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
