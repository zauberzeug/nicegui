import math

from .scene_object3d import Object3D


class Group(Object3D):

    def __init__(self) -> None:
        """Group

        This element is based on Three.js' `Group <https://threejs.org/docs/index.html#api/en/objects/Group>`_ object.
        It is used to group objects together.
        """
        super().__init__('group')


class Box(Object3D):

    def __init__(self,
                 width: float = 1.0,
                 height: float = 1.0,
                 depth: float = 1.0,
                 wireframe: bool = False,
                 ) -> None:
        """Box

        This element is based on Three.js' `BoxGeometry <https://threejs.org/docs/index.html#api/en/geometries/BoxGeometry>`_ object.
        It is used to create a box-shaped mesh.

        :param width: width of the box (default: 1.0)
        :param height: height of the box (default: 1.0)
        :param depth: depth of the box (default: 1.0)
        :param wireframe: whether to display the box as a wireframe (default: `False`)
        """
        super().__init__('box', width, height, depth, wireframe)


class Sphere(Object3D):

    def __init__(self,
                 radius: float = 1.0,
                 width_segments: int = 32,
                 height_segments: int = 16,
                 wireframe: bool = False,
                 ) -> None:
        """Sphere

        This element is based on Three.js' `SphereGeometry <https://threejs.org/docs/index.html#api/en/geometries/SphereGeometry>`_ object.
        It is used to create a sphere-shaped mesh.

        :param radius: radius of the sphere (default: 1.0)
        :param width_segments: number of horizontal segments (default: 32)
        :param height_segments: number of vertical segments (default: 16)
        :param wireframe: whether to display the sphere as a wireframe (default: `False`)
        """
        super().__init__('sphere', radius, width_segments, height_segments, wireframe)


class Cylinder(Object3D):

    def __init__(self,
                 top_radius: float = 1.0,
                 bottom_radius: float = 1.0,
                 height: float = 1.0,
                 radial_segments: int = 8,
                 height_segments: int = 1,
                 wireframe: bool = False,
                 ) -> None:
        """Cylinder

        This element is based on Three.js' `CylinderGeometry <https://threejs.org/docs/index.html#api/en/geometries/CylinderGeometry>`_ object.
        It is used to create a cylinder-shaped mesh.

        :param top_radius: radius of the top (default: 1.0)
        :param bottom_radius: radius of the bottom (default: 1.0)
        :param height: height of the cylinder (default: 1.0)
        :param radial_segments: number of horizontal segments (default: 8)
        :param height_segments: number of vertical segments (default: 1)
        :param wireframe: whether to display the cylinder as a wireframe (default: `False`)
        """
        super().__init__('cylinder', top_radius, bottom_radius, height, radial_segments, height_segments, wireframe)


class Ring(Object3D):

    def __init__(self,
                 inner_radius: float = 0.5,
                 outer_radius: float = 1.0,
                 theta_segments: int = 8,
                 phi_segments: int = 1,
                 theta_start: float = 0,
                 theta_length: float = 2 * math.pi,
                 wireframe: bool = False,
                 ) -> None:
        """Ring

        This element is based on Three.js' `RingGeometry <https://threejs.org/docs/index.html#api/en/geometries/RingGeometry>`_ object.
        It is used to create a ring-shaped mesh.

        :param inner_radius: inner radius of the ring (default: 0.5)
        :param outer_radius: outer radius of the ring (default: 1.0)
        :param theta_segments: number of horizontal segments (default: 8, higher means rounder)
        :param phi_segments: number of vertical segments (default: 1)
        :param theta_start: start angle in radians (default: 0)
        :param theta_length: central angle in radians (default: 2π)
        :param wireframe: whether to display the ring as a wireframe (default: `False`)
        """
        super().__init__('ring',
                         inner_radius, outer_radius, theta_segments, phi_segments, theta_start, theta_length, wireframe)


