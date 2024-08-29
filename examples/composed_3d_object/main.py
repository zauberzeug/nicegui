import math

from nicegui import ui


class CoordinateSystem(ui.scene.group):
    def __init__(self, name: str = "", axis_length: float = 1.0, show_labels: bool = True):
        """AxisTripos

        This element is a Group pre-populated with colored x, y and z axes.
        It can be used to display the pose of a coordinate system

        :param name: name of the coordinate system
        :param axis_length: length of the axis arrow (default 1.0)
        :param show_labels: whether to show the xyz and name labels or not
        """

        super().__init__()

        with self:
            line_radius = 0.02 * axis_length
            line_length = 0.8 * axis_length
            tip_radius = 0.1 * axis_length
            tip_length = axis_length - line_length

            for label, color, rx, ry, rz in (("x", "#ff0000", 0, 0, -math.pi/2), ("y", "#00ff00", 0, 0, 0), ("z", "#0000ff", math.pi/2, 0, 0)):
                with scene.group() as arrow:
                    ui.scene.cylinder(line_radius, line_radius, line_length).move(
                        y=line_length/2).material(color)
                    ui.scene.cylinder(0, tip_radius, tip_length).move(y=line_length +
                                                                      tip_length/2).material(color)
                    if show_labels:
                        ui.scene.text(label, style=f"color:{color}").move(y=1.05 * axis_length)
                arrow.rotate(rx, ry, rz)

            ui.scene.text(name, style="color:darkgray")


with ui.scene() as scene:
    CoordinateSystem("origin")
    custom_frame = CoordinateSystem("custom frame").move(2, 2, 1).rotate(math.pi/3, 0, 0)

ui.run()
