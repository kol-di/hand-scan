import bpy

from .armature import create_hand_armature, create_bones_data
from ui.camera import display


def output(context):
    for ob in context.scene.objects:
        print(ob)


class HS_OT_CreateLeftHandMesh(bpy.types.Operator):
    bl_idname = "action.create_left_hand_mesh"
    bl_label = "L"
    bl_options = {"REGISTER", "UNDO"}

    # @classmethod
    # def poll(cls, context):
    #     """Verify if we can run the operation"""
    #     return context.active_object is not None

    def execute(self, context):
        # bpy.ops.mesh.primitive_cube_add()
        bones_data = create_bones_data('L')
        create_hand_armature(context, bones_data)
        output(context)
        return {'FINISHED'}
    

class HS_OT_CaptureHands(bpy.types.Operator):
    bl_idname = "action.capture_hands"
    bl_label = "Capture Hands"
    
    def execute(self, context):
        display()
        return {'FINISHED'}
    