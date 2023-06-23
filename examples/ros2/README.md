# Simple NiceGUI example
This example is a basic ROS2 implementation with NiceGUI. It starts up a virtual joystick on a local webpage (127.0.0.1:8000), that publishes messages on the /turtle1/twist topic for an instance of turtlesim_node to be controlled.
ROS2 and NiceGUI are fully functional in this example, changes to the code will trigger a restart of the full ROS2 Node.

## Run

Note: Keep in mind that the provided Docker composition is for usage within an Ubuntu system. If you are running it somewhere else, you might have to change the .yml file. These changes are related to the visualization of the turtlesim_node

Before Running the Docker, you have to configure your xhost like this:

```bash
xhost local:root
```
Starting from the `ros2` folder:

```bash
docker compose up
```
If you want just want run the joystick from Docker:

```bash
docker compose up joystick_example
```

## Run information
The parameter `uvicorn_reload_dirs` will define which files trigger a reload on change. The path is automatically detected.

## Without Docker
If you want to run the Nodes locally in your ROS2 environment, you can copy the Nodes from the ros2_ws/src folder.
To run it, just use the normal ros2 run:

```bash
ros2 run nicegui_ros2 joystick_nicegui
```