class QuadraticBezierTube(Object3D):

    def __init__(self,
                 start: list[float],
                 mid: list[float],
                 end: list[float],
                 tubular_segments: int = 64,
                 radius: float = 1.0,
                 radial_segments: int = 8,
                 closed: bool = False,
                 wireframe: bool = False,
                 ) -> None:
        """Quadratic Bezier Tube

        This element is based on Three.js' `QuadraticBezierCurve3 <https://threejs.org/docs/index.html#api/en/extras/curves/QuadraticBezierCurve3>`_ object.
        It is used to create a tube-shaped mesh.

        :param start: start point of the curve
        :param mid: middle point of the curve
        :param end: end point of the curve
        :param tubular_segments: number of tubular segments (default: 64)
        :param radius: radius of the tube (default: 1.0)
        :param radial_segments: number of radial segments (default: 8)
        :param closed: whether the tube should be closed (default: `False`)
        :param wireframe: whether to display the tube as a wireframe (default: `False`)
        """
        super().__init__('quadratic_bezier_tube',
                         start, mid, end, tubular_segments, radius, radial_segments, closed, wireframe)


class Extrusion(Object3D):

    def __init__(self,
                 outline: list[list[float]],
                 height: float,
                 wireframe: bool = False,
                 ) -> None:
        """Extrusion

        This element is based on Three.js' `ExtrudeGeometry <https://threejs.org/docs/index.html#api/en/geometries/ExtrudeGeometry>`_ object.
        It is used to create a 3D shape by extruding a 2D shape to a given height.

        :param outline: list of points defining the outline of the 2D shape
        :param height: height of the extrusion
        :param wireframe: whether to display the extrusion as a wireframe (default: `False`)
        """
        super().__init__('extrusion', outline, height, wireframe)


class Stl(Object3D):

    def __init__(self,
                 url: str,
                 wireframe: bool = False,
                 ) -> None:
        """STL

        This element is used to create a mesh from an STL file.

        :param url: URL of the STL file
        :param wireframe: whether to display the STL as a wireframe (default: `False`)
        """
        super().__init__('stl', url, wireframe)


class Gltf(Object3D):

    def __init__(self,
                 url: str,
                 ) -> None:
        """GLTF

        This element is used to create a mesh from a glTF file.

        :param url: URL of the glTF file
        """
        super().__init__('gltf', url)


class Line(Object3D):

    def __init__(self,
                 start: list[float],
                 end: list[float],
                 ) -> None:
        """Line

        This element is based on Three.js' `Line <https://threejs.org/docs/index.html#api/en/objects/Line>`_ object.
        It is used to create a line segment.

        :param start: start point of the line
        :param end: end point of the line
        """
        super().__init__('line', start, end)


class Curve(Object3D):

    def __init__(self,
                 start: list[float],
                 control1: list[float],
                 control2: list[float],
                 end: list[float],
                 num_points: int = 20,
                 ) -> None:
        """Curve

        This element is based on Three.js' `CubicBezierCurve3 <https://threejs.org/docs/index.html#api/en/extras/curves/CubicBezierCurve3>`_ object.

        :param start: start point of the curve
        :param control1: first control point of the curve
        :param control2: second control point of the curve
        :param end: end point of the curve
        :param num_points: number of points to use for the curve (default: 20)
        """
        super().__init__('curve', start, control1, control2, end, num_points)


class Text(Object3D):

    def __init__(self,
                 text: str,
                 style: str = '',
                 ) -> None:
        """Text

        This element is used to add 2D text to the scene.
        It can be moved like any other object, but always faces the camera.

        :param text: text to display
        :param style: CSS style (default: '')
        """
        super().__init__('text', text, style)


class Text3d(Object3D):

    def __init__(self,
                 text: str,
                 style: str = '',
                 ) -> None:
        """3D Text

        This element is used to add a 3D text mesh to the scene.
        It can be moved and rotated like any other object.

        :param text: text to display
        :param style: CSS style (default: '')
        """
        super().__init__('text3d', text, style)


