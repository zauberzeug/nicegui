import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.node import Node


class Simulator(Node):

    def __init__(self):
        super().__init__('simulator')
        self.pose_publisher_ = self.create_publisher(Pose, 'pose', 1)
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.on_steering, 1)
        self.pose = Pose()

    def on_steering(self, msg):
        self.pose.position.x += msg.linear.x
        self.pose.orientation.z += msg.angular.z
        self.pose_publisher_.publish(self.pose)


def main(args=None):
    rclpy.init(args=args)
    simulator = Simulator()
    rclpy.spin(simulator)
    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
