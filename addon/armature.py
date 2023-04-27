from __future__ import annotations

import bpy
from math import radians
from mathutils import Vector, Quaternion

from dataclasses import dataclass
from typing import Optional




@dataclass
class Bone:
    name: str
    location: Vector
    rotation: Quaternion
    length: float
    parent: Optional[Bone] = None


def create_bones_data(orient: str):
    assert orient in ('L', 'R'), "Orientation can be either L or R"
    bones = []

    # base
    bones.append(bone_base := Bone("Base.{}".format(orient), Vector((0, 0, 0)), Quaternion((0, 0, 0), radians(0)), 1))
    #thumb
    bones.append(bone_thumb_0 := Bone("Thumb.0.{}".format(orient), Vector((1, 0, 1)), Quaternion((0, 1, 0), radians(30)), 1, bone_base))
    bones.append(bone_thumb_1 := Bone("Thumb.1.{}".format(orient), Vector((1, 0, 2)), Quaternion((0, 1, 0), radians(30)), 1, bone_thumb_0))
    bones.append(bone_thumb_2 := Bone("Thumb.2.{}".format(orient), Vector((1, 0, 3)), Quaternion((0, 1, 0), radians(30)), 1, bone_thumb_1))
    # ring
    bones.append(bone_index_0 := Bone("Index.0.{}".format(orient), Vector((1, 0, 1)), Quaternion((0, 0, 0), radians(0)), 1, bone_base))
    bones.append(bone_index_1 := Bone("Index.1.{}".format(orient), Vector((1, 0, 2)), Quaternion((0, 0, 0), radians(0)), 1, bone_index_0))
    bones.append(bone_index_2 := Bone("Index.2.{}".format(orient), Vector((1, 0, 3)), Quaternion((0, 0, 0), radians(0)), 1, bone_index_1))
    # middle
    bones.append(bone_middle_0 := Bone("Middle.0.{}".format(orient), Vector((0, 0, 1)), Quaternion((0, 0, 0), radians(0)), 1, bone_base))
    bones.append(bone_middle_1 := Bone("Middle.1.{}".format(orient), Vector((0, 0, 2)), Quaternion((0, 0, 0), radians(0)), 1, bone_middle_0))
    bones.append(bone_middle_2 := Bone("Middle.2.{}".format(orient), Vector((0, 0, 3)), Quaternion((0, 0, 0), radians(0)), 1, bone_middle_1))
    # ring
    bones.append(bone_ring_0 := Bone("Ring.0.{}".format(orient), Vector((-1, 0, 1)), Quaternion((0, 0, 0), radians(0)), 1, bone_base))
    bones.append(bone_ring_1 := Bone("Ring.1.{}".format(orient), Vector((-1, 0, 2)), Quaternion((0, 0, 0), radians(0)), 1, bone_ring_0))
    bones.append(bone_ring_2 := Bone("Ring.2.{}".format(orient), Vector((-1, 0, 3)), Quaternion((0, 0, 0), radians(0)), 1, bone_ring_1))
    # pinky
    bones.append(bone_pinky_0 := Bone("Pinky.0.{}".format(orient), Vector((-2, 0, 1)), Quaternion((0, 0, 0), radians(0)), 1, bone_base))
    bones.append(bone_pinky_1 := Bone("Pinky.1.{}".format(orient), Vector((-2, 0, 2)), Quaternion((0, 0, 0), radians(0)), 1, bone_pinky_0))
    bones.append(bone_pinky_2 := Bone("Pinky.2.{}".format(orient), Vector((-2, 0, 3)), Quaternion((0, 0, 0), radians(0)), 1, bone_pinky_1))

    return bones


def left_hand_armature(context: bpy.types.Context):

    # get new armature
    bpy.ops.object.armature_add(
        enter_editmode=True, 
        location=context.scene.cursor.location
    )
    armature = bpy.data.armatures[-1]
    if not armature.is_editmode:
        bpy.ops.object.mode_set(mode='EDIT')

    # init bone positions
    bones_data = create_bones_data(orient='L')

    # create edit_bones in armature
    for bone_data in bones_data:
        bone = armature.edit_bones.new(bone_data.name)
        bone.translate(bone_data.location)
        bone.length = bone_data.length
        bone.transform(bone_data.rotation.to_matrix())
        if bone_data.parent is not None:
            bone.parent = armature.edit_bones.get(
                bone_data.parent.name
            )
        bone.use_connect
