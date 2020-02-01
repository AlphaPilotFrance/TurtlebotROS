#! /usr/bin/env python

import rospy #library: Python for ROS 
from geometry_msgs.msg import Twist #Twist message from std_msgs package

def talker():
	rospy.init_node('vel_publisher') #initiate a Node named 'vel_publihser'
	pub= rospy.Publisher('cmd_vel', Twist, queue_size=10) #create Publisher object
	move= Twist()		#var named move of type Twist
	rate= rospy.Rate(1)	#set a publish rate of 0.5Hz
	while not rospy.is_shutdown():
		move.linear.x=1
		move.angular.z=1
		pub.publish(move)
		rate.sleep()

__name__ == '__main__':
	try:
		talker()
	except rospy.ROSInterruptException:
		pass
