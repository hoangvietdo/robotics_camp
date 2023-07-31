#!/usr/bin/env python3

import rclpy
import math

from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty


class RobotController(Node):
    def __init__(self):
        super().__init__("feed_back_circle")

        self.t = 0.0
        self.reset = 0.0

        self.cmd_vel_pub_ = self.create_publisher(Twist, "/turtle1/cmd_vel", 5);
        self.reset_client_ = self.create_client(Empty, "/reset")
        self.clear_client_ = self.create_client(Empty, "/clear")

        self.request_ = Empty.Request()
        
        self.timer_ = self.create_timer(0.05, self.send_command)
        self.get_logger().info("Controlling the robot to draw a circle using a feedforward controller")
    
    def send_command(self):
        a = 5.0
        b = 0.7
        msg = Twist()

        if self.t == 0.0 and self.reset == 0.0:
            self.get_logger().info("Clearing and resetting turtlesim")
            self.clear_client_.call_async(self.request_)
            self.reset_client_.call_async(self.request_)
            self.reset = 1.0
        else:
            pass

        ## TODO
        ## - Add keyboard to control (press s) or stop the robot (press 'Space')

        if self.t >= 5.0:
            x_d = -a * b * math.sin(b * self.t)
            y_d = a * b * math.cos(b * self.t)
            x_dd = -a * b * b * math.cos(b * self.t)
            y_dd = -a * b * b * math.sin(b * self.t)
            msg.linear.x = math.sqrt(math.pow(x_d, 2) + math.pow(y_d, 2))
            msg.angular.z = (y_dd * x_d - y_d * x_dd) / msg.linear.x
            self.cmd_vel_pub_.publish(msg)
            self.t = self.t + 0.05
        else:
            msg.linear.x = 0.0
            msg.angular.z = 0.0
            self.cmd_vel_pub_.publish(msg)
            self.t = self.t + 0.05

def main():
    rclpy.init()
    robot_controller = RobotController()
    rclpy.spin(robot_controller)
    robot_controller.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()
