from setuptools import setup

package_name = 'nicegui_ros2'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='jens',
    maintainer_email='jens.ogorek@gmail.com',
    description='This is an example of NiceGUI in a ROS2 node based that uses a joystick to control turtlesim.',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'nicegui_node = nicegui_ros2.nicegui_node:main',
        ],

    },
)