class Texture(Object3D):

    def __init__(self,
                 url: str,
                 coordinates: list[list[list[float] | None]],
                 ) -> None:
        """Texture

        This element is used to add a texture to a mesh.

        :param url: URL of the texture image
        :param coordinates: texture coordinates
        """
        super().__init__('texture', url, coordinates)

    def set_url(self, url: str) -> None:
        """Change the URL of the texture image."""
        self.args[0] = url
        self.scene.run_method('set_texture_url', self.id, url)

    def set_coordinates(self, coordinates: list[list[list[float] | None]]) -> None:
        """Change the texture coordinates."""
        self.args[1] = coordinates
        self.scene.run_method('set_texture_coordinates', self.id, coordinates)


class SpotLight(Object3D):

    def __init__(self,
                 color: str = '#ffffff',
                 intensity: float = 1.0,
                 distance: float = 0.0,
                 angle: float = math.pi / 3,
                 penumbra: float = 0.0,
                 decay: float = 1.0,
                 ) -> None:
        """Spot Light

        This element is based on Three.js' `SpotLight <https://threejs.org/docs/index.html#api/en/lights/SpotLight>`_ object.
        It is used to add a spot light to the scene.

        :param color: CSS color string (default: '#ffffff')
        :param intensity: light intensity (default: 1.0)
        :param distance: maximum distance of light (default: 0.0)
        :param angle: maximum angle of light (default: π/2)
        :param penumbra: penumbra (default: 0.0)
        :param decay: decay (default: 2.0)
        """
        super().__init__('spot_light', color, intensity, distance, angle, penumbra, decay)


class PointCloud(Object3D):

    def __init__(self,
                 points: list[list[float]],
                 colors: list[list[float]] | None = None,
                 point_size: float = 1.0,
                 ) -> None:
        """Point Cloud

        This element is based on Three.js' `Points <https://threejs.org/docs/index.html#api/en/objects/Points>`_ object.

        :param points: list of points
        :param colors: optional list of colors (one per point)
        :param point_size: size of the points (default: 1.0)
        """
        super().__init__('point_cloud', points, colors, point_size)
        if colors is not None:
            self.material(color=None)

    def set_points(self, points: list[list[float]], colors: list[list[float]] | None = None) -> None:
        """Change the points and colors of the point cloud."""
        self.args[0] = points
        self.args[1] = colors
        self.scene.run_method('set_points', self.id, points, colors)
        if colors is not None:
            self.material(color=None)


class AxesHelper(Object3D):

    def __init__(self,
                 length: float = 1.0,
                 ) -> None:
        """Axes Helper

        This element is based on Three.js' `AxesHelper <https://threejs.org/docs/#api/en/helpers/AxesHelper>`_ object.
        It is used to visualize the XYZ axes:
        The X axis is red.
        The Y axis is green.
        The Z axis is blue.

        :param length: length of the the axes (default: 1.0)
        """
        super().__init__('axes_helper', length)


class Polyline(Object3D):

    def __init__(self,
                 points: list[list[float]],
                 colors: list[list[float]] | None = None,
                 dashed: bool = False,
                 dash_size: float = 3.0,
                 gap_size: float = 1.0,
                 ) -> None:
        """Polyline

        This element is based on Three.js' `Line <https://threejs.org/docs/#api/en/objects/Line>`_ object.
        It connects a sequence of 3D points with line segments and optionally dashes them via
        `LineDashedMaterial <https://threejs.org/docs/#api/en/materials/LineDashedMaterial>`_.

        ``dash_size`` and ``gap_size`` defaults match the Three.js ``LineDashedMaterial`` defaults
        (``3.0`` and ``1.0``); the units are scene units, so adjust them for your scene scale.

        :param points: list of ``[x, y, z]`` points
        :param colors: optional list of per-vertex ``[r, g, b]`` colors (each component in ``[0, 1]``).
            When supplied, the line uses vertex colors instead of the material color.
        :param dashed: whether to use a dashed material (default: ``False``)
        :param dash_size: dash length in scene units (default: ``3.0``)
        :param gap_size: gap length in scene units (default: ``1.0``)
        """
        super().__init__('polyline', points, colors, dashed, dash_size, gap_size)
        if colors is not None:
            self.material(color=None)


