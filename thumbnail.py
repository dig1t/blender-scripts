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
bpy.context.scene.render.resolution_x = 512  # Icon size
bpy.context.scene.render.resolution_y = 512
bpy.context.scene.render.resolution_percentage = 100

# Set up camera for isometric view
bpy.ops.object.camera_add(location=(10, -10, 10), rotation=(radians(60), 0, radians(45)))
camera = bpy.context.object
bpy.context.scene.camera = camera

# Professional product photoshoot lighting setup

# Key Light: Main light source (front-right, 45 degrees)
bpy.ops.object.light_add(type='AREA', location=(5, 5, 4))
key_light = bpy.context.object
key_light.data.type = 'AREA'
key_light.data.energy = 2000  # Strong key light
key_light.data.color = (1.0, 0.98, 0.95)  # Slightly warm daylight
key_light.data.size = 8  # Large soft light source
key_light.data.size_y = 8
key_light.data.use_shadow = False

# Fill Light: Softer light to fill shadows (front-left, lower intensity)
bpy.ops.object.light_add(type='AREA', location=(-4, 4, 2))
fill_light = bpy.context.object
fill_light.data.type = 'AREA'
fill_light.data.energy = 800  # Softer fill light
fill_light.data.color = (0.98, 0.99, 1.0)  # Slightly cool fill
fill_light.data.size = 6
fill_light.data.size_y = 6
fill_light.data.use_shadow = False

# Rim Light: Back light to separate subject from background (back-left)
bpy.ops.object.light_add(type='AREA', location=(-6, -6, 3))
rim_light = bpy.context.object
rim_light.data.type = 'AREA'
rim_light.data.energy = 1200  # Bright rim light
rim_light.data.color = (1.0, 1.0, 1.0)  # Pure white
rim_light.data.size = 4
rim_light.data.size_y = 4
rim_light.data.use_shadow = False

# Background Light: Subtle light for background separation
bpy.ops.object.light_add(type='AREA', location=(0, -8, 1))
bg_light = bpy.context.object
bg_light.data.type = 'AREA'
bg_light.data.energy = 600  # Subtle background light
bg_light.data.color = (0.95, 0.97, 1.0)  # Cool background tone
bg_light.data.size = 10
bg_light.data.size_y = 10
bg_light.data.use_shadow = False

# Top Light: Overhead light for even illumination
bpy.ops.object.light_add(type='AREA', location=(0, 0, 8))
top_light = bpy.context.object
top_light.data.type = 'AREA'
top_light.data.energy = 1000  # Moderate overhead
top_light.data.color = (1.0, 0.99, 0.97)  # Natural overhead
top_light.data.size = 12
top_light.data.size_y = 12
top_light.data.use_shadow = False

# Front-Left Shadow Fill: Additional light to eliminate shadow blob
bpy.ops.object.light_add(type='AREA', location=(-2, 3, 1))
shadow_fill = bpy.context.object
shadow_fill.data.type = 'AREA'
shadow_fill.data.energy = 1200  # Bright enough to eliminate shadow
shadow_fill.data.color = (1.0, 0.99, 0.98)  # Warm fill to match key light
shadow_fill.data.size = 5
shadow_fill.data.size_y = 5
shadow_fill.data.use_shadow = False

# Camera Light: Wide radius light from camera position
bpy.ops.object.light_add(type='AREA', location=(10, -10, 10))
camera_light = bpy.context.object
camera_light.data.type = 'AREA'
camera_light.data.energy = 1500  # Bright camera flash
camera_light.data.color = (1.0, 1.0, 1.0)  # Pure white camera flash
camera_light.data.size = 15  # Very wide radius
camera_light.data.size_y = 15
camera_light.data.use_shadow = False

# Bottom Up Light: Soft upward illumination from below
bpy.ops.object.light_add(type='AREA', location=(0, 0, -3))
bottom_light = bpy.context.object
bottom_light.data.type = 'AREA'
bottom_light.data.energy = 300  # Low brightness for soft effect
bottom_light.data.color = (1.0, 0.99, 0.98)  # Soft warm tone
bottom_light.data.size = 20  # Big radius for wide coverage
bottom_light.data.size_y = 20
bottom_light.data.use_shadow = False

# Add ambient light for fill
bpy.ops.object.light_add(type='AREA', location=(0, 0, 0))
ambient = bpy.context.object
ambient.data.type = 'AREA'
ambient.data.energy = 500  # Overall scene lighting boost
ambient.data.color = (0.95, 0.95, 0.85)  # Soft pastel yellow ambient
ambient.data.size = 10  # Width of the area light
ambient.data.size_y = 10  # Height of the area light
ambient.data.use_shadow = False

# Function to center and scale object
def prepare_object(obj):
    # Select object
    bpy.ops.object.select_all(action='DESELECT')
    obj.select_set(True)
    bpy.context.view_layer.objects.active = obj

    # Center object at origin based on bounding box
    bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='BOUNDS')
    obj.location = (0, 0, 1)  # Centered at origin with Z offset

    # Reset rotation to ensure consistent orientation
    # obj.rotation_euler = (0, 0, 0)

    # Scale to fit within camera view
    max_dim = max(obj.dimensions.x, obj.dimensions.y, obj.dimensions.z)
    if max_dim > 0:
        scale = 6.0 / max_dim  # Increased from 4.0 to 6.0 for 1.5x zoom
        obj.scale = (scale, scale, scale)
    else:
        print(f"Warning: Object {obj.name} has zero dimensions, skipping scaling.")

    # Add default material to ensure visibility
    if not obj.data.materials:
        mat = bpy.data.materials.new(name="Default")
        mat.use_nodes = True
        bsdf = mat.node_tree.nodes.get("Principled BSDF")
        bsdf.inputs['Base Color'].default_value = (1, 1, 1, 1.0)  # White
        obj.data.materials.append(mat)

# Loop through .obj files
for filename in os.listdir(obj_directory):
    if filename.endswith(".obj"):
        # Clear scene objects (except camera and lights)
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
        cam_z = max(imported_obj.dimensions) * 1.33  # Reduced from 2 to 1.33 for 1.5x zoom
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