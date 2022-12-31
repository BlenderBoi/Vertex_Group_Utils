import bpy
from . VGU_Operators import *
from . VGU_UI_Panel import *


class VGU_MT_PIE_MENU(bpy.types.Menu):
    bl_idname = "VGU_MT_Pie_Menu"
    bl_label = "Vertex Group Utility"

    def draw(self, context):

        layout = self.layout

        item = context.object.vertex_groups.active
        obj = context.object





        pie = layout.menu_pie()
        if len(context.object.vertex_groups) > 0:

            pie.operator("vgu.panel_new_vertexgroup", text="New Vertex Group", icon="PLUS")
            pie.operator("vgu.panel_remove", text="Remove Vertex Group", icon="TRASH")
            pie.operator("vgu.panel_solo", text="Solo Active", icon="SOLO_ON").index = item.index
            pie.operator("vgupie.call_active_group_menu", text="Set Active Group", icon="LAYER_ACTIVE")

            pie.operator("vgu.panel_assign", text="Assign to Active", icon="ADD").index = item.index
            pie.operator("vgu.panel_unassign", text="Unassign from Active", icon="REMOVE").index = item.index
            pie.operator("vgu.panel_visibility_toogle", text="Hide/Unhide Active", icon="HIDE_OFF").index = item.index
            pie.operator("vgu.panel_selection_toogle", text="Select/Deselect Active", icon="RESTRICT_SELECT_OFF").index = item.index

            pie.separator()
            pie.separator()

        else:
            pie.operator("vgu.panel_new_vertexgroup", text="New Vertex Group", icon="PLUS")
            # pie.operator("vgu.panel_split_loose_to_vertex_group", text="Loose Mesh to Group", icon="SNAP_VERTEX")
            # pie.operator("vgu.panel_join_as_vertex_group", text="Join as Group", icon="OUTLINER_DATA_MESH")
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            # pie.operator("vgu.panel_vertex_group_from_side", text="Group From Side", icon="SNAP_VERTEX")
            # pie.operator("vgu.panel_vertex_group_from_material", text="Group From Material", icon="SNAP_VERTEX")
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()
            pie.separator()

        other = pie.column()
        gap = other.column()
        gap.separator()
        gap.scale_y = 7
        other_menu = other.box().column()
        other_menu.scale_y=1.3
        other_menu.operator("vgu.call_vg_list", text = "Vertex Group Panel",icon = "BLENDER")
        other_menu.separator()
        other_menu.operator("vgu.panel_join_as_vertex_group", text="Join as Group", icon="OUTLINER_DATA_MESH")
        other_menu.separator()
        other_menu.operator("vgu.panel_split_loose_to_vertex_group", text="Loose Mesh to Group", icon="SNAP_VERTEX")
        other_menu.operator("vgu.panel_vertex_group_from_side", text="Group From Side", icon="SNAP_VERTEX")
        other_menu.operator("vgu.panel_vertex_group_from_material", text="Group From Material", icon="SNAP_VERTEX")

        other_menu.separator()
        other_menu.operator("vgu.panel_remove_empty_vertexgroup", text="Empty Group", icon="TRASH")

        other_menu.separator()
        other_menu.operator("vgu.panel_separate_all_vertexgroup", text="Separate All", icon="MOD_EXPLODE")
        other_menu.operator("vgu.panel_batch_rename_group", text="Find and Replace", icon="ZOOM_ALL")
        other_menu.operator("vgu.panel_merge_vertex_group", text="Merge Group", icon="AUTOMERGE_ON")



class VGU_OT_CALL_PIE(bpy.types.Operator):

    bl_idname = "vgu.call_pie"
    bl_label = "Vertex Group Utils"


    def execute(self, context):

        if context.object:
            bpy.ops.wm.call_menu_pie(name="VGU_MT_Pie_Menu")

        return {'FINISHED'}



class VGU_OT_CALL_VG_Panel(bpy.types.Operator):

    bl_idname = "vgu.call_vg_list"
    bl_label = "VGU Panel"


    def execute(self, context):

        if context.object:
            bpy.ops.wm.call_panel(name="VERTEXGROUPUTILS_PT_list_panel_DATA")

        return {'FINISHED'}






addon_keymaps=[]









classes = [VGU_MT_PIE_MENU, VGU_OT_CALL_PIE, VGU_OT_CALL_VG_Panel]

def register():

    for cls in classes:
        bpy.utils.register_class(cls)


    # wm = bpy.context.window_manager
    # kc = wm.keyconfigs.addon

    # if kc:
    #     km = kc.keymaps.new(name="3D View", space_type="VIEW_3D")
    #     kmi = km.keymap_items.new("vgu.call_pie", type="F", value="PRESS", shift=True)

    #     addon_keymaps.append((km, kmi))




def unregister():

    # for km, kmi in addon_keymaps:
    #     km.keymap_items.remove(kmi)
    # addon_keymaps.clear()


    for cls in classes:
        bpy.utils.unregister_class(cls)




if __name__ == "__main__":
    register()
