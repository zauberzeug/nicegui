import logging
import math
from typing import TYPE_CHECKING, List, Literal, Optional, Self

from .scene_object3d import Object3D

if TYPE_CHECKING:
    import cadquery as cq


class Group(Object3D):
    def __init__(self) -> None:
        """Group

        This element is based on Three.js' `Group <https://threejs.org/docs/index.html#api/en/objects/Group>`_ object.
        It is used to group objects together.
        """
        super().__init__("group")


class Box(Object3D):
    def __init__(
        self,
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
        super().__init__("box", width, height, depth, wireframe)


class Sphere(Object3D):
    def __init__(
        self,
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
        super().__init__("sphere", radius, width_segments, height_segments, wireframe)


class Cylinder(Object3D):
    def __init__(
        self,
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
        super().__init__("cylinder", top_radius, bottom_radius, height, radial_segments, height_segments, wireframe)


class Ring(Object3D):
    def __init__(
        self,
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
        super().__init__(
            "ring", inner_radius, outer_radius, theta_segments, phi_segments, theta_start, theta_length, wireframe
        )


class QuadraticBezierTube(Object3D):
    def __init__(
        self,
        start: List[float],
        mid: List[float],
        end: List[float],
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
        super().__init__(
            "quadratic_bezier_tube", start, mid, end, tubular_segments, radius, radial_segments, closed, wireframe
        )


class Extrusion(Object3D):
    def __init__(
        self,
        outline: List[List[float]],
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
        super().__init__("extrusion", outline, height, wireframe)


class Stl(Object3D):
    def __init__(
        self,
        url: str,
        wireframe: bool = False,
    ) -> None:
        """STL

        This element is used to create a mesh from an STL file.

        :param url: URL of the STL file
        :param wireframe: whether to display the STL as a wireframe (default: `False`)
        """
        super().__init__("stl", url, wireframe)


class Gltf(Object3D):
    def __init__(
        self,
        url: str,
    ) -> None:
        """GLTF

        This element is used to create a mesh from a glTF file.

        :param url: URL of the glTF file
        """
        super().__init__("gltf", url)


class Line(Object3D):
    def __init__(
        self,
        start: List[float],
        end: List[float],
    ) -> None:
        """Line

        This element is based on Three.js' `Line <https://threejs.org/docs/index.html#api/en/objects/Line>`_ object.
        It is used to create a line segment.

        :param start: start point of the line
        :param end: end point of the line
        """
        super().__init__("line", start, end)


class Curve(Object3D):
    def __init__(
        self,
        start: List[float],
        control1: List[float],
        control2: List[float],
        end: List[float],
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
        super().__init__("curve", start, control1, control2, end, num_points)


class Text(Object3D):
    def __init__(
        self,
        text: str,
        style: str = "",
    ) -> None:
        """Text

        This element is used to add 2D text to the scene.
        It can be moved like any other object, but always faces the camera.

        :param text: text to display
        :param style: CSS style (default: '')
        """
        super().__init__("text", text, style)


class Text3d(Object3D):
    def __init__(
        self,
        text: str,
        style: str = "",
    ) -> None:
        """3D Text

        This element is used to add a 3D text mesh to the scene.
        It can be moved and rotated like any other object.

        :param text: text to display
        :param style: CSS style (default: '')
        """
        super().__init__("text3d", text, style)


class Texture(Object3D):
    def __init__(
        self,
        url: str,
        coordinates: List[List[Optional[List[float]]]],
    ) -> None:
        """Texture

        This element is used to add a texture to a mesh.

        :param url: URL of the texture image
        :param coordinates: texture coordinates
        """
        super().__init__("texture", url, coordinates)

    def set_url(self, url: str) -> None:
        """Change the URL of the texture image."""
        self.args[0] = url
        self.scene.run_method("set_texture_url", self.id, url)

    def set_coordinates(self, coordinates: List[List[Optional[List[float]]]]) -> None:
        """Change the texture coordinates."""
        self.args[1] = coordinates
        self.scene.run_method("set_texture_coordinates", self.id, coordinates)


class SpotLight(Object3D):
    def __init__(
        self,
        color: str = "#ffffff",
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
        super().__init__("spot_light", color, intensity, distance, angle, penumbra, decay)


class PointCloud(Object3D):
    def __init__(
        self,
        points: List[List[float]],
        colors: Optional[List[List[float]]] = None,
        point_size: float = 1.0,
    ) -> None:
        """Point Cloud

        This element is based on Three.js' `Points <https://threejs.org/docs/index.html#api/en/objects/Points>`_ object.

        :param points: list of points
        :param colors: optional list of colors (one per point)
        :param point_size: size of the points (default: 1.0)
        """
        super().__init__("point_cloud", points, colors, point_size)
        if colors is not None:
            self.material(color=None)

    def set_points(self, points: List[List[float]], colors: Optional[List[List[float]]] = None) -> None:
        """Change the points and colors of the point cloud."""
        self.args[0] = points
        self.args[1] = colors
        self.scene.run_method("set_points", self.id, points, colors)
        if colors is not None:
            self.material(color=None)


class AxesHelper(Object3D):
    def __init__(
        self,
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
        super().__init__("axes_helper", length)


class Mesh(Object3D):
    def __init__(
        self,
        vertices: List[List[float]],
        triangles: List[List[int]],
        wireframe: bool = False,
        threshold_angle: Optional[float] = None,
        only_show_open_edges: bool = False,
    ) -> None:
        """Mesh

        This element is based on Three.js' `BufferGeometry <https://threejs.org/docs/#api/en/core/BufferGeometry>`_ object.
        It is used to create a mesh from vertices and triangles.

        :param vertices: list of vertex coordinates (e.g., [[x1, y1, z1], [x2, y2, z2], ...])
        :param triangles: list of triangle indices (e.g., [[0, 1, 2], [0, 2, 3], ...])
        :param wireframe: whether to display the mesh as a wireframe (default: `False`)
        :param threshold_angle: angle in degrees to determine sharp edges for display (default: `None`, meaning all edges of a wireframe are shown, or smooth shading for solid mesh)
        :param only_show_open_edges: if `True`, only edges that are not shared by two triangles are shown (default: `False`). This parameter only has an effect if `wireframe` is `True`.
        """
        super().__init__("mesh", vertices, triangles, wireframe, threshold_angle, only_show_open_edges)
        self.wireframe = wireframe


class FacetMesh(Object3D):
    def __init__(
        self,
        vertices: List[List[float]],
        triangles: List[List[int]],
        facets: Optional[int] = None,
        wireframe: bool = False,
        show_facets: bool = True,
        show_edges: bool = True,
    ) -> None:
        """Facet Mesh

        This element is based on Three.js' `BufferGeometry <https://threejs.org/docs/#api/en/core/BufferGeometry>`_ object.
        It is used to create a mesh from vertices and facets.

        :param vertices: list of vertex coordinates (e.g., [[x1, y1, z1], [x2, y2, z2], ...])
        :param triangles: list of triangles which are represented by 3 vertices each (e.g., [[0, 1, 2], [0, 2, 3], ...])
        :param facets: list of facets which are represented by a list of triangles with variable length (e.g., [[0, 1], [2, 3], ...]). If `None`, each triangle is its own facet.
        :param wireframe: whether to display the mesh as a wireframe (default: `False`)
        :param show_edges: whether to show edges of the facets (default: `True`)
        """
        super().__init__("group")  # Initialize FacetMesh as a group
        self.facet_meshes = []  # List to hold the individual meshes for each facet
        self.facet_edge_meshes = []  # List to hold the edge meshes for each facet
        if facets is None:
            facets = []
            for i in range(len(triangles)):
                facets.append([i])
        with self:  # Ensure 'self' (this FacetMesh group) is the current parent on the stack
            for facet_indices in facets:
                # Create each facet as a separate mesh;
                # it will automatically become a child of 'self' due to the 'with self:' context.
                if show_facets:
                    self.facet_meshes.append(
                        self.scene.mesh(vertices, [triangles[i] for i in facet_indices], wireframe)
                    )
                if show_edges:
                    self.facet_edge_meshes.append(
                        self.scene.mesh(
                            vertices,
                            [triangles[i] for i in facet_indices],
                            wireframe=True,
                            threshold_angle=0,
                            only_show_open_edges=True,
                        )
                    )
        self.wireframe = wireframe

    def material(
        self,
        color: Optional[str] = "#ffffff",
        opacity: float = 1.0,
        side: Literal["front", "back", "both"] = "front",
    ) -> Self:
        # Call the parent's material method to set material properties on the FacetMesh group itself.
        super().material(color, opacity, side)
        # Apply this material to all child meshes.
        # self.children is a property from Object3D that lists direct children.
        # self.color, self.opacity, self.side_ will be the values just set by super().material().
        for facet_mesh in self.facet_meshes:
            if hasattr(facet_mesh, "material") and callable(facet_mesh.material):  # Ensure child can have material
                facet_mesh.material(color=self.color, opacity=self.opacity, side=self.side_)
        return self

    def edge_material(self, color: Optional[str] = "#ffffff", opacity: float = 1.0) -> Self:
        for facet_edge_mesh in self.facet_edge_meshes:
            if hasattr(facet_edge_mesh, "material") and callable(facet_edge_mesh.material):
                facet_edge_mesh.material(color=color, opacity=opacity, side="both")
        return self


class CQShape(FacetMesh):
    def __init__(
        self,
        cq_object: "cq.Shape",
        tolerance: float = 0.1,
        angular_tolerance: float = 0.1,
        wireframe: bool = False,
        show_edges: bool = False,
    ) -> None:
        """CadQuery Shape

        This element renders a CadQuery shape by tessellating its faces and creating a FacetMesh.

        :param cq_object: The CadQuery shape to render (e.g., `cq.Workplane().box(1,1,1).val()`).
        :param tolerance: Tessellation tolerance (default: 0.1). Smaller values mean finer mesh.
        :param angular_tolerance: Tessellation angular tolerance in radians (default: 0.1).
        :param wireframe: Whether to display the facets as wireframes (default: `False`).
                         If True, only edges are shown (`show_edges` is forced to True), and facets themselves are not rendered.
        :param show_edges: Whether to show explicit edges for non-wireframe facets (default: `False`).
                           Ignored if `wireframe` is True (edges are always shown).

        """
        try:
            import cadquery as cq
        except ImportError as e:
            # Consider raising a more specific NiceGUI error or logging.
            # For now, re-raising to make it clear to the user.
            raise ImportError(
                "The 'cadquery' library is not installed. Please install it to use CQShape (e.g., pip install cadquery)."
            ) from e

        global_vertices = []
        global_triangles = []
        facets_data = []
        vertex_offset = 0

        faces_to_process = []
        if isinstance(cq_object, cq.Solid) or isinstance(cq_object, cq.Compound):
            faces_to_process = cq_object.Faces()
        elif isinstance(cq_object, cq.Face):
            faces_to_process = [cq_object]
        else:
            # Or log a warning and create an empty FacetMesh
            raise ValueError(f"Unsupported CadQuery object type: {type(cq_object)}. Expected Solid, Compound, or Face.")

        for cq_face in faces_to_process:
            try:
                face_tess = cq_face.tessellate(tolerance=tolerance, angularTolerance=angular_tolerance)
                if (
                    not face_tess or not face_tess[0] or not face_tess[1]
                ):  # Tessellation might return (None,None) or ([],[])
                    continue

                face_vertices_cq, face_triangles_local_indices = face_tess

                current_face_vertex_count = len(face_vertices_cq)
                for v_cq in face_vertices_cq:
                    global_vertices.append([v_cq.x, v_cq.y, v_cq.z])

                current_facet_global_triangle_indices = []
                for local_tri_indices in face_triangles_local_indices:
                    global_tri = [
                        local_tri_indices[0] + vertex_offset,
                        local_tri_indices[1] + vertex_offset,
                        local_tri_indices[2] + vertex_offset,
                    ]
                    global_triangles.append(global_tri)
                    current_facet_global_triangle_indices.append(len(global_triangles) - 1)

                if current_facet_global_triangle_indices:
                    facets_data.append(current_facet_global_triangle_indices)

                vertex_offset += current_face_vertex_count
            except Exception as e:
                logging.error(f"Error tessellating a CadQuery face: {e}")
                continue

        if not global_vertices and not global_triangles and not facets_data:
            # If no geometry was generated (e.g. empty shape or all faces failed)
            # Initialize with empty data to avoid errors in super().__init__
            # This will result in an empty group being created.
            logging.warning("No geometry generated from CadQuery object for CQShape.")
            global_vertices, global_triangles, facets_data = [], [], []

        _show_edges = show_edges  # Use a temporary variable to hold the intended show_edges value
        if wireframe:
            # If wireframe is True, edges should be shown, and facets should not.
            _show_edges = True

        # Call the FacetMesh constructor with the generated data
        super().__init__(
            vertices=global_vertices,
            triangles=global_triangles,
            facets=facets_data,
            wireframe=False,
            show_facets=not wireframe,
            show_edges=_show_edges,
        )


class CQAssembly(Object3D):
    def __init__(
        self,
        cq_assembly: "cq.Assembly",
        tolerance: float = 0.1,
        angular_tolerance: float = 0.1,
        wireframe: bool = False,
        show_edges: bool = False,
        parent: Optional[Object3D] = None,
    ) -> None:
        """CadQuery Assembly

        This element renders a CadQuery assembly by tessellating its components and creating a FacetMesh for each.

        :param cq_assembly: The CadQuery assembly to render (e.g., `cq.Assembly()`).
        :param tolerance: Tessellation tolerance (default: 0.1). Smaller values mean finer mesh.
        :param angular_tolerance: Tessellation angular tolerance in radians (default: 0.1).
        :param wireframe: Whether to display the facets as wireframes (default: `False`).
        :param show_edges: Whether to show explicit edges for non-wireframe facets (default: `False`).
                           If `wireframe` is True, this parameter's effect might be combined or overridden.

        """
        try:
            import cadquery as cq
        except ImportError as e:
            raise ImportError(
                "The 'cadquery' library is not installed. Please install it to use CQAssembly (e.g., pip install cadquery)."
            ) from e

        super().__init__("group")  # Initialize CQAssembly as a group
        self.cq_assembly = cq_assembly
        self.wireframe = wireframe  # Storing for potential future use or consistency, passed to children
        if parent is not None:
            self.parent = parent  # Optional parent Object3D, useful for scene hierarchy
        self.child_assemblies = []

        for assembly_item in cq_assembly.children:
            name = assembly_item.name
            color_tuple = (
                assembly_item.color.toTuple() if assembly_item.color else (0.8, 0.8, 0.8, 1.0)
            )  # Default color if None
            color_rgb = color_tuple[0:3]
            color_hex = f"#{int(color_rgb[0] * 255):02X}{int(color_rgb[1] * 255):02X}{int(color_rgb[2] * 255):02X}"
            opacity = color_tuple[3]

            # Extract translation from CadQuery Location
            # cq.Location.toTuple() returns ((x,y,z), (axis_x,axis_y,axis_z), angle_degrees)
            # We are primarily interested in the translation part for .move()
            loc_tuple = assembly_item.loc.toTuple()
            translation = loc_tuple[0] if loc_tuple and len(loc_tuple) > 0 else (0.0, 0.0, 0.0)
            # Rotation handling would require converting (axis, angle) to quaternion or Euler for Three.js
            # For now, only translation is applied directly via .move()

            child_obj = assembly_item.obj
            if (
                child_obj is None
            ):  # Indicates a nested assembly (assembly_item.obj is None, assembly_item itself is the cq.Assembly)
                nested_assembly_obj = self.scene.cq_assembly(
                    assembly_item,  # Pass the cq.Assembly child item
                    tolerance=tolerance,
                    angular_tolerance=angular_tolerance,
                    wireframe=wireframe,  # Pass down wireframe state
                    show_edges=show_edges,  # Pass down show_edges state
                    parent=self,  # Set current assembly as parent
                )
                if isinstance(translation, (list, tuple)) and len(translation) == 3:
                    nested_assembly_obj.move(*translation)  # Apply translation to the group
                # Note: Color/material of the group itself might not be directly applicable unless it overrides children.
                # CadQuery assemblies usually define colors on their leaf shapes.
                self.child_assemblies.append(nested_assembly_obj)

            elif isinstance(child_obj, (cq.Shape, cq.Solid, cq.Compound, cq.Face)):
                cq_shape_obj = self.scene.cq_shape(
                    child_obj,
                    tolerance=tolerance,
                    angular_tolerance=angular_tolerance,
                    wireframe=wireframe,  # Pass down wireframe state
                    show_edges=show_edges,
                )  # Pass down show_edges state
                if isinstance(translation, (list, tuple)) and len(translation) == 3:
                    cq_shape_obj.move(*translation)  # Apply translation
                cq_shape_obj.material(color=color_hex, opacity=opacity)  # Apply color and opacity
            else:
                logging.warning(f"Child '{name}' in CQAssembly is of an unhandled type: {type(child_obj)}. Skipping.")
