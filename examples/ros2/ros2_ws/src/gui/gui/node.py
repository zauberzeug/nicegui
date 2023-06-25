import threading
from dataclasses import dataclass
from pathlib import Path

import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from nicegui import app, run, ui


@dataclass(kw_only=True)
class User():
    linear: ui.slider = None
    angular: ui.slider = None
    position: ui.label = None
    map: ui.html = None


class NiceGuiNode(Node):
    def __init__(self) -> None:
        super().__init__('nicegui')
        self.cmd_vel_publisher = self.create_publisher(Twist, 'cmd_vel', 1)
        self.subscription = self.create_subscription(Pose, 'pose', self.on_pose, 1)
        self.users = []

        @ui.page('/')
        def index() -> None:
            user = User()
            with ui.row().classes('items-stretch'):
                with ui.card().classes('w-44 text-center items-center'):
                    ui.label('Control').classes('text-2xl')
                    ui.joystick(
                        color='blue', size=50,
                        on_move=lambda e: self.send_speed(float(e.y), float(e.x)),
                        on_end=lambda _: self.send_speed(0.0, 0.0),
                    )
                    ui.label('Publish steering commands by dragging your mouse around in the blue field')
                with ui.card().classes('w-44 text-center items-center'):
                    ui.label('Data').classes('text-2xl')
                    ui.label('linear velocity').classes('text-xs mb-[-1.8em]')
                    slider_props = 'readonly selection-color="transparent"'
                    user.linear = ui.slider(min=-1, max=1, step=0.05, value=0).props(slider_props)
                    ui.label('angular velocity').classes('text-xs mb-[-1.8em]')
                    user.angular = ui.slider(min=-1, max=1, step=0.05, value=0).props(slider_props)
                    ui.label('position').classes('text-xs mt-8 mb-[-1.4em]')
                    user.position = ui.label('x: 0.0, y: 0.0')
                with ui.card().classes('w-96 h-96 items-center'):
                    ui.label('Visualization').classes('text-2xl')
                    user.map = ui.html()
            self.users.append(user)

    def send_speed(self, x, y) -> None:
        msg = Twist()
        msg.linear.x = x
        msg.angular.z = -y
        for user in self.users:
            user.linear.value = x
            user.angular.value = y
        self.cmd_vel_publisher.publish(msg)

    def on_pose(self, msg: Pose) -> None:
        for user in self.users:
            user.position.text = f'x: {msg.position.x:.2f}, y: {msg.position.y:.2f}'
            user.map.content = f'''
            <svg width="100%" height="100%" viewBox="-20 -20 40 40">
                <circle cx="{msg.position.x}" cy="{msg.position.y}" r="1" fill="red" />
            </svg>'''


def node_spin(node: Node) -> None:
    try:
        print(f'starting node', flush=True)
        rclpy.spin(node)
    except ExternalShutdownException:
        print(f'stopped node', flush=True)


def main() -> None:
    pass  # NOTE: This is originally used as the ROS entry point, but we give the control of the node to NiceGUI.


def ros_main() -> None:
    rclpy.init()
    node = NiceGuiNode()
    threading.Thread(target=node_spin, args=(node,), daemon=True).start()


app.on_startup(lambda: threading.Thread(target=ros_main).start())
run.APP_IMPORT_STRING = f'{__name__}:app'
ui.run(uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))
