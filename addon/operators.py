import bpy

from .armature import left_hand_armature


def output(context):
    for ob in context.scene.objects:
        print(ob)


class HS_OT_CreateLeftHandMesh(bpy.types.Operator):
    bl_idname = "action.create_left_hand_mesh"
    bl_label = "Hand Scan"
    bl_options = {"REGISTER", "UNDO"}

    # @classmethod
    # def poll(cls, context):
    #     """Verify if we can run the operation"""
    #     return context.active_object is not None

    def execute(self, context):
        # bpy.ops.mesh.primitive_cube_add()
        left_hand_armature(context)
        output(context)
        return {'FINISHED'}
