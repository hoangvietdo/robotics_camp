#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist

class RobotController(Node):
    def __init__(self):
        super().__init__("")
        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 5);
        self.get_logger().info("Controlling the robot to draw a circle using a feedforward controller")


def main():
    rclpy.init()
    robot_controller = RobotController()
    rclpy.spin(robot_controller)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
