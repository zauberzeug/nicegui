import math

import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.node import Node


class Simulator(Node):
    INTERVAL = 0.1

    def __init__(self) -> None:
        super().__init__('simulator')
        self.pose_publisher_ = self.create_publisher(Pose, 'pose', 1)
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.handle_velocity_command, 1)
        self.pose = Pose()
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.timer = self.create_timer(self.INTERVAL, self.update_pose)

    def handle_velocity_command(self, msg: Twist) -> None:
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    def update_pose(self) -> None:
        yaw = 2 * math.atan2(self.pose.orientation.z, self.pose.orientation.w)
        self.pose.position.x += self.linear_velocity * math.cos(yaw) * self.INTERVAL
        self.pose.position.y += self.linear_velocity * math.sin(yaw) * self.INTERVAL
        yaw += self.angular_velocity * self.INTERVAL
        self.pose.orientation.z = math.sin(yaw / 2)
        self.pose.orientation.w = math.cos(yaw / 2)
        self.pose_publisher_.publish(self.pose)


def main(args=None) -> None:
    rclpy.init(args=args)
    simulator = Simulator()
    rclpy.spin(simulator)
    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
