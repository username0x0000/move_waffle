cmake_minimum_required(VERSION 3.0.2)
project(control)

find_package(catkin REQUIRED COMPONENTS
  rospy
  geometry_msgs
  std_msgs
  message_generation
)

add_message_files(
  FILES
  LoStr.msg
  Locations.msg
  Coordinate.msg
)

generate_messages(
  DEPENDENCIES
  std_msgs
  geometry_msgs
)

catkin_package(
  CATKIN_DEPENDS rospy geometry_msgs std_msgs
)


