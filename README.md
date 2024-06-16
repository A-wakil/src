# src

# For SLAM
- **Using ros2 humble**
**mkdir slam work space (slam_ws) or clone the repo and use the folder from the repo(slam_ws)**
-
If you're using the repo slam workspace, delete every other folder from the workspace except from the src folder when it's on your device and run `colcon build --symlink-install` in the directory. If you made a new workspace, copy the src folder into it and run `colcon build --symlink-install`

# *Install the following*
- `sudo apt install ros-humble-slam-toolbox`
- `sudo apt install ros-humble-navigation2 ros-humble-nav2-bringup ros-humble-turtlebot3*`
- source workspace inside directory `source install/setup.bash`

Repeat all of these steps on the robot device workspace as well
- On the robot workspace, run `ros2 launch articubot_one launch_robot.launch.py`
- On the computer workspace/slam_ws, run `ros2 launch articubot_one joystick.launch.py` replace this file accordingly to the appropriate hardware control model for our bot
- On the computer workspace/slam_ws, run rviz `rviz2 -d src/articubot_one/config/main.rviz`
- On the robot workspace, run `ros2 launch articubot_one rplidar.launch.py`
- Record the map option in rviz as the robot navigates
