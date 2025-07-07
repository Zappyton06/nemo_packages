from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    bringup_package = "nemo_bringup"

    world_path = PathJoinSubstitution([
        FindPackageShare(bringup_package),
        'world',
        'world_side.sdf'
    ])

    return LaunchDescription([
        ExecuteProcess(
            cmd=['ign', 'gazebo','-r', world_path],
            output='screen'
        )
    ]) 
