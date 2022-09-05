#!/usr/bin/env python

import queue
import rospy
from std_msgs import String
from geometry_msgs.msg import Pose
from control.msg import LoStr

ModeList = ("go", "grip", "release")

class control_tower:
    def __init__(self, lo_str):
        self.mode = "init_program"
        aruco_pub = rospy.Publisher("ARUCO", String, queue_size=1)
        dwa_pub = rospy.Publisher("DWA", Pose, queue_size=1)
        mani_pub = rospy.Publisher("MANI", Pose, queue_size=1)
        self.aruco = LoStr()
        self.dwa = " "
        self.mani = " "
        self.pose = Pose()
        self.controlmodelist = ("GoToDoor", "GripDoor", "OpenDoor", "ReleaseDoor", "FindObject", "GoToObject", "GripObject", "GoToHome")

    def check_mode(self):
        if self.mode == "GoToDoor":
            self.go()
        elif self.mode == "GripDoor":
            self.grip()
        elif self.mode == "OpenDoor":
            self.go()
        elif self.mode == "ReleaseDoor":
            self.release()

        ##########################
        elif self.mode == "FindObject":
            pass
        elif self.mode == "GoToObject":
            self.go()
        elif self.mode == "GripObject":
            self.grip()
        elif self.mode == "GoToHome":
            self.go()

    def sub_all(self):
        self.sub_aruco()
        self.sub_dwa()
        self.sub_mani()

    def sub_aruco(self): aruco_sub = rospy.Subscriber("aruco", LoStr, self.read_aruco)

    def sub_dwa(self): dwa_sub = rospy.Subscriber("dwa", String, self.read_dwa)

    def sub_mani(self): mani_sub = rospy.Subscriber("mani", String, self.read_mani)
    
    def read_aruco(self, lostr): self.aruco = lostr

    def read_dwa(self, data): self.dwa = data

    def read_mani(self, data): self.mani = data

    def go(self):
        dwa_pose = Pose()
        dwa_pose = self.aruco.pose
        dwa_pose.postion.x -= 0.05
        self.dwa_pub.publish(dwa_pose)

    def grip(self):
        mani_pose = Pose()
        mani_pose = self.aruco.pose
        self.mani_pub.publish(mani_pose)

    def release(self):
        mani_pose = Pose()
        mani_pose.postion.x = -1
        mani_pose.postion.y = -1
        mani_pose.postion.z = -1
        self.mani_pub.publish(mani_pose)


def main():
    rospy.init_node("control")
    
    control = control_tower
    
    rospy.spin()

if __name__ == "__main__":
    main()