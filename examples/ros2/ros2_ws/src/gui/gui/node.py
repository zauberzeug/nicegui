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
        self.linear = 0.0
        self.angular = 0.0
        self.publisher_ = self.create_publisher(Twist, 'cmd_vel', 1)
        timer_period = 0.15  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.subscription = self.create_subscription(Pose, 'pose', self.on_pose, 1)

    def timer_callback(self) -> None:
        msg = Twist()
        msg.linear.x = float(self.linear)
        msg.angular.z = float(-self.angular)
        self.publisher_.publish(msg)

    def update_speeds(self, x, y) -> None:
        self.linear = x
        self.angular = y

    def on_pose(self, msg: Pose) -> None:
        print(f'pose: {msg}')


active_node: NiceGuiNode = None


def node_spin(node: Node) -> None:
    try:
        print('starting node')
        rclpy.spin(node)
    except ExternalShutdownException:
        print('stopped node')


@ui.page('/')
def index() -> None:
    with ui.row().classes('items-stretch'):
        with ui.card().classes('w-44'):
            ui.markdown('''
                ## Control

                Publish steering commands by dragging your mouse around in the blue field
            ''')
            ui.joystick(
                color='blue',
                size=50,
                on_move=lambda e: active_node.update_speeds(e.y, e.x),
                on_end=lambda _: active_node.update_speeds(0.0, 0.0),
            ).classes('my-joystick')
        with ui.card():
            ui.markdown('### Status')
            ui.label('linear speed')
            ui.label().bind_text_from(active_node, 'linear', backward=lambda value: f'{value:.3f}')
            ui.label('angular speed')
            ui.label().bind_text_from(active_node, 'angular', backward=lambda value: f'{value:.3f}')
        with ui.card().classes('w-96'):
            map = ui.html()


def main() -> None:
    pass  # NOTE: This is originally used as the ROS entry point, but we give the control of the node to NiceGUI.


def ros_main() -> None:
    global active_node
    rclpy.init()
    active_node = NiceGuiNode()
    threading.Thread(target=node_spin, args=(active_node,), daemon=True).start()


app.on_startup(lambda: threading.Thread(target=ros_main).start())
run.APP_IMPORT_STRING = f'{__name__}:app'
ui.run(uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))
