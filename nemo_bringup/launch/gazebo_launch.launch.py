from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.actions import ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.substitutions import Command, PathJoinSubstitution
from launch_ros.substitutions import FindPackageShare
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    description_pkg = 'nemo_description'
    bringup_pac = "nemo_bringup"

    #xacro_path = '/home/zappington/submarine_ws/src/nemo_description/urdf/nemo.urdf.xacro'  # Replace with the actual absolute path    # Run xacro to generate robot description
    
    #xacro_path = '/home/zappington/submarine_ws/src/nemo_description/urdf/nemo_sdf.sdf'

    xacro_path = PathJoinSubstitution([
        FindPackageShare(description_pkg),
        'urdf',
        'nemo.urdf.xacro'
    ])
    

    rviz_config_path = PathJoinSubstitution([
        FindPackageShare(description_pkg),
        'rviz',
        'robot_config.rviz'
    ])


    return LaunchDescription([
        # 2. robot_state_publisher
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{
                'robot_description': ParameterValue(
                    Command(['xacro ', xacro_path]),
                    value_type=str
            ),
                'use_sim_time': True
            }],
            output='screen'
        ),

        Node(
            package='joint_state_publisher',
            executable='joint_state_publisher'
        ),

        # 3. Spawn the robot in Gazebo at 1.5 - 2m below the fluid level to avoid seg faults
        Node(
            package='ros_gz_sim',
            executable='create',
            name='spawn_nemo',
            arguments=[
                '-name', 'nemo_auv',
                '-x', '0', '-y', '0', '-z', '-2',
                '-topic', '/robot_description'
            ],
            output='screen',
            parameters=[{'use_sim_time': True}]
        ),

        # 4. Gazebo ↔ ROS bridge
        Node(
            package='ros_gz_bridge',
            executable='parameter_bridge',
            name='ros_ign_bridge_node',
            output='screen',
            arguments=[
                '/clock@rosgraph_msgs/msg/Clock[ignition.msgs.Clock',
                '/joint_states@sensor_msgs/msg/JointState[ignition.msgs.Model',
                '/tf@tf2_msgs/msg/TFMessage[ignition.msgs.Pose_V',
                '/nemo_auv/thruster1/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster2/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster3/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster4/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster5/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster6/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster7/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
                '/nemo_auv/thruster8/cmd@std_msgs/msg/Float64]ignition.msgs.Double',
            ]
        ),

        # 5. RViz
        Node(
            package='rviz2',
            executable='rviz2',
            name='rviz2',
            arguments=['-d', rviz_config_path],
            parameters=[{'use_sim_time': True}],
            output='screen'
        )
    ]) 
