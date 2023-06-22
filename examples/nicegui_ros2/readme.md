# Simple NiceGUI example
The example is based on ROS2's Minimal Publisher, that is controlled by NiceGUI's app.on_startup function. You can see and access the published message on the /topic topic and see the simple visualization of NiceGUI on 127.0.0.1:8000. If you change some part of the code and save it, you can immediately see the change without restarting the node.

## Run
Starting from the `nicegui_ros2/basic_example` folder:

```bash
docker compose up 
```

# Nicegui Joystick and Turtlesim
Like the simple example, ROS2 itself is controlled by the app.on_startup function. Everything works like the Simple NiceGUI example, but this time the UI on the local webpage will display a joystick. 
If you are running the Node from the provided Docker, it will start a second Docker with the turtlesim_node already running. 
Note: Keep in mind that the provided Docker composition is for usage within an Ubuntu system. If you are running it somewhere else, you might have to change the .yml file. These changes are related to the visualization of the turtlesim_node

## Run
Before Running the Docker, you have to configure your xhost like this: 

```bash
xhost local:root
```

 Starting from the `nicegui_ros2/joystick_example` folder:

```bash
docker compose up 
```

If you want to run the turtlesim_node locally and just run the joystick from Docker:

```bash
docker compose up joystick_example
```

## Run information
The parameter `uvicorn_reload_dirs` will define which files trigger a reload on change. The path is automatically detected.

## Without Docker
If you want to run the Nodes locally in your ROS2 environment, you can copy the Nodes from the ros2_ws/src folder. 
To run it, just use the normal ros2 run:

```bash
ros2 run nicegui_ros2 basic_nicegui
```
or 
```bash
ros2 run nicegui_ros2 joystick_nicegui
```