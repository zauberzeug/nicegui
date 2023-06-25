import threading
from pathlib import Path

import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from nicegui import app, run, ui


class NiceGuiNode(Node):
    def __init__(self) -> None:
        super().__init__('nicegui')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.subscription = self.create_subscription(Pose, 'pose', self.on_pose, 1)

        @ui.page('/')
        def index() -> None:
            with ui.row().classes('items-stretch'):
                with ui.card().classes('w-44 text-center items-center'):
                    ui.label('Control').classes('text-2xl')
                    ui.joystick(
                        color='blue', size=50,
                        on_move=lambda e: self.send_speed(e.y, e.x),
                        on_end=lambda _: self.send_speed(0.0, 0.0),
                    )
                    ui.label('Publish steering commands by dragging your mouse around in the blue field')
                with ui.card().classes('w-44 text-center items-center'):
                    ui.label('Data').classes('text-2xl')
                    ui.label('linear speed')
                    ui.label().bind_text_from(self, 'linear', backward=lambda value: f'{value:.3f}')
                    ui.label('angular speed')
                    ui.label().bind_text_from(self, 'angular', backward=lambda value: f'{value:.3f}')
                with ui.card().classes('w-96 items-center'):
                    ui.label('Visualization').classes('text-2xl')
                    map = ui.html()

    def send_speed(self, x, y) -> None:
        msg = Twist()
        msg.linear.x = float(x)
        msg.angular.z = float(-y)
        self.cmd_vel_publisher.publish(msg)

    def on_pose(self, msg: Pose) -> None:
        print(f'pose: {msg}')


def node_spin(node: Node) -> None:
    try:
        print('starting node')
        rclpy.spin(node)
    except ExternalShutdownException:
        print('stopped node')


def main() -> None:
    pass  # NOTE: This is originally used as the ROS entry point, but we give the control of the node to NiceGUI.


def ros_main() -> None:
    rclpy.init()
    node = NiceGuiNode()
    threading.Thread(target=node_spin, args=(node,), daemon=True).start()


app.on_startup(lambda: threading.Thread(target=ros_main).start())
run.APP_IMPORT_STRING = f'{__name__}:app'
ui.run(uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))
