#!/usr/bin/env python
import rospy
import sys, select, os
if os.name == 'nt':
  import msvcrt, time
else:
  import tty, termios
from control_2022.srv import control_2022, control_2022Response


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


def srv_callback(request):
    print(request)
    response = which_key()
    
    return response


def main():
    rospy.init_node("test_res")
    
    res = rospy.Service("test_srv", control_2022, srv_callback)
    
    rospy.spin()


if __name__ == "__main__": main()