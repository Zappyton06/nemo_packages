# nemo_packages
Development packages for the software Stack of the SRM-AUV 25 vehicle (Project NEMO)

Requirements:
  1. ubuntu 22.04
  2. ROS2 Humble Hawksbill
  3. Gazebo Fortress (Ignition-Gazebo) with ROS 2 Integeration
  4. Robot State Publisher , Joint State Publisher 

Instructions to use this package:
  1. Create a ROS2 workspace
      ```mdkir submarine_ws && cd submarine_ws```
      ```mkdir src && cd src```
  3. Clone the above repository into your src directory and return to the root of the workspace
     ```
     git clone https://github.com/Zappyton06/nemo_packages 
     cd ..
     ```
  4. To launch the simulation
     ```
     colcon build
     source install/setup.bash
     ros2 launch nemo_bringup world_launch.launch.py
     ```
  6. In another terminal (assuming you are in the root of the same workspace)
     ```
     source install/setup.bash
     ros2 launch nemo_bringup gazebo_launch.launch.py     
     ```

  PS: For Ease of use , I suggest adding ```source ~/submarine_ws/install/setup.bash``` to the ```bashrc``` for better performance
