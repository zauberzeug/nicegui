import glob
import os

from setuptools import setup

package_name = 'gui'

setup(
    name=package_name,
    version='1.0.0',
    packages=[package_name],
    data_files=[
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Zauberzeug GmbH',
    maintainer_email='nicegui@zauberzeug.com',
    description='This is an example of NiceGUI in a ROS2 node based that uses a joystick to control turtlesim.',
    license='MIT License',
    entry_points={
        'console_scripts': [
            'nicegui_node = gui.node:main',
        ],

    },
)
