import bpy
from . import VGU_Operators
from . import VGU_Preferences
from . import utility_function


def draw_ui_list(self, context, layout, data, item, icon, active_data, active_propname, emboss_name=False):

    ob = data
    vgroup = item

    row = layout.row(align=True)

    preferences = utility_function.get_addon_preferences(context)


    if preferences.SoloIcon:
        row.operator("vgu.panel_solo", text="", icon="SOLO_ON").index = item.index

    if preferences.VisibilityIcon:

        row.operator("vgu.panel_visibility_toogle", text="", icon="HIDE_OFF").index = item.index

    if context.mode == "EDIT_MESH":
        if preferences.SelectionIcon:
            row.operator("vgu.panel_selection_toogle", text="", icon="RESTRICT_SELECT_OFF").index = item.index

    if preferences.SetPivotIcon:
        row.operator("vgu.panel_set_origin", text="", icon="OBJECT_ORIGIN").index = item.index

    row.prop(vgroup, "name", text="", emboss=emboss_name, icon_value=icon)

    if preferences.LockWeightIcon:
        icon = 'LOCKED' if vgroup.lock_weight else 'UNLOCKED'
        row.prop(vgroup, "lock_weight", text="", icon=icon, emboss=False)

    if preferences.LockAllButThis:
        row.operator("vgu.lock_all_weight_but_this", text="",icon="MARKER_HLT").index = item.index 


    if preferences.AddModifierIcon:
        row.operator("vgu.panel_addmodifier", text="", icon="MODIFIER").index = item.index

    if preferences.SeperateIcon:
        row.operator("vgu.panel_seperate", text="", icon="MOD_BOOLEAN").index = item.index

    if context.mode == "EDIT_MESH":
        if preferences.AssignIcon:
            row.operator("vgu.panel_assign", text="", icon="ADD").index = item.index

    if context.mode == "EDIT_MESH":
        if preferences.UnassignIcon:
            row.operator("vgu.panel_unassign", text="", icon="REMOVE").index = item.index

    if preferences.RemoveIcon:
        row.operator("vgu.panel_remove", text="", icon="TRASH").index = item.index




class VGU_UL_VertexGroup_List(bpy.types.UIList):


    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        draw_ui_list(self, context, layout, data, item, icon, active_data, active_propname, emboss_name=False)

class VGU_UL_VertexGroup_Pie_List(bpy.types.UIList):


    def draw_item(self, context, layout, data, item, icon, active_data, active_propname):

        draw_ui_list(self, context, layout, data, item, icon, active_data, active_propname, emboss_name=True)



def draw_panels(layout, context, emboss_name):
    

    obj = context.object

    preferences = utility_function.get_addon_preferences(context)

    row=layout.row()

    if obj:
        if context.object.type == "MESH":


            if emboss_name:
                row.template_list("VGU_UL_VertexGroup_Pie_List", "", obj, "vertex_groups", obj.vertex_groups, "active_index")
            else:
                row.template_list("VGU_UL_VertexGroup_List", "", obj, "vertex_groups", obj.vertex_groups, "active_index")


            col = row.column(align=True)
            col.operator("object.vertex_group_add", icon='ADD', text="")
            props = col.operator("object.vertex_group_remove", icon='REMOVE', text="")
            props.all_unlocked = props.all = False

            col.separator()

            col.menu("MESH_MT_vertex_group_context_menu", icon='DOWNARROW_HLT', text="")

            col.menu("VGU_MT_icon_expose", text="",icon="VIS_SEL_11")

            col.separator()

            col.operator("object.vertex_group_move", icon='TRIA_UP', text="").direction = 'UP'
            col.operator("object.vertex_group_move", icon='TRIA_DOWN', text="").direction = 'DOWN'

            row = layout.row()
    
            # row.prop(context.space_data.overlay,"show_weight" )

            row = layout.row(align=True)
            row.prop(context.scene.tool_settings, "vertex_group_weight", text="Weight")

            row = layout.row(align=True)
            row.operator("vgu.panel_new_vertexgroup", text="New", icon="PLUS").weight = context.scene.tool_settings.vertex_group_weight
            row.operator("object.vertex_group_remove", text="Remove", icon="TRASH")


            row = layout.row(align=True)
            if len(obj.vertex_groups) > 0:
                if obj.vertex_groups.active_index >= 0 and obj.vertex_groups.active_index < len(obj.vertex_groups):
                    if context.mode == "EDIT_MESH":
                        reassign = row.operator("vgu.panel_assign", text="Assign", icon="ADD")
                        reassign.weight = context.scene.tool_settings.vertex_group_weight
                        reassign.index = obj.vertex_groups.active_index


                        row.operator("object.vertex_group_remove_from", text="Unassign", icon="REMOVE")

                        layout.separator()
                        layout.operator("object.vertex_group_remove_from", text="Unassign from all", icon="REMOVE").use_all_groups=True
                    layout.operator("vgu.unhide_all_visibility", text="Unhide All", icon="HIDE_OFF")




class VGU_PT_Vertex_Group_List_SIDE(bpy.types.Panel):

    bl_label = "Vertex Group List"
    bl_idname = "VERTEXGROUPUTILS_PT_list_panel_SIDE"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vertex Group Utils"

    @classmethod
    def poll(cls, context):
        preferences = utility_function.get_addon_preferences(context)
        if preferences.Vertex_Group_List_Side_Panel:
            if context.object:
                if context.object.type == "MESH":
	                return True


    def draw(self, context):

        layout = self.layout
        emboss_name = False
        draw_panels(layout, context, emboss_name)

        layout.prop(context.space_data.overlay,"show_weight" )


