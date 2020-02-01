#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan

def callback(msg): 
	print('===============================')
	print('s1 [0]') #value front-direction laser beam
	print msg.ranges[0] #print the distance to an obstacle in front
	#first value of 359 is front.

	print('s1 [90]') 
	print msg.ranges[90] 

	print('s1 [180]') 
	print msg.ranges[180] 

	print('s1 [270]') 
	print msg.ranges[270] 

	print('s1 [359]') 
	print msg.ranges[359] 

rospy.init_node('laser_data') #initiate node: 'laser_data'
sub = rospy.Subscriber('scan', LaserScan, callback) #sub to laser/scan topic

rospy.spin()

