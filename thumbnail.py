import bpy
import os
from math import radians
import mathutils

# Define paths
obj_directory = "/Users/dig1t/Git/blender-scripts/obj"  # Directory with .obj files
output_directory = "/Users/dig1t/Git/blender-scripts/out"  # Directory for PNG output
os.makedirs(output_directory, exist_ok=True)

# Clear existing scene
bpy.ops.wm.read_factory_settings(use_empty=True)

# Set up rendering settings
bpy.context.scene.render.image_settings.file_format = 'PNG'
bpy.context.scene.render.image_settings.color_mode = 'RGBA'  # Enable alpha channel
bpy.context.scene.render.film_transparent = True  # Enable transparent background
bpy.context.scene.render.resolution_x = 256  # Icon size
bpy.context.scene.render.resolution_y = 256
bpy.context.scene.render.resolution_percentage = 100

# Set up camera for isometric view
bpy.ops.object.camera_add(location=(10, -5, 10), rotation=(radians(0), 0, radians(0)))
camera = bpy.context.object
bpy.context.scene.camera = camera

# Set up lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
light = bpy.context.object
light.data.energy = 5
light.data.use_shadow = False  # Disable shadows for cleaner render

# Function to center and scale object
def prepare_object(obj):
    # Select object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Center object at origin based on bounding box
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    obj.location = (0, 0, 1)

    # Reset rotation to ensure consistent orientation
    # obj.rotation_euler = (0, 0, 0)

    # Scale to fit within camera view
    max_dim = max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z)
    if max_dim > 0:
        scale = 4.0 / max_dim  # Adjusted for better centering and visibility
        obj.scale = (scale, scale, scale)
    else:
        print(f"Warning: Object {obj.name} has zero dimensions, skipping scaling.")

    # Add default material to ensure visibility
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Default")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (1,1,1, 1.0)  # Light gray
        obj.data.materials.append(mat)

# Loop through .obj files
for filename in os.listdir(obj_directory):
    if filename.endswith(".obj"):
        # Clear scene objects (except camera and light)
        bpy.ops.object.select_all(action='DESELECT')
        for obj in bpy.context.scene.objects:
            if obj.type not in ['CAMERA', 'LIGHT']:
                obj.select_set(True)
        bpy.ops.object.delete()

        # Import .obj file
        obj_path = os.path.join(obj_directory, filename)
        try:
            bpy.ops.wm.obj_import(filepath=obj_path)
        except Exception as e:
            print(f"Error importing {filename}: {e}")
            continue

        # Check if an object was imported
        if not bpy.context.selected_objects:
            print(f"Error: No objects imported from {filename}")
            continue

        # Prepare the imported object
        imported_obj = bpy.context.selected_objects[0]
        prepare_object(imported_obj)

        # Frame the object in the camera
        bpy.ops.object.select_all(action='DESELECT')
        imported_obj.select_set(True)
        bpy.ops.view3d.camera_to_view_selected()

        # Adjust camera distance to ensure model fits
        cam_z = max(imported_obj.dimensions) * 2  # Dynamic distance based on model size
        camera.location = (cam_z, -cam_z, cam_z)
        camera.rotation_euler = (radians(60), 0, radians(45))

        # Set output path for PNG
        output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.png")
        bpy.context.scene.render.filepath = output_path

        # Render the scene
        try:
            bpy.ops.render.render(write_still=True)
            print(f"Rendered: {output_path}")
        except Exception as e:
            print(f"Error rendering {filename}: {e}")

print("All .obj files processed!")