class VGU_PT_Vertex_Group_List_DATA(bpy.types.Panel):

    bl_label = "Vertex Group List"
    bl_idname = "VERTEXGROUPUTILS_PT_list_panel_DATA"
    bl_space_type = 'PROPERTIES'
    bl_region_type = 'WINDOW'
    bl_context = "data"


    @classmethod
    def poll(cls, context):
        preferences = utility_function.get_addon_preferences(context)
        if preferences.Vertex_Group_List_Data_Panel:
            if context.object:
                if context.object.type == "MESH":
	                return True


    def draw(self, context):

        layout = self.layout
        emboss_name = True 
        draw_panels(layout, context, emboss_name)


def draw_tools(layout, context):

    if context.object:
        if context.object.type == "MESH":

            layout.label(text="Clean Up")
            layout.operator("vgu.panel_remove_empty_vertexgroup", text="Empty Group", icon="TRASH")
            layout.operator("vgu.panel_unassign_zero_weight_from_all_group", text="Remove Zero Weights from Group", icon="REMOVE").index = context.object.vertex_groups.active_index

            layout.separator()
            layout.label(text="Groups")

            row = layout.row()
            if context.mode == "OBJECT":
                row.operator("vgu.panel_join_as_vertex_group", text="Join as Group", icon="OUTLINER_DATA_MESH")

            row.operator("vgu.panel_split_loose_to_vertex_group", text="Loose Mesh to Group", icon="SNAP_VERTEX")

            row = layout.row()
            row.operator("vgu.panel_vertex_group_from_side", text="Group From Side", icon="SNAP_VERTEX")
            row.operator("vgu.panel_vertex_group_from_material", text="Group From Material", icon="SNAP_VERTEX")

            layout.operator("vgu.panel_separate_all_vertexgroup", text="Separate All", icon="MOD_EXPLODE")


            layout.separator()
            layout.label(text="Utility")
            layout.operator("vgu.panel_batch_rename_group", text="Batch Rename Vertex Groups", icon="ZOOM_ALL")
            layout.operator("vgu.panel_merge_vertex_group", text="Merge Group", icon="AUTOMERGE_ON")
            layout.operator("vgu.panel_merge_multiple_vertex_groups", text="Merge Multiple Groups", icon="AUTOMERGE_ON")
            layout.operator("vgu.round_vertex_weight", text="Round All Vertex Weight", icon="AUTOMERGE_ON")

            row = layout.row(align=True)
            row.operator("vgu.select_unlocked_vertex_group", text="Select Unlocked", icon="RESTRICT_SELECT_OFF").mode = "SELECT"
            row.operator("vgu.select_unlocked_vertex_group", text="Deselect Unlocked", icon="RESTRICT_SELECT_ON").mode = "DESELECT"

            layout.separator()
            layout.label(text="Armature")
            bone = layout.operator("vgu.panel_create_bone", text="Bone from Vertex Group", icon="BONE_DATA")
            bone.index = context.object.vertex_groups.active_index
            bone.from_loose_mesh = False

            bone = layout.operator("vgu.panel_create_bone", text="Bone from Loose Mesh", icon="BONE_DATA")
            bone.index = context.object.vertex_groups.active_index
            bone.from_loose_mesh = True

            layout.separator()

            layout.operator("vgu.smooth_all_vertex_groups_weights", text="Smooth All Vertex Groups Weight")


            layout.separator()
            layout.label(text="Selected Objects")
            # layout.operator("vgu.panel_batch_rename_selected_objects_vertex_group", text="Find And Replace", icon="ZOOM_ALL")
            layout.operator("vgu.duplicate_selected_objects_mesh_and_rename_vertex_groups", text="Duplicate Mesh And Rename Vertex Group (Experimental)", icon="DUPLICATE")




            layout.separator()
            layout.label(text="Vertex Colors")
            layout.operator("vgu.vertex_color_from_vertex_group", text="Vertex Color From Vertex Group", icon="VPAINT_HLT")
            layout.operator("vgu.random_vertex_color_from_all_vertex_groups", text="Random Vertex Color From All Vertex Groups", icon="VPAINT_HLT")
            
            layout.separator()
            layout.label(text="Active Object")
            layout.label(text=context.object.name, icon="OBJECT_DATA")
            layout.prop(context.object, "VGU_Object_Seed_Offset", text="Seed")









class VGU_PT_Vertex_Group_Tools(bpy.types.Panel):

    bl_label = "Vertex Group Tools"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Vertex Group Utils"
    bl_options = {'DEFAULT_CLOSED'}


    @classmethod
    def poll(cls, context):
        preferences = utility_function.get_addon_preferences(context)
        if preferences.Vertex_Group_Tools:
            return True




    def draw(self, context):

        layout = self.layout

        notice = True 

        if context.object:
            if context.object.type == "MESH":
                notice = False
                draw_tools(layout, context)

        if notice:
            layout.label(text="Please Select A Mesh Object", icon="INFO")

classes = (
        VGU_UL_VertexGroup_List,
        VGU_UL_VertexGroup_Pie_List,
        # VIEW3D_PT_SIDE_VGU_Panel_SIDE,
        # VIEW3D_PT_SIDE_VGU_Panel_DATA,
        # VIEW3D_PT_VGU_Vertex_Group_Utils_Tools
        )


def register():

    for cls in classes:
        bpy.utils.register_class(cls)



def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
