#! /usr/bin/env python

import rospy
from sensor_msgs.msg import LaserScan
from darknet_ros_msgs.msg import BoundingBoxes
from geometry_msgs.msg import Twist
from std_msgs.msg import Int32
import time
	 
def callback1(msg): 
	print('===============================')
	#print( msg.object_detector)
	print('Boxes') #get reaadddyyy
	size = len(msg.bounding_boxes)
	print (size)
	for i in msg.bounding_boxes:
		print('checking for objects')
		print(i.Class)
		if i.Class == "person":
			print(i.xmin, i.xmax)
			print('person!')
			global boundaries
			boundaries = [i.xmin, i.xmax]
			print(boundaries[0])
		

				

def callback2(msg):
	if ('validpath' in globals()):
		print('===============================')
		print('s1 [0]') #value front-direction laser beam
		print msg.ranges[0] #print the distance to an obstacle in front
				#first value of 359 is front.
		if ('distance' in globals()):
		#then already started...
			pass
		else:
			global distance
			distance=msg.ranges[0]
		print('initial distance to target:', distance)

def callback3(msg):
	print('===============================')
#wrap up in various trajectories... upon modes for global variable.
#path='rotate' UNTIL global msg.ranges[0]=msg.ranges[68]
#path='avoid' WHEN global validpath=1 

	if ('distance' in globals()):
		now2=msg.data
		if ('start2' in globals()):
			#then already started...
			pass
		else:
			global start2
			start2=msg.data
		elapsed = now2 - start2
		duration = (distance/0.2)
		print ('seconds since start:', elapsed)
		print ('total time:', duration)
		if elapsed < duration:	
			move.linear.x = 0.2
			move.angular.z = 0.0
		else:
			move.linear.x = 0.0
			move.angular.z = 0.0
		pub.publish(move)


	if ('boundaries' in globals()):
			center= (boundaries[0]+boundaries[1])/2
			deviation=center-320
			
			print('deviation', deviation)

			if abs(deviation) > 50:
				global deviate				
				deviate=1
				now=msg.data
				if ('start' in globals()):
					#then already started...
					pass
				else:
					global start
					start=msg.data
				elapsed = now - start
				print ('seconds since start:', elapsed)
				duration = 100
				print ('total time:', duration)
				if deviation > 0:
					if elapsed < duration:	
						move.linear.x = 0.0
						move.angular.z = -0.05
					else:
						move.linear.x = 0.0
						move.angular.z = 0.0
				else:
					if elapsed < duration:	
						move.linear.x = 0.0
						move.angular.z = 0.05
					else:
						move.linear.x = 0.0
						move.angular.z = 0.0
			else:
				if ('deviate' in globals()) and deviate==1:
					deviate = 0
					move.linear.x = 0.0
					move.angular.z = 0.0
					if ('validpath' in globals()):
						#then already started...
						pass
					else:
						global validpath
						validpath=1
					
				

			pub.publish(move)

rospy.init_node('obstacle_avoidance')
sub = rospy.Subscriber ('/counter', Int32, callback3)
sub = rospy.Subscriber ('/scan', LaserScan, callback2)
sub = rospy.Subscriber ('/darknet_ros/bounding_boxes/', BoundingBoxes, callback1)
pub = rospy.Publisher ('/cmd_vel', Twist)
move = Twist()


rospy.spin()
