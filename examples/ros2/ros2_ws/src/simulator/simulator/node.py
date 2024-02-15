import math

import rclpy
from geometry_msgs.msg import Pose, Twist
from rclpy.node import Node


class Simulator(Node):
    INTERVAL = 0.1

    def __init__(self) -> None:
        """
        Initializes the Simulator class.

        This class represents a simulator node in a ROS2 system. It creates a publisher for the 'pose' topic
        and a subscription for the 'cmd_vel' topic. It also initializes the pose, linear velocity, angular velocity,
        and a timer for updating the pose.

        Args:
            None

        Returns:
            None
        """
        super().__init__('simulator')
        self.pose_publisher_ = self.create_publisher(Pose, 'pose', 1)
        self.subscription = self.create_subscription(Twist, 'cmd_vel', self.handle_velocity_command, 1)
        self.pose = Pose()
        self.linear_velocity = 0.0
        self.angular_velocity = 0.0
        self.timer = self.create_timer(self.INTERVAL, self.update_pose)

    def handle_velocity_command(self, msg: Twist) -> None:
        """
        Handles the velocity command received from the 'cmd_vel' topic.

        This method is called whenever a new Twist message is received on the 'cmd_vel' topic. It updates the
        linear velocity and angular velocity based on the received message.

        Args:
            msg (Twist): The Twist message containing the linear and angular velocities.

        Returns:
            None
        """
        self.linear_velocity = msg.linear.x
        self.angular_velocity = msg.angular.z

    def update_pose(self) -> None:
        """
        Updates the pose of the simulator.

        This method is called periodically by the timer. It updates the pose of the simulator based on the
        current linear and angular velocities. The updated pose is then published on the 'pose' topic.

        Args:
            None

        Returns:
            None
        """
        yaw = 2 * math.atan2(self.pose.orientation.z, self.pose.orientation.w)
        self.pose.position.x += self.linear_velocity * math.cos(yaw) * self.INTERVAL
        self.pose.position.y += self.linear_velocity * math.sin(yaw) * self.INTERVAL
        yaw += self.angular_velocity * self.INTERVAL
        self.pose.orientation.z = math.sin(yaw / 2)
        self.pose.orientation.w = math.cos(yaw / 2)
        self.pose_publisher_.publish(self.pose)


def main(args=None) -> None:
    """
    Entry point of the simulator node.

    Args:
        args (List[str], optional): Command-line arguments. Defaults to None.

    Returns:
        None
    """
    rclpy.init(args=args)
    simulator = Simulator()
    rclpy.spin(simulator)
    simulator.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
