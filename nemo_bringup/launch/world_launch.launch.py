from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    world_path = '/home/zappington/submarine_ws/src/nemo_bringup/world/world_side.sdf'

    return LaunchDescription([
        ExecuteProcess(
            cmd=['ign', 'gazebo','-r', world_path],
            output='screen'
        )
    ]) 
