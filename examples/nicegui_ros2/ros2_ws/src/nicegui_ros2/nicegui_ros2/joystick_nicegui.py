import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from geometry_msgs.msg import Twist
import threading
from nicegui import ui, app, run
from pathlib import Path

class MinimalPublisher(Node):
    linear = 0.0
    angular = 0.0

    def __init__(self) -> None:
        super().__init__('turtlesim_joystick')
        self.publisher_ = self.create_publisher(Twist, 'turtle1/cmd_vel', 1)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

    def timer_callback(self) -> None:
        msg = Twist()
        self.get_logger().info('Publishing-> linear: "%f", angular: "%f"' % (self.linear, self.angular))
        msg.linear.x = float(self.linear)
        msg.angular.z = float(-self.angular)
        self.publisher_.publish(msg)

    @classmethod
    def update(cls, x, y) -> None:
        cls.linear = x
        cls.angular = y

def ros_main() -> None:
    print('Starting ROS2...', flush=True)
    rclpy.init()
    minimal_publisher_node = MinimalPublisher()
    try:
        rclpy.spin(minimal_publisher_node)
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
                field and drag your mouse around.<br><br>
                If your linar & angular values gets stuck, just <br>
                click once inside the joystick field.
            ''')

        with ui.card():
            ui.markdown('### Turtlebot3 Joystick')

            # NOTE: Joystick will be reworked in the future, so this is a temporary workaround for the size.
            ui.add_head_html('<style>.my-joystick > div { width: 20em !important; height: 20em !important; }</style>')
            ui.joystick(
                color='blue',
                size=50,
                on_move=lambda e: MinimalPublisher.update(e.y, e.x),
                on_end=lambda _: MinimalPublisher.update(0.0, 0.0),
            ).classes('my-joystick')

        with ui.card():
            ui.markdown('### Status')
            
            ui.label('linear speed')
            ui.label().bind_text_from(MinimalPublisher, 'linear', backward=lambda value: f'{value:.3f}')
            ui.label('angular speed')
            ui.label().bind_text_from(MinimalPublisher, 'angular', backward=lambda value: f'{value:.3f}')

def main() -> None:
    pass  # NOTE: This is originally used as the ROS entry point, but we give the control of the node to NiceGUI.

app.on_startup(lambda: threading.Thread(target=ros_main).start())
run.APP_IMPORT_STRING = f'{__name__}:app'
ui.run(port=8000, uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))