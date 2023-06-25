FROM ros:humble-ros-base

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential 

SHELL ["/bin/bash", "-c"]

RUN pip3 install nicegui pyquaternion

ADD ros2_ws ros2_ws/

RUN cd ros2_ws && \
    source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install

COPY ros_entrypoint.sh /

EXPOSE 8080
ENTRYPOINT ["/ros_entrypoint.sh"]
CMD ["bash"]

