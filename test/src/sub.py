#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped


rospy.init_node('sub')
sub = rospy.Subscriber('pub_m', PoseStamped, queue_size = 1)
print(sub.seq)
rospy.spin()