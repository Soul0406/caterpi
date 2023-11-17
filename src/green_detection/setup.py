from setuptools import find_packages, setup

package_name = 'green_detection'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='robotica',
    maintainer_email='robotica@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': ['publicador_camara=green_detection.publicador_camara:main',
        'suscriptor_camara=green_detection.suscriptor_camara:main', 'detector_verde=green_detection.detector_verde:main',
        ],
    },
)
