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
        split = layout.split()
        col_l = split.column()
        col_l.label(text="L")
        col_l.operator("action.create_left_hand_mesh")
        