import rclpy
from rclpy.node import Node
from std_msgs.msg import String
from std_srvs.srv import Empty
import logging
import asyncio
import simpleobsws

class ObsSubscriber(Node):
    def __init__(self):
        super().__init__('obs_subscriber')
        self.subscription = self.create_subscription(String, 'obs_command_topic', self.callback, 10)
        self.subscription  # prevent unused variable warning
        self.toggle_recording_ser=self.create_service(Empty,"obs_toggle_recording",self.toggle_recording_callback)
        logging.basicConfig(level=logging.DEBUG)
        self.parameters = simpleobsws.IdentificationParameters(ignoreNonFatalRequestChecks=False)
        self.ws = simpleobsws.WebSocketClient(url='ws://192.168.1.139:4455', password='TABIlBoUV2QyUwqb',
                                              identification_parameters=self.parameters)
        #asyncio.run(self.connect())
        self.loop=asyncio.new_event_loop()
        
        

    async def connect(self):
        await self.ws.connect()
        await self.ws.wait_until_identified()

    async def make_request(self, message):
        await self.ws.connect()
        await self.ws.wait_until_identified()
        request=simpleobsws.Request('SetCurrentProgramScene')
        request.requestData={"sceneName":message.data}
        #request = simpleobsws.Request(message.data)
        ret = await self.ws.call(request)
        print(f"returned {ret}")
        if ret.ok():
            self.get_logger().info("Request succeeded! Response data: {}".format(ret.responseData))
            results = ret.responseData

        await self.ws.disconnect()

    async def recording_request(self, message):
        await self.ws.connect()
        await self.ws.wait_until_identified()
        if message==1:
            request=simpleobsws.Request('ToggleRecord')
        else:
            request=simpleobsws.Request('StopRecording')
        request.requestData={}
        #request = simpleobsws.Request(message.data)
        ret = await self.ws.call(request)
        print(f"returned {ret}")
        if ret.ok():
            self.get_logger().info("Request succeeded! Response data: {}".format(ret.responseData))
            results = ret.responseData

        await self.ws.disconnect()

    def toggle_recording_callback(self,request,response):
        try:
            #self.get_logger().info("Received command: {}".format(msg.data))
            self.loop.run_until_complete(self.recording_request(1))
            
        except Exception as E:
            self.get_logger().info(f"Error: {E}")
        

        return response

    def callback(self, msg):
        try:
            self.get_logger().info("Received command: {}".format(msg.data))
            self.loop.run_until_complete(self.make_request(msg))
            
        except Exception as E:
            self.get_logger().info(f"Error: {E}")

def main(args=None):
    rclpy.init(args=args)
    obs_subscriber = ObsSubscriber()
    rclpy.spin(obs_subscriber)
    obs_subscriber.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
