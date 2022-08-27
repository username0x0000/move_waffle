#!/usr/bin/env python
import rospy
from geometry_msgs.msg import PoseStamped



rospy.init_node('pub_a')
data = PoseStamped
data.seq = 3
pub = rospy.Publisher('sub', PoseStamped, queue_size = 1)
rospy.spin()