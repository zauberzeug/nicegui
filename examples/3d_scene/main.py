#!/usr/bin/env python3
import cadquery as cq
from nicegui import app, ui, events

app.add_static_files('/stl', 'static')

def hover_handle_creator():
    hover_dict = {}
    def handle_hover(e: events.SceneHoverEventArguments):
        old_hover_dict = hover_dict.copy()
        if e.hits:
            for hit in e.hits:
                name = hit.object_name or hit.object_id
                if hit.object_id in e.sender.objects:
                    obj = e.sender.objects[hit.object_id]
                    if hasattr(obj,'wireframe') and obj.wireframe == False:
                        if hit.object_id in old_hover_dict:
                            del old_hover_dict[hit.object_id]
                        if hit.object_id not in hover_dict:
                            hover_dict[hit.object_id] = {'color':obj.color,'opacity':obj.opacity}
                            if isinstance(obj, ui.scene.facetmesh):
                                hover_dict[hit.object_id]['edge_color'] = obj.edge_color
                            obj.material('#fff000')
                            # if isinstance(obj, ui.scene.facetmesh):
                            #     obj.edge_material('#0ff0ff')
                            print(obj)
                        break
        for obj_id in old_hover_dict:
            obj = e.sender.objects[obj_id]
            obj.material(color=hover_dict[obj_id]['color'], opacity=hover_dict[obj_id]['opacity'])
            # if isinstance(obj, ui.scene.facetmesh):
            #     obj.edge_material(color=hover_dict[obj_id]['edge_color'])
            del hover_dict[obj_id]
                #print(f'You hovered on the {name} at ({hit.x:.2f}, {hit.y:.2f}, {hit.z:.2f})')
    return handle_hover


with ui.scene(width=1024, height=800, on_hover=hover_handle_creator(), on_click=hover_handle_creator()) as scene:
    
    scene.spot_light(distance=100, intensity=0.1).move(-10, 0, 10)
    scene.stl('/stl/pikachu.stl').move(x=-0.5).scale(0.06)

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
        [0, 1, 2], [0, 2, 3],  # bottom face
        [4, 5, 6], [4, 6, 7],  # top face
        [0, 1, 5], [0, 5, 4],  # front face
        [2, 3, 7], [2, 7, 6],  # back face
        [1, 2, 6], [1, 6, 5],  # right face
        [0, 3, 7], [7, 0, 4],  # left face
    ]

    facets = [ [0,1], [2,3], [4,5], [6,7], [8,9], [10,11] ]
    scene.mesh(vertices, triangles).move(x=1.5, y=0, z=0).scale(0.5).material('#00ff00')
    scene.mesh(vertices, triangles, wireframe=True, threshold_angle=100).move(x=1.5, y=1, z=0).scale(0.5).material('#ff0000')
    
    scene.mesh(vertices, triangles[:4],wireframe=True,only_show_open_edges=True,threshold_angle=0).move(x=1.5, y=-2, z=0).scale(0.5).material('#00ff00')
    
    scene.mesh(vertices, triangles[:4],wireframe=True,only_show_open_edges=False,threshold_angle=0).move(x=1.5, y=-3, z=0).scale(0.5).material('#00ff00')
    scene.facetmesh(vertices, triangles,facets,show_edges=True).move(x=3.5, y=0, z=0).scale(0.5).material('#00ff00').edge_material('#ff0000')

    # Example of CQShape
    try:
        # Create a CadQuery object (e.g., a box with a hole)
        cq_obj = cq.Workplane("XY").box(1.0, 1.0, 1.0).faces(">Z").workplane().hole(0.5)
        cq_obj_2 = cq.Workplane("XY").cylinder(0.75, 1.5, centered=(True, True, False)) # Another example
        cq_obj_3 = cq.Workplane("XY").sphere(0.75) # Another example

        # Render with default (solid)
        scene.cq_shape(cq_obj.val()).move(x=-2, y=0, z=0.5).material('#FFBF00')

        # Render as wireframe (full wireframe, as FacetMesh does not currently pass only_show_open_edges to its main facets)
        scene.cq_shape(cq_obj.val(), wireframe=True, show_edges=True).move(x=-2, y=-1.5, z=0.5).material('#FFBF00')
        
        # Render as solid with highlighted open edges (using FacetMesh's show_edges=True)
        scene.cq_shape(cq_obj.val(), wireframe=False, show_edges=True).move(x=-2, y=-3, z=0.5).material('#FFBF00').edge_material("black")
        
        cq_assembly = cq.Assembly()
        cq_assembly.add(cq_obj_3.val(), name="box_with_hole", color=cq.Color('red'))
        #scene.cq_shape(cq_obj_3.val()).material('#0FBFF0')
        cq_assembly.add(cq_obj_2.val(), name="cylinder", color=cq.Color('blue'))
        #scene.cq_shape(cq_obj_2.val()).material('#0FBFF0')

        scene.cq_assembly(cq_assembly)

    except ImportError:
        ui.label("CadQuery library not found. Skipping cq_shape example.")
    except Exception as e:
        ui.label(f"Error in cq_shape example: {e}")


ui.run()
