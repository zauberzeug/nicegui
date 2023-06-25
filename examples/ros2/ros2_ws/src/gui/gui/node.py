import threading
from pathlib import Path

import rclpy
from geometry_msgs.msg import Twist
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from nicegui import app, run, ui


class TurtleTwistNode(Node):
    def __init__(self) -> None:
        super().__init__('nicegui')
        self.linear = 0.0
        self.angular = 0.0
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 1)
        timer_period = 0.15  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self) -> None:
        msg = Twist()
        msg.linear.x = float(self.linear)
        msg.angular.z = float(-self.angular)
        self.publisher_.publish(msg)

    def update_speeds(self, x, y) -> None:
        self.linear = x
        self.angular = y


active_node: TurtleTwistNode = None


def node_spin(node: Node) -> None:
    try:
        rclpy.spin(node)
    except ExternalShutdownException:
        print('ROS2 was shutdown by NiceGUI.')


@ui.page('/')
def page() -> None:

    with ui.row().classes('items-stretch'):
        with ui.card():
            ui.markdown('''
                ## Guide

                This is a simple virtual joystick <br>
                that sends twist commands to turtlesim.<br><br>
                To control the turtle, just klick inside the blue <br>
                field and drag your mouse around.
            ''')

        with ui.card():
            ui.markdown('### Turtlesim Joystick')

            # NOTE: Joystick will be reworked in the future, so this is a temporary workaround for the size.
            ui.add_head_html('<style>.my-joystick > div { width: 20em !important; height: 20em !important; }</style>')
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


def main() -> None:
    pass  # NOTE: This is originally used as the ROS entry point, but we give the control of the node to NiceGUI.


def ros_main() -> None:
    global active_node
    rclpy.init()
    active_node = TurtleTwistNode()
    threading.Thread(target=node_spin, args=(active_node,), daemon=True).start()


app.on_startup(lambda: threading.Thread(target=ros_main).start())
run.APP_IMPORT_STRING = f'{__name__}:app'
ui.run(uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))
