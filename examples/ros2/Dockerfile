FROM ros:humble-ros-base

RUN apt-get update && apt-get install -y \
    python3-pip \
    python3-dev \
    build-essential 

SHELL ["/bin/bash", "-c"]

RUN pip3 install nicegui

EXPOSE 8000

COPY ros2_ws ros2_ws/

RUN cd ros2_ws && \
    source /opt/ros/humble/setup.bash && \
    colcon build --symlink-install

COPY ros_entrypoint.sh /

ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]

