import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.node import Node


class Simulator(Node):

    def __init__(self):
        super().__init__('simple_simulator')
        self.pose_publisher_ = self.create_publisher(Pose, 'pose', 10)
        self.subscription = self.create_subscription(
            Twist,
            'cmd_vel',
            self.listener_callback,
            10)

    def listener_callback(self, msg):
        pose = Pose()
        pose.position.x += msg.linear.x
        pose.position.y += 0
        pose.orientation.z += msg.angular.z
        self.pose_publisher_.publish(pose)


def main(args=None):
    rclpy.init(args=args)
    simulator = Simulator()
    rclpy.spin(simulator)
    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
