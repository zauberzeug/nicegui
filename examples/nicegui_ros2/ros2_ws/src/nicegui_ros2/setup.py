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
    description='This is a basic example of Nicegui in a ROS2 node based on the minimal publisher example by ROS2',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'basic_nicegui = nicegui_ros2.basic_nicegui:main',
            'joystick_nicegui = nicegui_ros2.joystick_nicegui:main',
        ],

    },
)
