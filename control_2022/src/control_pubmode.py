#!/usr/bin/env python
import rospy
import message_filters
from geometry_msgs.msg import PoseStamped


def aruco_wait():
    wait_ps.header.frame_id = "wait"
    wait_ps = PoseStamped()
    pub_aruco(wait_ps)

def dwa_wait():
    wait_ps = PoseStamped()
    wait_ps.header.frame_id = "wait"
    pub_dwa(wait_ps)

def mani_wait():
    wait_ps = PoseStamped()
    wait_ps.header.frame_id = "wait"
    pub_mani(wait_ps)


def pub_aruco(aruco_pdata):
    aruco_pub = rospy.Publisher("aruco", PoseStamped, queue_size=1)
    aruco_pub(aruco_pdata)

def pub_dwa(dwa_pdata):
    dwa_pub = rospy.Publisher("dwa", PoseStamped, queue_size=1)
    dwa_pub(dwa_pdata)

def pub_mani(mani_pdata):
   mani_pub = ropsy.Publisher("mani", PoseStamped, queue_size=1)
   mani_pub.publish(mani_pdata)


class control_mode:
    def __init(self, sub_data):
        self.PS_data = sub_data
        Mode = {
            "InitProgram" : FindDoor,
            
            # mode success
            "FindDoorFin" : GoToDoor,
            "GoToDoorFin" : GripDoor,
            "GripDoorFin" : OpenDoor,
            "OpenDoorFin" : ReleaseDoor,
            "ReleaseDoorFin" : FindObject,
            "FindObjectFin" : GoToObject,
            "GoToObjectFin" : GripObject,
            "GripObjectFin" : GoToHome,
           
            # mode fail
            "GoToDoorFail" : FindDoor,
            "GripDoorFail" : GoToDoor,
            "OpenDoorFail" : GripDoor,
            "ReleaseDoorFail" : OpenDoor,
            "FindObjectFail" : ReleaseDoor,
            "GoToObjectFail" : FindObject,
            "GripObjectFail" : GoToObject
        }

    def check_mode(self):
        self.Mode[self.PS_data.header.frame_id]()

    def change_mode(self, new_mode):
        self.PS_data.header.frame_id = new_mode


    def FindDoor(self):
        pub_aruco(self.PS_data)
        pub_dwa(self.PS_data)
        mani_wait()

    def GoToDoor(self):
        pub_dwa(self.PS_data)
        aruco_wait()
        mani_wait()

    def GripDoor(self):
        pub_mani(self.PS_data)
        aruco_wait()
        dwa_wait()

    def OpenDoor(self):
        pub_dwa(self.PS_data)
        aruco_wait()
        mani_wait()

    def ReleaseDoor(self):
        pub_mani(self.PS_data)
        aruco_wait()
        dwa_wait()

    def FindObject(self):
        pub_aruco(self.PS_data)
        pub_dwa(self.PS_data)
        mani_wait()

    def GoToObject(self):
        pub_dwa(self.PS_data)
        aruco_wait()
        mani_wait()

    def GripObject(self):
        pub_mani(self.PS_data)
        aruco_wait()
        dwa_wait()

    def GoToHome(self):
        pub_dwa(self.PS_data)
        aruco_wait()
        mani_wait()


ps_data = PoseStamped()
ps_data.header.frame_id = "init_program"

def save_data(a_data, d_data, m_data):
    global ps_data
    check = [a_data.header.frame_id, d_data.header.frame_id, m_data.header.frame_id]
    ready = []
    for a in range(3):
        if not check[a] == "waiting" or not check[a] == "working":
            ready.append(check[a])
    for a in ready:
        if a[-4:] == "Fail":
            ps_data.header.frame_id = a
            return
    for a in ready:
        if a[-3:] == "Fin":
            ps_data.header.frame_id = check[a]
            return


def main():
    rospy.init_node("control_2022")

    aruco_data = message_filters.Subscriber("ARUCO", PoseStamped, save_data)
    dwa_data = message_filters.Subscriber("DWA", PoseStamped, save_data)
    mani_data = message_filters.Subscriber("MANI", PoseStamped, save_data)
   
    united_data = message_filters.TimeSynchronizer([aruco_data, dwa_data, mani_data], 10)
    united_data.registerCallback(save_data)

    global ps_data
    
    control_class = control_mode(ps_data)
    control_class.check_mode()

    rospy.spin()


if __name__ == "__main__":
    main()