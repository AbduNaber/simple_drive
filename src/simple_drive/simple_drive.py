#!/usr/bin/python

import rospy
import serial
import struct
from geometry_msgs.msg.Twist

cmd_byte_map = {
    'twist': b"\x00"
}

def main():
    rospy.init_node("simple_drive")
    
    baudrate = rospy.get_param('~baudrate', 9600)
    serial_port = rospy.get_param("~serial_dev")
    Serial = serial.Serial(port=serial_port, baudrate=baudrate)
    Serial.open()
    
    def on_new_twist(data):
        serial_msg = cmd_byte_map['twist'] + struct.pack("<ff", data.linear.x, data.angular.z)
        Serial.write(serial_msg)

    subscriber_twist = rospy.Subscriber("cmd_vel", Twist, on_new_twist, queue_size=10)

    rospy.spin()

if __name__ == '__main__':
    main()

