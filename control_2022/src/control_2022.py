#!/usr/bin/env python
import rospy
from control.srv import tl_r, tl_rRequest
from geometry_msgs.msg import Pose, PoseStamped
from std_msgs.msg import String


status_list = ["find_door", "go_to_door", "grip_door", "open_door", "release_door", "go_inside", "find_object", "grip_object", "go_home"]
status_dic = {
    "find_aruco":which_aruco,
    "go":go,
    "grip":grip,
    "release":release
}
task = {}


def which_aruco(aruco_id):
    if aruco_id == "door":
        return "open_door"
    if aruco_id == "object":
        return "grip_object"


def go(task, location):
    rospy.wait_for_service("DWA")
    dwa = rospy.ServiceProxy("DWA", tl_r)
    req = tl_rRequest(task, location)
    res = dwa(req)
    return res


def grip(task, location):
    rospy.wait_for_service("MANIPULATOR")
    manipulator = rospy.ServiceProxy("MANIPULATOR", tl_r)
    req = tl_rRequest(task, location)
    res = manipulator(req)
    return res


def release(task):
    rospy.wait_for_service("MANIPULATOR")
    manipulator = rospy.ServiceProxy("MANIPULATOR", tl_r)
    voidlocation = Pose()
    req = tl_rRequest(task, voidlocation)
    res = manipulator(req)
    return res


def check_status(status):
    if status == "find_door":
        aruco = rospy.Subsrcriber("ARUCO", PoseStamped)
        if aruco.frame_id == "success":
            return "go_to_door"
        else:
            return
    
    if status == "go_to_door":
        rospy.wait_for_service("DWA", control_2022)
        dwa = rospy.ServiceProxy("DWA", control_2022)
        
 
        
        


def main():
    rospy.init_node("control_2022")
    while not rospy.is_shutdown():
        rospy.wait_for_service("DWA")
        rospy.wait_for_service("MANIPULATOR")
        
        dwa = rospy.ServiceProxy("DWA", control_2022)
        manipulator = rospy.ServiceProxy("MANIPULATOR", control_2022)
        
        d_s = String()
        d_p = Pose()
        m_s = String()
        m_p = Pose()
        
        dwa_request = control_2022Request(d_s, d_p)
        manipulator_request = control_2022Request(m_s, m_p)


if __name__ == "__main__": main()