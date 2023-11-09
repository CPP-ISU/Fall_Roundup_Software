import rclpy
from rclpy.node import Node
from your_package_name.srv import MyCustomSrv  # Replace with your service type

def main(args=None):
    rclpy.init(args=args)
    node = rclpy.create_node('service_client')
    client = node.create_client(MyCustomSrv, 'my_service')  # Match the service name

    while not client.wait_for_service(timeout_sec=1.0):
        node.get_logger().info('Service not available, waiting...')
    
    request = MyCustomSrv.Request()
    request.a = 5
    request.b = 3

    future = client.call(request)
    rclpy.spin_until_future_complete(node, future)

    if future.result() is not None:
        node.get_logger().info(f'Service response: sum={future.result().sum}')
    else:
        node.get_logger().error('Service call failed.')

    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()