#!/usr/bin/env python3
import cadquery as cq

from nicegui import app, events, ui

app.add_static_files('/stl', 'static')


def hover_handle_creator():
    hover_dict = {}  # Stores original material properties of the currently hovered object

    def handle_hover(e: events.SceneHoverEventArguments):
        # Make a copy of current hovered objects to identify which ones are no longer hovered
        old_hover_dict = hover_dict.copy()

        if e.hits:
            for hit in e.hits:  # Iterate through all hits (though we usually only care about the first)
                name = hit.object_name or hit.object_id
                if hit.object_id in e.sender.objects:
                    obj = e.sender.objects[hit.object_id]

                    # Only apply hover effect to non-wireframe objects that have a material
                    if (
                        hasattr(obj, 'material')
                        and callable(obj.material)
                        and (not hasattr(obj, 'wireframe') or obj.wireframe is False)
                    ):
                        if hit.object_id in old_hover_dict:
                            # This object was already hovered, remove from old_hover_dict so it's not restored
                            del old_hover_dict[hit.object_id]

                        if hit.object_id not in hover_dict:
                            # New object hovered: store original material and apply hover material
                            original_props = {'color': obj.color, 'opacity': obj.opacity}
                            if isinstance(obj, (ui.scene.facetmesh, ui.scene.cq_shape)) and hasattr(obj, 'edge_color'):
                                original_props['edge_color'] = obj.edge_color
                            hover_dict[hit.object_id] = original_props

                            obj.material(color='#FFFF00', opacity=1.0)  # Highlight with yellow
                            # Example: Highlight edge material for facetmesh/cq_shape if desired
                            # if 'edge_color' in original_props and hasattr(obj, 'edge_material'):
                            #     obj.edge_material(color='#00FF00') # Highlight edges in green

                            print(f'Hovering on: {name} (type: {obj.__class__.__name__}, id: {obj.id})')
                        break  # Process only the first valid hit for hover effect

        # Restore material for objects that are no longer hovered
        for obj_id, original_props in old_hover_dict.items():
            if obj_id in e.sender.objects:  # Check if object still exists
                obj = e.sender.objects[obj_id]
                obj.material(color=original_props.get('color'), opacity=original_props.get('opacity'))
                if (
                    'edge_color' in original_props
                    and isinstance(obj, (ui.scene.facetmesh, ui.scene.cq_shape))
                    and hasattr(obj, 'edge_material')
                    and callable(obj.edge_material)
                ):
                    obj.edge_material(color=original_props.get('edge_color'))

                hover_dict.pop(obj_id, None)  # Remove from hover_dict if it exists

        # Fallback print if no specific object was highlighted but there were hits
        # (e.g. if all hits were wireframes or had no material method)
        if e.hits and not hover_dict and not old_hover_dict:
            name = e.hits[0].object_name or e.hits[0].object_id
            # ui.notify(f"Hover detected near: {name} at ({e.hits[0].x:.2f}, {e.hits[0].y:.2f}, {e.hits[0].z:.2f})")
            # The print statement inside the loop is more specific if an object is highlighted.

    return handle_hover


# Simple click handler for demonstration
def handle_click(e: events.SceneClickEventArguments):
    if e.hits:
        hit = e.hits[0]
        name = hit.object_name or hit.object_id
        ui.notify(f'Clicked on: {name}')


