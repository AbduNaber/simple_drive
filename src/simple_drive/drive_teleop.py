#!/usr/bin/python

import rospy
import subprocess

from sensor_msgs.msg import Joy
from geometry_msgs.msg import Twist
from actionlib_msgs.msg import GoalID

class DriveTeleop:
    def __init__(self):
        self.speed_setting = 2  # default to medium speed

        self.cmd_vel_pub = rospy.Publisher("teleop/cmd_vel", Twist, queue_size=1)
        self.goal_cancel_pub = rospy.Publisher("move_base/cancel", GoalID, queue_size=1)
        self.joy_sub = rospy.Subscriber("joy", Joy, self.on_joy)

    def on_joy(self, data):
        # Set speed ratio using d-pad
        if data.axes[7] == 1:  # full speed (d-pad up)
            self.speed_setting = 1
        elif data.axes[6] != 0:  # medium speed (d-pad left or right)
            self.speed_setting = 2
        elif data.axes[7] == -1:  # low speed (d-pad down)
            self.speed_setting = 3

        # Left stick for forward and backward movement
        linear_vel = data.axes[1] / self.speed_setting  # (m/s)

        # Right stick for turning
        angular_vel = data.axes[3] / self.speed_setting  # (rad/s)

        # Publish Twist
        twist = Twist()
        twist.linear.x = linear_vel
        twist.angular.z = angular_vel
        self.cmd_vel_pub.publish(twist)

        # Cancel move base goal
        if data.buttons[2]:  # X button
            rospy.loginfo('Cancelling move_base goal')
            cancel_msg = GoalID()
            self.goal_cancel_pub.publish(cancel_msg)

def main():
    rospy.init_node("drive_teleop")
    controller = DriveTeleop()
    rospy.spin()

if __name__ == '__main__':
    main()

