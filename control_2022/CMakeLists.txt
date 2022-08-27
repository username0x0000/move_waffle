cmake_minimum_required(VERSION 3.0.2)
project(control_2022)

find_package(catkin REQUIRED COMPONENTS
  geometry_msgs
  message_generation
  rospy
  sensor_msgs
  std_msgs
)

add_service_files(
  FILES
  contol_2022.srv
)

generate_messages(
  DEPENDENCIES
  std_msgs  geometry_msgs  sensor_msgs
)

catkin_package(
  CATKIN_DEPENDS geometry_msgs rospy sensor_msgs std_msgs
)


