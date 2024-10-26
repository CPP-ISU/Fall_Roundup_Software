from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    # Define the first node
    node1 = Node(
        package='sled_display',  # Replace with the package name of your first node
        executable='sled_display',  # Replace with the executable name of your first node
        name='sled',  # Name for this node instance
        output='screen'  # Outputs the log to the screen
    )

    # Define the second node
    node2 = Node(
        package='sled_can',  # Replace with the package name of your second node
        executable='sled_can',  # Replace with the executable name of your second node
        name='Sled_Can',  # Name for this node instance
        output='screen'  # Outputs the log to the screen
    )

    # Return the launch description with both nodes
    return LaunchDescription([node1, node2])
