import rospy
from geometry_msgs.msg import PoseStamped


data = PoseStamped
data.seq = 4

pub = rospy.Publisher('sub', data, queue_size = 1)
rospy.spin()