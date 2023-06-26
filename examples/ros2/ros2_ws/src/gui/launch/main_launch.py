from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    return LaunchDescription([
        Node(
            package='gui',
            executable='nicegui_node',
            name='example_gui',
            output='screen',
        ),
        Node(
            package='simulator',
            executable='simulator_node',
            name='example_simulator',
            output='screen',
        ),
    ])