class Lathe(Object3D):

    def __init__(self,
                 points: list[list[float]],
                 segments: int = 12,
                 phi_start: float = 0.0,
                 phi_length: float = 2 * math.pi,
                 wireframe: bool = False,
                 ) -> None:
        """Lathe

        This element is based on Three.js' `LatheGeometry <https://threejs.org/docs/#api/en/geometries/LatheGeometry>`_ object.
        It creates a surface of revolution by rotating a 2D polyline around the y axis.

        :param points: list of 2D ``[x, y]`` points making up the profile (x ≥ 0)
        :param segments: number of segments around the circumference (default: 12)
        :param phi_start: starting angle in radians (default: 0.0)
        :param phi_length: angular extent in radians (default: ``2π``)
        :param wireframe: whether to render the mesh as wireframe (default: ``False``)
        """
        super().__init__('lathe', points, segments, phi_start, phi_length, wireframe)


class ArrowHelper(Object3D):

    def __init__(self,
                 direction: list[float] = [0.0, 0.0, 1.0],  # noqa: B006
                 origin: list[float] = [0.0, 0.0, 0.0],  # noqa: B006
                 length: float = 1.0,
                 color: int = 0xffff00,
                 head_length: float | None = None,
                 head_width: float | None = None,
                 line_width: float = 1.0,
                 radial_segments: int = 16,
                 ) -> None:
        """Arrow Helper

        This element wraps Three.js' `ArrowHelper <https://threejs.org/docs/#api/en/helpers/ArrowHelper>`_ object.
        It is convenient for visualizing directions, forces, or velocities.

        ``line_width`` is forwarded to ``LineBasicMaterial.linewidth``, but most WebGL implementations
        clamp ``LineBasicMaterial.linewidth`` to ``1`` regardless of the value supplied; treat values
        ``> 1`` as a hint that browsers frequently ignore.

        :param direction: direction vector (will be normalized) (default: ``[0, 0, 1]``)
        :param origin: origin point (default: ``[0, 0, 0]``)
        :param length: arrow length (default: ``1.0``)
        :param color: arrow color as 24-bit hex integer (default: ``0xffff00``)
        :param head_length: cone head length (default: ``0.2 * length`` per Three.js)
        :param head_width: cone head base width (default: ``0.2 * head_length`` per Three.js)
        :param line_width: line thickness hint (default: ``1.0``; commonly ignored by browsers)
        :param radial_segments: number of segments around the cone head (default: ``16``)
        """
        # Mutable default lists are intentional read-only sentinels; ``noqa: B006`` per CONTRIBUTING.
        super().__init__('arrow_helper', direction, origin, length, color,
                         head_length, head_width, line_width, radial_segments)


class PolarGridHelper(Object3D):

    def __init__(self,
                 radius: float = 10.0,
                 sectors: int = 16,
                 rings: int = 8,
                 divisions: int = 64,
                 color1: int = 0x444444,
                 color2: int = 0x888888,
                 ) -> None:
        """Polar Grid Helper

        This element is based on Three.js' `PolarGridHelper <https://threejs.org/docs/#api/en/helpers/PolarGridHelper>`_ object.
        It draws a circular reference grid in the XZ plane (Three.js' default) — rotate or attach to
        a parent to align it with another plane.

        :param radius: outer radius of the grid (default: ``10.0``)
        :param sectors: number of angular sectors (default: ``16``)
        :param rings: number of concentric rings (default: ``8``)
        :param divisions: number of segments used to draw each ring (default: ``64``)
        :param color1: color of the central crosshair lines as 24-bit hex (default: ``0x444444``)
        :param color2: color of the rest of the grid as 24-bit hex (default: ``0x888888``)
        """
        super().__init__('polar_grid_helper', radius, sectors, rings, divisions, color1, color2)
