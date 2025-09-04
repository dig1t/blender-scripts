import bpy
import os
from math import radians

# Define paths
obj_directory = "/Users/dig1t/Desktop/renders/obj"  # Directory with .obj files
output_directory = "/Users/dig1t/Desktop/renders/out"  # Directory for PNG output
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

# Set up camera
bpy.ops.object.camera_add(location=(0, -5, 2), rotation=(radians(75), 0, 0))
camera = bpy.context.object
bpy.context.scene.camera = camera

# Set up lighting
bpy.ops.object.light_add(type='SUN', location=(5, 5, 5))
light = bpy.context.object
light.data.energy = 5

# Function to center and scale object
def prepare_object(obj):
    # Select object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Center object at origin
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    obj.location = (0, 0, 0)

    # Scale to fit within camera view
    max_dim = max(obj.dimensions)
    if max_dim > 0:
        scale = 2.0 / max_dim  # Adjust scale to fit in frame
        obj.scale = (scale, scale, scale)

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
        bpy.ops.wm.obj_import(filepath=obj_path)

        # Prepare the imported object
        imported_obj = bpy.context.selected_objects[0]
        prepare_object(imported_obj)

        # Set output path for PNG
        output_path = os.path.join(output_directory, f"{os.path.splitext(filename)[0]}.png")
        bpy.context.scene.render.filepath = output_path

        # Render the scene
        bpy.ops.render.render(write_still=True)

        print(f"Rendered: {output_path}")

print("All .obj files processed!")