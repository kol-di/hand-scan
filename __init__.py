bl_info = {
    "name" : "HandScan",
    "author" : "koldi",
    "description" : "",
    "blender" : (2, 80, 0),
    "version" : (0, 0, 1),
    "location" : "",
    "warning" : "",
    "category" : "Generic"
}


import bpy

from .addon.operators import HS_OT_CreateLeftHandMesh
from .addon.panel import HS_PT_Panel

classes = (
    HS_OT_CreateLeftHandMesh, 
    HS_PT_Panel,
)

def register():
    for c in classes:
        bpy.utils.register_class(c)

def unregister():
    for c in classes:
        bpy.utils.unregister_class(c)
