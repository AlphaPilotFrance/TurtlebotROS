import rospy

from nav_msgs.msg import Odometry

#Attempt!
#import System
#import RosSharp.RosBridgeClient
#import std_msgs = RosSharp.RosBridgeClient.Messages.Standard

from geometry_msgs.msg import PoseStamped
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrt, cos, sin

x = 0.0
y = 0.0
theta = 0.0
x_real = 0.0
y_real = 0.0
carlength = 0.44
xvel = 0.0
yvel = 0.0
yrot = 0.0 

def newOdom(msg):
	#print(Odometry)
	global x
	global y
	global theta
	global omega

	x = msg.pose.position.x
	y = msg.pose.position.y
	#print('ww',x)
	#print(y)

	#Pose orientation. Inferior idea.
	rot_q = msg.pose.orientation
	(roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])
	#theta=theta*3.14
	#omega=omega*3.14

	#print('roll', roll)
	#print('omega', omega)
	#print('theta', theta)

def WheelTwist(msg):
	#My simulation wheels: their velocities.
	global xvel
	global yvel
	global yrot
	xvel = msg.linear.x
	yvel = msg.linear.y
	zrot = msg.angular.z
	yrot = msg.angular.y

	print('yrot', yrot)
	if yrot > 2.84:
		yrot = 2.84
	#print('xvel', xvel)
	#print('yvel', yvel)
	#Also need theta going forward.

#calculate omega from x rotation and theta!

#def TbOdom(msg):
	#my real pose. In order to calculate increments. Inferior idea.
#	global x_real
#	global y_real
#	global theta_real

#	x_real = msg.pose.pose.position.x
#	x_real = msg.pose.pose.position.y

#	rot_q_real = msg.pose.pose.orientation
#	(roll_real, pitch_real, theta_real) = euler_from_quaternion([rot_q_real.x, rot_q_real.y, rot_q_real.z, rot_q_real.w])

rospy.init_node("speed_controller")
sub= rospy.Subscriber("/myodom", PoseStamped, newOdom)
#sub= rospy.Subscriber("/odom", Odometry, TbOdom)
sub= rospy.Subscriber("/velocities", Twist, WheelTwist)
pub= rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()
r= rospy.Rate(10)



while not rospy.is_shutdown():
	Forward=xvel*cos(theta)+yvel*sin(theta)
	Sideways=xvel*sin(theta)+yvel*cos(theta)
	Rotation=(Sideways/carlength)/2.5
	#print("Forward", Forward)
	#print("Rotation", Rotation)
	speed.linear.x = Forward
	if (Rotation > 1):
		print('theta', theta)
	print('Rotation', Rotation)
	if (Rotation<2.84):
		if (Rotation>0):
			speed.angular.z = yrot
		else:
			speed.angular.z = yrot


#Inferior idea.
#	goal = Point()
#	goal.x=x
#	goal.y=y
#	inc_x = goal.x -x_real
#	inc_y = goal.y -y_real
#	inc_path = sqrt(inc_x**2+inc_y**2)
#	angle_to_goal = atan2(inc_y, inc_x)
#	inc_angle=angle_to_goal - theta	
#	print('inc_x', inc_x)
#	print('inc_y', inc_y)
#	print('inc_path', inc_path)
#	print('inc_angle', inc_angle)

#	if abs(inc_angle) > 0.1:
#		print('rotate left')
#		speed.angular.z = 0.8
#		#speed.linear.x = 0.0
#		#speed.angular.z = 0.0
#	else: 
		#if inc_angle < -1:
		#	speed.angular.z = -0.5
		#	speed.linear.x = 0.0
		#else:

#		if inc_x > 0.5:
#			print('sprint')
#			speed.linear.x = 0.3
#		else: 
#			if inc_x < -0.5:
#				speed.linear.x = -0.3

		#speed.linear.x = 0.0
		#speed.angular.z = 0.0

	pub.publish(speed)
	r.sleep()

