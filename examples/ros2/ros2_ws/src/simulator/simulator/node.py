import math

import rclpy
from geometry_msgs.msg import Pose, Twist
from pyquaternion import Quaternion
from rclpy.node import Node


class Simulator(Node):

    def __init__(self):
        super().__init__('simulator')
        self.pose_publisher_ = self.create_publisher(Pose, 'pose', 1)
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.on_steering, 1)
        self.pose = Pose()
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.step_size = 0.1
        self.timer = self.create_timer(self.step_size, self.update_pose)

    def on_steering(self, msg):
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z
        self.get_logger().info(f'linear: {self.linear_velocity}, angular: {self.angular_velocity}')

    def update_pose(self):
        quaternion = Quaternion(self.pose.orientation.w, self.pose.orientation.x,
                                self.pose.orientation.y, self.pose.orientation.z)
        theta = quaternion.yaw_pitch_roll[0]

        self.pose.position.x += self.linear_velocity * math.cos(theta) * self.step_size
        self.pose.position.y += self.linear_velocity * math.sin(theta) * self.step_size
        self.get_logger().info(f'x: {self.pose.position.x}, y: {self.pose.position.y}')
        theta += self.angular_velocity * self.step_size

        quaternion = Quaternion(axis=[0.0, 0.0, 1.0], radians=theta)
        self.pose.orientation.x = quaternion.x
        self.pose.orientation.y = quaternion.y
        self.pose.orientation.z = quaternion.z
        self.pose.orientation.w = quaternion.w

        self.pose_publisher_.publish(self.pose)


def main(args=None):
    rclpy.init(args=args)
    simulator = Simulator()
    rclpy.spin(simulator)
    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
