import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node
from std_msgs.msg import String
import threading
from nicegui import ui, app, run
from pathlib import Path



class MinimalPublisher(Node):
    """This is a minimal publisher example from the ROS2 tutorials integrated with NiceGUI.

    https://docs.ros.org/en/humble/Tutorials/Beginner-Client-Libraries/Writing-A-Simple-Py-Publisher-And-Subscriber.html
    """

    def __init__(self) -> None:
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'topic', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

    def timer_callback(self) -> None:
        msg = String()
        msg.data = 'Hello World: %d' % self.i
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


def ros_main() -> None:
    print('Starting ROS2...', flush=True)
    rclpy.init()
    minimal_publisher_node = MinimalPublisher()
    try:
        rclpy.spin(minimal_publisher_node)
    except ExternalShutdownException:
        print('ROS2 was shutdown by NiceGUI.')

@ui.page('/')
def page():
    ui.label('Hello NiceGUI!')

def main():
    pass # NOTE: This is originally used as the ROS entry point, but we give the controll of the node to NiceGUI.

app.on_startup(lambda: threading.Thread(target=ros_main).start())
run.APP_IMPORT_STRING = f'{__name__}:app'
ui.run(port=8000, uvicorn_reload_dirs=str(Path(__file__).parent.resolve()))
