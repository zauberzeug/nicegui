from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    """
    Generate the launch description for the GUI and simulator nodes.

    This function creates a LaunchDescription object that contains the necessary configuration
    for launching the GUI and simulator nodes. The GUI node is launched with the 'nicegui_node'
    executable from the 'gui' package, while the simulator node is launched with the 'simulator_node'
    executable from the 'simulator' package.

    Returns:
        A LaunchDescription object containing the configuration for launching the GUI and simulator nodes.
    """
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
