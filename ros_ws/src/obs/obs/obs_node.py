#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
import time
from sled_msgs.msg import Currentpull
import obspython


class MyNode(Node):

    def __init__(self):
        super().__init__('my_node')
        self.track_state_sub = self.create_subscription(Currentpull,'track_state',self.track_state_callback,10)
        
        self.timer=self.create_timer(1,self.timer_callback)
        self.time=MyNode.get_clock().now().seconds
        self.obs_state=0

    
    def track_state_callback(self,msg):
        if self.track_state!=msg.trackstate:
            self.track_state=msg.trackstate
            self.time=MyNode.get_clock().now().seconds
    
    def timer_callback(self):
        if MyNode.get_clock().now().seconds-self.time >10 and self.track_state==2 and self.obs_state !=2:
            print("going to state 2")

    
        


def main(args=None):
    rclpy.init(args=args)
    node = MyNode()
    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
