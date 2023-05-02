import bpy

class HS_PT_Panel(bpy.types.Panel):
    bl_label = "Hand Scan"
    bl_space_type = "PROPERTIES"
    bl_region_type = "WINDOW"
    bl_context = "modifier"

    def draw(self, context):
        scene = context.object
        layout = self.layout 

        layout.label(text="Generate hand armature")
        split_armature_gen = layout.split(align=True)
        col_l = split_armature_gen.column()
        col_l.operator("action.create_left_hand_mesh")
        col_r = split_armature_gen.column()
        col_r.operator("action.create_left_hand_mesh")

        row_capture_hands = layout.row()
        row_capture_hands.operator("action.capture_hands")