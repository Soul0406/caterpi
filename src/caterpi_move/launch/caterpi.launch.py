#Librerias para Ubicar Archivos
import os
from ament_index_python import get_package_share_directory
#Librerias para Procesar Archivos
import xacro
from launch.launch_description_sources import PythonLaunchDescriptionSource
#Librerias para Lanzar Nodos
from launch.actions import IncludeLaunchDescription
from launch_ros.actions import Node
from launch import LaunchDescription


def generate_launch_description():
    """ gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([gazebo_launch_filepath])
    ) """

    teleoperacion_node = Node(
        package= "caterpi_move",
        executable= "teleoperacion_caterpi",
        #parameters= [robot_description_config, controller_filepath]
    )

    camara_node = Node(
        package="green_detection",
        executable="publicador_camara",
        #arguments= ["joint_state_broadcaster"]
    )
    
    detector_node = Node(
        package="green_detection",
        executable="detector_verde",
        #arguments= ["joint_group_position_controller"]
    )

    nodes_to_run = [teleoperacion_node, camara_node, detector_node]
    return LaunchDescription(nodes_to_run)
