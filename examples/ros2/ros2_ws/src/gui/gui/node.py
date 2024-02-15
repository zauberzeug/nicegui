import math
import threading
from pathlib import Path

import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from nicegui import Client, app, ui, ui_run


class NiceGuiNode(Node):
    """
    A ROS2 node for controlling a GUI interface.

    This node provides a graphical user interface (GUI) for controlling a robot's movement
    and visualizing its position in a 3D scene. It subscribes to the 'pose' topic to receive
    the robot's position and orientation information, and publishes velocity commands to the
    'cmd_vel' topic to control the robot's movement.

    The GUI consists of three main components:
    - Control: A joystick for controlling the robot's movement. The user can drag the joystick
      in the blue field to specify the linear and angular velocities of the robot.
    - Data: Sliders for adjusting the linear and angular velocities of the robot. The current
      position of the robot is also displayed.
    - Visualization: A 3D scene that visualizes the robot's position. The robot is represented
      as a prism shape that moves and rotates according to the received pose information.

    Usage:
    1. Create an instance of NiceGuiNode.
    2. Spin the node to start processing ROS2 messages.
    3. Interact with the GUI to control the robot's movement and visualize its position.

    Example:
    ```python
    from nicegui.examples.ros2.ros2_ws.src.gui.gui.node import NiceGuiNode

    def main():
        node = NiceGuiNode()
        node.spin()

    if __name__ == '__main__':
        main()
    ```
    """

    def __init__(self) -> None:
        super().__init__('nicegui')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.subscription = self.create_subscription(Pose, 'pose', self.handle_pose, 1)

        with Client.auto_index_client:
            with ui.row().classes('items-stretch'):
                with ui.card().classes('w-44 text-center items-center'):
                    ui.label('Control').classes('text-2xl')
                    ui.joystick(color='blue', size=50,
                                on_move=lambda e: self.send_speed(float(e.y), float(e.x)),
                                on_end=lambda _: self.send_speed(0.0, 0.0))
                    ui.label('Publish steering commands by dragging your mouse around in the blue field').classes('mt-6')
                with ui.card().classes('w-44 text-center items-center'):
                    ui.label('Data').classes('text-2xl')
                    ui.label('linear velocity').classes('text-xs mb-[-1.8em]')
                    slider_props = 'readonly selection-color=transparent'
                    self.linear = ui.slider(min=-1, max=1, step=0.05, value=0).props(slider_props)
                    ui.label('angular velocity').classes('text-xs mb-[-1.8em]')
                    self.angular = ui.slider(min=-1, max=1, step=0.05, value=0).props(slider_props)
                    ui.label('position').classes('text-xs mb-[-1.4em]')
                    self.position = ui.label('---')
                with ui.card().classes('w-96 h-96 items-center'):
                    ui.label('Visualization').classes('text-2xl')
                    with ui.scene(350, 300) as scene:
                        with scene.group() as self.robot_3d:
                            prism = [[-0.5, -0.5], [0.5, -0.5], [0.75, 0], [0.5, 0.5], [-0.5, 0.5]]
                            self.robot_object = scene.extrusion(prism, 0.4).material('#4488ff', 0.5)

    def send_speed(self, x: float, y: float) -> None:
        """
        Publishes the linear and angular velocities of the robot.

        Args:
            x (float): The linear velocity of the robot.
            y (float): The angular velocity of the robot.
        """
        msg = Twist()
        msg.linear.x = x
        msg.angular.z = -y
        self.linear.value = x
        self.angular.value = y
        self.cmd_vel_publisher.publish(msg)

    def handle_pose(self, msg: Pose) -> None:
        """
        Handles the received pose message.

        Updates the position label and moves/rotates the 3D robot object in the scene.

        Args:
            msg (Pose): The received pose message.
        """
        self.position.text = f'x: {msg.position.x:.2f}, y: {msg.position.y:.2f}'
        self.robot_3d.move(msg.position.x, msg.position.y)
        self.robot_3d.rotate(0, 0, 2 * math.atan2(msg.orientation.z, msg.orientation.w))


def main() -> None:
    """
    This is the main function of the GUI node.

    It serves as the entry point for the ROS2 system and is called by the setup.py file.
    However, in this implementation, the function is left empty to allow for NiceGUI auto-reloading.

    Usage:
    - This function is automatically called by the ROS2 system.
    - It should not be called directly from other parts of the code.

    Note:
    - The function is intentionally left empty to enable NiceGUI auto-reloading.
    """
    pass


def ros_main() -> None:
    """
    Entry point for the ROS node.

    This function initializes the ROS client library, creates a NiceGuiNode instance,
    and starts spinning the node to process incoming messages.

    Raises:
        ExternalShutdownException: If an external shutdown signal is received.

    Usage:
        Call this function to start the ROS node and begin processing messages.

    Example:
        ros_main()
    """
    rclpy.init()
    node = NiceGuiNode()
    try:
        rclpy.spin(node)
    except ExternalShutdownException:
        pass


app.on_startup(lambda: threading.Thread(target=ros_main).start())
ui_run.APP_IMPORT_STRING = f'{__name__}:app'  # ROS2 uses a non-standard module name, so we need to specify it here
ui.run(uvicorn_reload_dirs=str(Path(__file__).parent.resolve()), favicon='🤖')
