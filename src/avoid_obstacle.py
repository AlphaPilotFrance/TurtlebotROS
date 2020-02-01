#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from darknet_ros_msgs.msg import BoundingBoxes
from geometry_msgs.msg import Twist
import time

meters=0
def human():
	start_time = time.time()
	duration= time.time() - start_time
	while (duration < meters):
		print("continue action")
		pub.publish(move)
		duration = time.time() - start_time
		move.linear.x = 0.5
		move.angular.z = 0.0
		pub.publish(move)

def distance(meters, move):
	start_time = time.time()
	duration= time.time() - start_time
	while (duration < meters):
		print("continue action")
		pub.publish(move)
		duration = time.time() - start_time
	 
def callback(msg): 
#	print('===============================')
	#print( msg.object_detector)
	if hasattr(msg, 'bounding_boxes'):
		print('Boxes') #get reaadddyyy
		size = len(msg.bounding_boxes)
		print (size)
		for i in msg.bounding_boxes:
			print('checking for objects')
			print(i.Class)
			if i.Class == "person":
				print('person!')
				#human()
				move.linear.x = 0.5
				move.angular.z = 0.0
				pub.publish(move)
				rospy.sleep(2)
				


	print('===============================')
	if hasattr(msg, 'ranges'):
		print('s1 [0]') #value front-direction laser beam
		print msg.ranges[0] #print the distance to an obstacle in front
		#first value of 359 is front.

		#If the distance to an obstacle in front of the robot is bigger than 1 meter, the robot will move forward
#		for x in msg.ranges:
#			if msg.ranges.index(x) != 0 and x<0.2:
#				move.linear.x = 0.0
#				move.angular.z = 0.6	
#			else: 
#				if msg.ranges.index(x) == 0 and x<0.2:
#					move.linear.x = 0.3
#					move.angular.z = 0.0	
		pub.publish(move)
				
		if msg.ranges[0] < 0.5:
			move.linear.x = 0.2
			move.angular.z = 0.0
		else:	
			move.linear.x = 0.0
			move.angular.z = 0.0
		pub.publish(move)
#		human()

	#Robot swerves until detection	
	#Robot detects obstacle under 0.5 m
	#Approaches it at 0.2 m/s
	#then stops by 0.2 m

#	if msg.ranges[0] < 0.7 and msg.ranges[0] > 0.2:
#		move.linear.x = 0.2
#		move.angular.z = 0.0
#	else: 	
#		if msg.ranges[0] < 0.2:
#			move.linear.x = 0.0
#			move.angular.z = 0.0
#		else:
#			move.linear.x = 0.0
#			move.angular.z = 0.2
	

rospy.init_node('obstacle_avoidance')
sub = rospy.Subscriber ('/scan', LaserScan, callback)
sub = rospy.Subscriber ('/darknet_ros/bounding_boxes/', BoundingBoxes, callback)
pub = rospy.Publisher ('/cmd_vel', Twist)
move = Twist()
rospy.spin()

