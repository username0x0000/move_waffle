#!/usr/bin/env python
import rospy
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios
from control_2022.srv import control_2022, control_2022Request
from geometry_msgs.msg import Pose


def getKey():
    tty.setraw(sys.stdin.fileno())
    rlist, _, _ = select.select([sys.stdin], [], [], 0.1)
    if rlist:
        key = sys.stdin.read(1)
    else:
        key = ''

    termios.tcsetattr(sys.stdin, termios.TCSADRAIN, settings)
    return key


def which_key():
    key = getKey()
    if key == 'q': return "go"
    elif key == 'e': return "grip"
    elif key == 'r': return "release"
    
    elif key == 'a': return "working"
    elif key == 's': return "fail"
    elif key == 'd': return "success"

    if int(key): return int(key)


def main():
    rospy.init_node("test_req")
    
    rospy.wait_for_service("test_srv")
    requester = rospy.ServiceProxy("test_srv", control_2022)
    rate = rospy.Rate(10)
    
    print("상태를 입력하세요.")
    data_s = which_key()
    
    data_p = Pose()
    print("x : ")
    data_p.position.x = which_key()
    print("y : ")
    data_p.position.y = which_key()
    print("z : ")
    data_p.position.z = which_key()

    data = control_2022Request(data_s, data_p)
    result = requester(data)
    
    print(data)
    print(result)
    
    rate.sleep()
    
    rospy.spin()


if __name__ == "__main__": main()