import bpy


def left_hand_armature(context):
    # armature = bpy.data.armatures.new("Armature")
    # rig = bpy.data.objects.new("Armature", armature)
    # context.view_layer.objects.active = rig
    # if bpy.ops.object.mode_set.poll():
    #     bpy.ops.object.mode_set(mode='EDIT')
    # # armature.select = True
    # bpy.ops.object.editmode_toggle()

    bpy.ops.object.armature_add(
        enter_editmode=True, 
        location=context.scene.cursor.location
    )
    armature = bpy.data.armatures[-1]
    if not armature.is_editmode:
        bpy.ops.object.mode_set(mode='EDIT')
    

    bone_parent = armature.edit_bones[0]

    bone_base = armature.edit_bones.new("L.Base Bone")
    bone_base.head = [0, 0, 0]
    bone_base.tail = [0, 0, 10]

    bone_base.parent = bone_parent
    bone_base.use_connect
    # bone_base.head = context.scene.cursor.location