with ui.scene(width=1024, height=800, on_hover=hover_handle_creator(), on_click=handle_click) as scene:
    # Basic lighting and a reference object
    scene.spot_light(distance=100, intensity=0.2).move(-10, -10, 10)
    scene.stl('/stl/pikachu.stl').move(x=0, y=-5, z=0).scale(0.06).material(color='#FFFF00', opacity=0.8)

    # Define vertices for a cube
    vertices = [
        [-0.5, -0.5, -0.5],  # 0
        [0.5, -0.5, -0.5],  # 1
        [0.5, 0.5, -0.5],  # 2
        [-0.5, 0.5, -0.5],  # 3
        [-0.5, -0.5, 0.5],  # 4
        [0.5, -0.5, 0.5],  # 5
        [0.5, 0.5, 0.5],  # 6
        [-0.5, 0.5, 0.5],  # 7
    ]
    # Define triangles for the cube (two triangles per face)
    triangles = [
        [1, 0, 2],
        [2, 0, 3],  # bottom face
        [4, 5, 6],
        [4, 6, 7],  # top face
        [0, 1, 5],
        [0, 5, 4],  # front face
        [2, 3, 7],
        [2, 7, 6],  # back face
        [1, 2, 6],
        [1, 6, 5],  # right face
        [3, 0, 7],
        [7, 0, 4],  # left face
    ]

    cube_facets = [[0, 1], [2, 3], [4, 5], [6, 7], [8, 9], [10, 11]]  # Each original face is a facet

    scene.mesh(vertices, triangles).move(x=1.5, y=0, z=0).scale(0.5).material(
        '#00ff00', opacity=0.7
    )  # Solid green cube
    scene.mesh(vertices, triangles, wireframe=True, threshold_angle=45).move(x=1.5, y=1.5, z=0).scale(0.5).material(
        '#ff0000'
    )  # Wireframe red cube with 45 degree threshold
    scene.mesh(vertices, triangles[:6], wireframe=True, only_show_open_edges=True, threshold_angle=0).move(
        x=1.5, y=-1.5, z=0
    ).scale(0.5).material('#0000ff')  # Wireframe blue half-cube with open edges only
    scene.mesh(vertices, triangles[:6], wireframe=True, only_show_open_edges=False, threshold_angle=0).move(
        x=1.5, y=-3, z=0
    ).scale(0.5).material('#00ffff')  # Wireframe cyan half-cube with all edges

    ui.label('FacetMesh Examples:')
    # FacetMesh with edges shown (default)
    scene.facetmesh(vertices, triangles, cube_facets, show_edges=True).move(x=4, y=0, z=0).scale(0.5).material(
        '#FFA500'
    ).edge_material('#000000')  # FacetMesh with Edges
    # FacetMesh with edges hidden
    scene.facetmesh(vertices, triangles, cube_facets, show_edges=False).move(x=4, y=1.5, z=0).scale(0.5).material(
        '#FFC0CB'
    )  # FacetMesh no Edges

    ui.label('CadQuery CQShape Examples:')
    try:
        # Create CadQuery objects
        cq_box_with_hole = cq.Workplane('XY').box(1.0, 1.0, 1.0).faces('>Z').workplane().hole(0.5).val()
        cq_cylinder = cq.Workplane('XY').cylinder(height=1.5, radius=0.3, centered=(True, True, False)).val()
        cq_sphere = cq.Workplane('XY').sphere(radius=0.6).val()

        # CQShape: Solid (default)
        scene.cq_shape(cq_box_with_hole).move(x=-3, y=0, z=0.5).material(
            '#FFBF00', opacity=0.8
        )  # CQShape Solid BoxHole

        # CQShape: Wireframe (show_facets=False, show_edges=True internally for CQShape when wireframe=True)
        scene.cq_shape(cq_box_with_hole, wireframe=True).move(x=-3, y=-1.5, z=0.5).material(
            '#FFBF00'
        )  # CQShape Wireframe BoxHole ; Color applies to edges

        # CQShape: Solid with Edges (show_facets=True, show_edges=True)
        scene.cq_shape(cq_box_with_hole, wireframe=False, show_edges=True).move(x=-3, y=-3, z=0.5).material(
            '#FFBF00', opacity=0.7
        ).edge_material('#333333')  # CQShape Solid+Edges BoxHole

        ui.label('CadQuery CQAssembly Examples:')
        # CQAssembly: Solid parts
        assembly_solid = cq.Assembly(name='Solid_Assembly')
        assembly_solid.add(cq_sphere, name='Sphere_Red', color=cq.Color('red'))
        assembly_solid.add(cq_cylinder, name='Cylinder_Blue', color=cq.Color('blue'))
        scene.cq_assembly(assembly_solid)  # CQAssembly Solid

        # CQAssembly: Solid with Edges
        assembly_solid_edges = cq.Assembly(name='Solid_Edges_Assembly')
        assembly_solid_edges.add(
            cq_sphere,
            name='Sphere_Yellow_SolidEdge',
            color=cq.Color(1, 1, 0, 0.7),
            loc=cq.Location(cq.Vector(0, 1.5, 0)),
        )  # Yellow, slightly transparent
        assembly_solid_edges.add(
            cq_cylinder,
            name='Cylinder_Cyan_SolidEdge',
            color=cq.Color(0, 1, 1, 0.7),
            loc=cq.Location(cq.Vector(0, 1.0, 0)),
        )
        # CQAssembly: Solid with Edges. 'show_edges=True' makes constituent CQShapes show their edges.
        # Edge material for assembly parts is inherited or can be set if building the assembly manually (see below).
        scene.cq_assembly(assembly_solid_edges, wireframe=False, show_edges=True)  # CQAssembly Solid+Edges

    except ImportError:
        ui.label('CadQuery library not found. Skipping cq_shape example.')
    except Exception as e:
        ui.label(f'Error in cq_shape example: {e}')


ui.run()
