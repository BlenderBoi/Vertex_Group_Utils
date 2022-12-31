import bpy


from . import VGU_Functions
from . utility_function import *
import bpy
import colorsys
import random
import hashlib
import bmesh
import re

def smooth_all_weights(obj):

    vertex_groups = obj.vertex_groups

    mode = obj.mode
    initial_index  = vertex_groups.active_index

    bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)

    for index, vertexgroup in enumerate(vertex_groups):
        vertex_groups.active_index = index
        bpy.ops.object.vertex_group_smooth()


    bpy.ops.object.mode_set(mode=mode, toggle=False)
    vertex_groups.active_index = initial_index




class VGU_OT_Smooth_All_Groups_Weights(bpy.types.Operator):
    """Smooth All Vertex Group of the Object"""

    bl_idname = "vgu.smooth_all_vertex_groups_weights"
    bl_label = "Smooth All Vertex Groups Weights"
    bl_options = {'UNDO', 'REGISTER'}


    def execute(self, context):
        obj = context.object
        smooth_all_weights(obj)
        return {'FINISHED'}

class VGU_OT_LIST_Visibility_Toogle(bpy.types.Operator):
    """Toogle the visibility of selected vertex group"""

    bl_idname = "vgu.panel_visibility_toogle"
    bl_label = "Toogle Visibility"
    bl_options = {'UNDO', 'REGISTER'}

    index : bpy.props.IntProperty()


    def execute(self, context):


        VGU_Functions.Visibility_Toogle(self, context, self.index)

        # if context.mode == "EDIT_MESH":
        #     VGU_Functions.Toogle_State_EditMode(self, context, self.index, "hide")

        # if context.mode == "OBJECT":
        #     VGU_Functions.Visibility_ObjectMode(self, context, self.index)

        return {'FINISHED'}

class VGU_OT_LIST_Selection_Toogle(bpy.types.Operator):
    """Toogle the selection of selected vertex group"""

    bl_idname = "vgu.panel_selection_toogle"
    bl_label = "Toogle Selection"
    bl_options = {'UNDO', 'REGISTER'}

    index : bpy.props.IntProperty()

    def execute(self, context):
        if context.mode == "EDIT_MESH":
            VGU_Functions.Toogle_State_EditMode(self, context, self.index, "select")

        return {'FINISHED'}

class VGU_OT_LIST_Remove(bpy.types.Operator):
    """Remove this vertex group"""

    bl_idname = "vgu.panel_remove"
    bl_label = "Remove Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    index : bpy.props.IntProperty()

    def execute(self, context):

        VGU_Functions.Remove_VertexGroup(self, context, self.index)

        return {'FINISHED'}

class VGU_OT_LIST_Solo(bpy.types.Operator):
    """Solo this vertex group"""

    index : bpy.props.IntProperty()

    bl_idname = "vgu.panel_solo"
    bl_label = "Solo Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):
        if context.mode == "EDIT_MESH":
            VGU_Functions.Solo_EditMode(self, context, self.index)

        if context.mode == "OBJECT":
            VGU_Functions.Solo_ObjectMode(self, context, self.index)

        return {'FINISHED'}

class VGU_OT_LIST_Assign(bpy.types.Operator):
    """Assign selected vertex to this vertex group"""

    bl_idname = "vgu.panel_assign"
    bl_label = "Assign Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    assignOption : bpy.props.EnumProperty(items=(("ASSIGN", "Assign Selected", "Assign Selected"), ("REASSIGN", "Reassign Group", "Reassign Group")), name="")
    index : bpy.props.IntProperty()
    weight : bpy.props.FloatProperty(default=1.0, min=0, max=1, subtype="FACTOR")

    def execute(self, context):

        if self.assignOption == "ASSIGN":
            VGU_Functions.Assign_VertexGroup(self, context, self.index, self.weight)
        elif self.assignOption == "REASSIGN":
            VGU_Functions.Reassign_VertexGroup(self, context, self.index, self.weight)

        return {'FINISHED'}


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "assignOption")
        layout.prop(self, "weight")


class VGU_OT_LIST_Unassign(bpy.types.Operator):
    """Unassign selected vertex to this vertex group"""

    bl_idname = "vgu.panel_unassign"
    bl_label = "Unassign Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    removeOption : bpy.props.EnumProperty(items=(("SELECTED", "Unassign Selected", "Unassign Selected"), ("ALL", "Unassign All", "Unassign All"), ("ZERO", "Unassign Zero Weights", "Unassign Zero Weights")), name="")
    index : bpy.props.IntProperty()

    def execute(self, context):

        if self.removeOption == "SELECTED":
            VGU_Functions.Unassign_VertexGroup(self, context, self.index)
        elif self.removeOption == "ALL":
            VGU_Functions.Unassign_All_VertexGroup(self, context, self.index)
        elif self.removeOption == "ZERO":
            amount = VGU_Functions.Unassign_Zero_Weight_From_Group(self, context, self.index)
            self.report({"INFO"}, "Removed %s vertices from vetex group" %(amount))


        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "removeOption")

class VGU_OT_LIST_Seperate(bpy.types.Operator):
    """Seperate this vertex group into a different object"""

    bl_idname = "vgu.panel_seperate"
    bl_label = "Seperate Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    index : bpy.props.IntProperty()
    centerpivot : bpy.props.BoolProperty(default=True)
    Mode : bpy.props.EnumProperty(items=(("EXTRACT", "Extract", "Extract"), ("DUPLICATE", "Duplicate", "Duplicate"), ("REMOVE", "Remove", "Remove")))

    def execute(self, context):

        separated = VGU_Functions.Seperate_From_VertexGroup(self, context, index=self.index, centerpivot=self.centerpivot, mode=self.Mode)


        return {'FINISHED'}


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)

    def draw(self, context):
        layout = self.layout

        layout.prop(self, "Mode")

        if self.Mode != "REMOVE":
            layout.prop(self,"centerpivot")

class VGU_OT_LIST_Add_Modifier(bpy.types.Operator):
    """Add Modifier and uses this vertex group"""

    bl_idname = "vgu.panel_addmodifier"
    bl_label = "Add Modifier"
    bl_options = {'UNDO', 'REGISTER'}

    index : bpy.props.IntProperty()
    modifier: bpy.props.EnumProperty(items = (("BEVEL", "Bevel", "Bevel"),("DECIMATE", "Decimate", "Decimate"), ("MASK", "Mask", "Mask"), ("SOLIDIFY", "Solidify", "Solidify"), ("WELD", "Weld", "Weld"),("WIREFRAME", "Wireframe", "Wireframe"), ("CAST", "Cast", "Cast"), ("CURVE", "Curve", "Curve"), ("DISPLACE", "Displace", "Displace"), ("HOOK", "Hook", "Hook"), ("LAPLACIANDEFORM", "Laplacian Deform", "Laplacian Deform"), ("LATTICE", "Lattice", "Lattice"), ("MESH_DEFORM", "Mesh Deform", "Mesh Deform"), ("SHRINKWRAP", "Shrinkwrap", "Shrinkwrap"), ("SIMPLE_DEFORM", "Simple Deform", "Simple Deform"), ("SMOOTH","Smooth","Smooth"), ("CORRECTIVE_SMOOTH", "Corrective Smooth", "Corrective Smooth"), ("LAPLACIANSMOOTH", "Laplacian Smooth", "Laplacian Smooth"), ("SURFACE_DEFORM", "Surface Deform", "Surface Deform"), ("WARP", "Warp", "Warp"), ("WAVE", "Wave","Wave")))

    thickness : bpy.props.FloatProperty(name = "Thickness", default = 1)

    def execute(self, context):


        NewModifier = context.object.modifiers.new(type=self.modifier, name = self.modifier)

        if self.modifier == "BEVEL":
            NewModifier.limit_method = "VGROUP"

        if self.modifier == "SOLIDIFY":
            NewModifier.thickness = self.thickness

        NewModifier.vertex_group = context.object.vertex_groups[self.index].name

        return {'FINISHED'}

    def draw(self, context):

        layout = self.layout
        layout.prop(self,"modifier")

        if self.modifier == "SOLIDIFY":
            layout.prop(self, "thickness")



    def invoke(self, context, event):


        return context.window_manager.invoke_props_dialog(self)

class VGU_OT_PANEL_New_VertexGroup(bpy.types.Operator):
    """Add a New Vertex Group"""

    bl_idname = "vgu.panel_new_vertexgroup"
    bl_label = "New Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    name: bpy.props.StringProperty(default="Group")
    weight: bpy.props.FloatProperty(default=1, subtype="FACTOR", min=0, max=1)

    def execute(self, context):

        mode = context.mode

        VGU_Functions.New_VertexGroup(self, context, self.name, self.weight)




        return {'FINISHED'}

    def draw(self, context):

        layout = self.layout
        layout.prop(self,"name")

        if context.mode == "EDIT_MESH":
            layout.prop(self, "weight")



    def invoke(self, context, event):


        return context.window_manager.invoke_props_dialog(self)


class VGU_OT_PANEL_Remove_Empty_VertexGroup(bpy.types.Operator):
    """Remove Empty Vertex Group"""

    bl_idname = "vgu.panel_remove_empty_vertexgroup"
    bl_label = "Remove Empty Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    isZeroWeight : bpy.props.BoolProperty(name = "Include Zero Weight", default=True)

    def execute(self, context):

        emptycount = VGU_Functions.Remove_Empty_Group(self, context)
        zerocount = 0

        if self.isZeroWeight:
            zerocount = VGU_Functions.Remove_Zero_Weight_Group(self, context)

        count = emptycount + zerocount
        message = "{} Empty Vertex Group Deleted!".format(str(count))

        self.report({"INFO"}, message)

        return {'FINISHED'}


    def draw(self, context):

        layout = self.layout

        layout.prop(self,"isZeroWeight")


    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)




class VGU_OT_PANEL_Separate_All(bpy.types.Operator):
    """Separate all Vertex Group into other object"""

    bl_idname = "vgu.panel_separate_all_vertexgroup"
    bl_label = "Seperate All"
    bl_options = {'UNDO', 'REGISTER'}

    centerpivot: bpy.props.BoolProperty(default=True)
    Mode : bpy.props.EnumProperty(items=(("EXTRACT", "Extract", "Extract"), ("DUPLICATE", "Duplicate", "Duplicate"), ("REMOVE", "Remove", "Remove")))

    def execute(self, context):

        for VG in context.object.vertex_groups:
            vertexgroup_id = VG.index
            VGU_Functions.Seperate_From_VertexGroup(self, context, index=vertexgroup_id, centerpivot=self.centerpivot, mode=self.Mode)

        if len(context.object.data.vertices) == 0:
            bpy.data.objects.remove(context.object)


        return {'FINISHED'}

    def draw(self, context):

        layout = self.layout

        layout.prop(self,"Mode")

        if self.Mode != "REMOVE":
            layout.prop(self,"centerpivot")

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)






class VGU_OT_Join_as_Group(bpy.types.Operator):
    """Join object as vertex group"""
    bl_idname = "vgu.panel_join_as_vertex_group"
    bl_label = "Join object as Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    vertexgroup_id : bpy.props.IntProperty()
    isParentVGroup: bpy.props.BoolProperty(default=True, name="Create Vertex Group for Active Object")
    isApplyModifier: bpy.props.BoolProperty(default=False, name="Apply Modifier")
    IncludeVertexGroup: bpy.props.BoolProperty(default=False, name="Include Vertex Group")
    isCenterPivot: bpy.props.BoolProperty(default=True, name="Center Pivot")
    isMergeVertex: bpy.props.BoolProperty(default=False, name="Merge Vertex")



    @classmethod
    def poll(cls, context):
        if context.mode == "OBJECT":
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        layout.prop(self,"isParentVGroup")
        layout.prop(self,"isApplyModifier")
        layout.prop(self,"IncludeVertexGroup")
        layout.prop(self,"isCenterPivot")
        layout.prop(self,"isMergeVertex")



    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def execute(self, context):

        if bpy.context.object.type == "MESH":
            VGU_Functions.Join_as_VertexGroup(context, isParentVGroup=self.isParentVGroup, isApplyModifier=self.isApplyModifier, IncludeVertexGroup=self.IncludeVertexGroup, isCenterPivot=self.isCenterPivot, isMergeVertex=self.isMergeVertex)


        else:
            self.report({"ERROR"}, "Please select an active mesh object")


        return {'FINISHED'}





class VGU_OT_PANEL_Loose_Mesh_To_Group(bpy.types.Operator):
    """Split Loose Mesh into Vertex Group"""
    bl_idname = "vgu.panel_split_loose_to_vertex_group"
    bl_label = "Split loose mesh into Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    vertexgroup_id : bpy.props.IntProperty()
    name: bpy.props.StringProperty(default="Object", name="Name")
    isResetGroup: bpy.props.BoolProperty(default=True, name="Reset Groups")



    @classmethod
    def poll(cls, context):
        if context.mode == "OBJECT" or context.mode == "EDIT_MESH":
            return True
        else:
            return False

    def draw(self, context):
        layout = self.layout
        layout.prop(self,"name")
        layout.prop(self,"isResetGroup")



    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)




    def execute(self, context):

        VGU_Functions.Split_Loose_to_Group(context, isResetGroup=self.isResetGroup, name=self.name)

        return {'FINISHED'}









ENUM_Batch_Rename_Mode = [("REPLACE","Find and Replace","Find and Replace"),("PREFIX","Prefix","Prefix"),("SUFFIX","Suffix","Suffix")]

class VGU_OT_PANEL_Batch_Rename_Group(bpy.types.Operator):
    """Batch Rename Vertex Groups"""
    bl_idname= "vgu.panel_batch_rename_group"
    bl_label = "Batch Rename Vertex Groups"
    bl_options = {'UNDO', 'REGISTER'}

    # Find: bpy.props.StringProperty()
    # Replace: bpy.props.StringProperty()

    String_A: bpy.props.StringProperty()
    String_B: bpy.props.StringProperty()

    Mode: bpy.props.EnumProperty(items=ENUM_Batch_Rename_Mode)

    Selected_Objects: bpy.props.BoolProperty(default=False)


    def draw(self, context):

        layout = self.layout


        layout.prop(self, "Mode", expand=True)
        if self.Mode == "REPLACE":
            layout.prop(self,  "String_A", text="Find")
            layout.prop(self,  "String_B", text="Replace")

        if self.Mode == "PREFIX":

            layout.prop(self,  "String_A", text="Prefix")

        if self.Mode == "SUFFIX":

            layout.prop(self,  "String_A", text="Suffix")

        layout.prop(self, "Selected_Objects", text="Rename All Selected Objects")



    def execute(self, context):


        if self.Selected_Objects:
            for obj in context.selected_objects:
                VGU_Functions.batch_rename_vertex_group(obj, self.Mode, self.String_A, self.String_B)
        else:

            obj = context.object
            VGU_Functions.batch_rename_vertex_group(obj, self.Mode, self.String_A, self.String_B)



        # VGU_Functions.Find_And_Replace_Name(context.object, self.Find, self.Replace)
        return {"FINISHED"}


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)







class VGU_OT_PANEL_Merge_Group(bpy.types.Operator):
    """Merge Two Vertex Group"""
    bl_idname= "vgu.panel_merge_vertex_group"
    bl_label = "Merge Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    VG1: bpy.props.StringProperty()
    VG2: bpy.props.StringProperty()
    mode: bpy.props.EnumProperty(default = "1", items = (("0", "Add", "Add"),("1", "Replace", "Replace"), ("2", "Average", "Average")))

    def execute(self, context):

        mode = context.mode

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



        if self.VG1 and self.VG2:
            VGU_Functions.MergeVertexGroup(self, context, context.object, self.VG1, self.VG2, self.mode)

        else:
            self.report({"ERROR"}, "No Vertex Group is Selected")



        if mode == "OBJECT":
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        if mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if mode == "PAINT_WEIGHT":
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)

        return{"FINISHED"}


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        layout = self.layout

        layout.prop_search(self, "VG1", context.active_object,  "vertex_groups", text="Main")

        layout.prop_search(self, "VG2", context.active_object,  "vertex_groups", text="other")

        layout.prop(self, "mode")













class VGU_OT_LIST_Set_Origin(bpy.types.Operator):
    """Use this Vertex Group Center as Origin"""

    index : bpy.props.IntProperty()

    bl_idname = "vgu.panel_set_origin"
    bl_label = "Set as Origin"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):

        VGU_Functions.Set_As_Origin(self, context, self.index)

        return {'FINISHED'}



class VGU_OT_LIST_Create_Bone_at_group(bpy.types.Operator):
    """Create Bones at Vertex Group"""

    index : bpy.props.IntProperty()
    add_armature_modifier: bpy.props.BoolProperty(default=True)
    bone_direction: bpy.props.EnumProperty(items=[("UP","Up","Up"), ("FRONT", "Front", "Front")])
    from_loose_mesh : bpy.props.BoolProperty()

    bl_idname = "vgu.panel_create_bone"
    bl_label = "Create Bone"
    bl_options = {'UNDO', 'REGISTER'}

    def execute(self, context):

        if self.from_loose_mesh:
            bpy.ops.vgu.panel_split_loose_to_vertex_group()

        VGU_Functions.Bone_from_Vertex_Group(self, context, self.index, self.add_armature_modifier, self.bone_direction)

        return {'FINISHED'}

    def draw(self, context):
        layout = self.layout
        layout.prop(self, "add_armature_modifier", text="Add Armature Modifier")
        layout.prop(self, "bone_direction", text="Bone Direction")


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)







class VGU_OT_PANEL_Unassign_Zero_Weight_From_Group(bpy.types.Operator):
    """Unassign Zero Weight From Group"""

    bl_idname = "vgu.panel_unassign_zero_weight_from_group"
    bl_label = "Unassign Zero Weight from Group"
    bl_options = {'UNDO', 'REGISTER'}

    index: bpy.props.IntProperty()


    def execute(self, context):


        VGU_Functions.Unassign_Zero_Weight_From_Group(self, context, self.index)

        return {'FINISHED'}




class VGU_OT_PANEL_Unassign_Zero_Weight_From_All_Group(bpy.types.Operator):
    """Unassign Zero Weight From Group"""

    bl_idname = "vgu.panel_unassign_zero_weight_from_all_group"
    bl_label = "Unassign Zero Weight from Group"
    bl_options = {'UNDO', 'REGISTER'}

    index: bpy.props.IntProperty()


    def execute(self, context):

        vertsCount = 0

        for vg in context.object.vertex_groups:

            amount = VGU_Functions.Unassign_Zero_Weight_From_Group(self, context, vg.index)
            vertsCount += amount

        self.report({"INFO"}, "Removed %s vertices from vetex group" %(vertsCount))
        return {'FINISHED'}



class VGU_OT_PANEL_Group_From_Side(bpy.types.Operator):
    """Create Group From Side"""

    bl_idname = "vgu.panel_vertex_group_from_side"
    bl_label = "Create Vertex Group From Side"
    bl_options = {'UNDO', 'REGISTER'}

    create_center: bpy.props.BoolProperty(name="Create Group for Center")
    include_center: bpy.props.BoolProperty(name="Include Center in each Side")

    # center : bpy.props.EnumProperty(items=(("ORIGIN", "Origin", "Origin"),("CENTER", "Center", "Center"), ("WORLD", "World", "World")))
    # center : bpy.props.EnumProperty(items=(("ORIGIN", "Origin", "Origin")))
    def execute(self, context):
        self.center = "ORIGIN"
        VGU_Functions.Vertex_Group_From_Side(self, context, createCenter= self.create_center, includeCenter= self.include_center, center = self.center)


        return {'FINISHED'}



    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)















class VGU_OT_PANEL_Group_From_Material(bpy.types.Operator):
    """Create Group From Material"""

    bl_idname = "vgu.panel_vertex_group_from_material"
    bl_label = "Create Vertex Group From Material"
    bl_options = {'UNDO', 'REGISTER'}


    def execute(self, context):

        VGU_Functions.Vertex_Group_From_Material(self, context)


        return {'FINISHED'}







class VGU_MT_PIE_Set_Active_Vertex_Group_Menu(bpy.types.Menu):
    bl_label = "Set Active Vertex Group"
    bl_idname = "OBJECT_MT_set_active_custom_menu"
    bl_options = {'UNDO', 'REGISTER'}

    def draw(self, context):
        layout = self.layout


        for VG in context.object.vertex_groups:


            if VG.index == context.object.vertex_groups.active_index:
                ActiveName = "Active: " + VG.name
                layout.operator("vgupie.set_active_group", text = ActiveName).VertexGroupIndex = VG.index
            else:
                layout.operator("vgupie.set_active_group", text = VG.name).VertexGroupIndex = VG.index




class VGU_OT_Set_Active_Vertex_Group(bpy.types.Operator):
    '''Set the active vertex group'''
    bl_idname = "vgupie.set_active_group"
    bl_label = "Set Active Group"
    bl_options = {'UNDO', 'REGISTER'}

    VertexGroupIndex : bpy.props.IntProperty()

    def execute(self, context):


        context.object.vertex_groups.active_index = self.VertexGroupIndex

        vg_group_name= context.object.vertex_groups[self.VertexGroupIndex].name

        message = "Active Group: " + vg_group_name

        self.report({"INFO"}, message)
        return {'FINISHED'}




class VGU_OT_PIE_Call_ActiveVertexGroup_Menu(bpy.types.Operator):
    '''Call the active vertex group menu'''
    bl_idname = "vgupie.call_active_group_menu"
    bl_label = "Call Active Group Menu"
    bl_options = {'UNDO', 'REGISTER'}


    def execute(self, context):

        bpy.ops.wm.call_menu(name="OBJECT_MT_set_active_custom_menu")

        return {'FINISHED'}






class VGU_OT_Select_Unlocked_Vertex_Group(bpy.types.Operator):
    """Select Unlocked Vertex Group"""

    bl_idname = "vgu.select_unlocked_vertex_group"
    bl_label = "Select Unlocked Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    mode : bpy.props.StringProperty()

    @classmethod
    def poll(cls, context):

        if context.object:
            if context.object.mode == "EDIT":
                return True
            else:
                return False
        else:
            return False


    def execute(self, context):

        save_active = context.object.vertex_groups.active_index

        for vertex_group in context.object.vertex_groups:

            if vertex_group.lock_weight == False:
                bpy.context.object.vertex_groups.active_index = vertex_group.index

                if self.mode == "SELECT":
                    bpy.ops.object.vertex_group_select()
                if self.mode == "DESELECT":
                    bpy.ops.object.vertex_group_deselect()



        context.object.vertex_groups.active_index = save_active

        return {'FINISHED'}




class VGU_OT_PANEL_Merge_Multiple_Groups(bpy.types.Operator):
    """Merge Multiple Vertex Groups"""
    bl_idname= "vgu.panel_merge_multiple_vertex_groups"
    bl_label = "Merge Multiple Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    VG1: bpy.props.StringProperty()
    merge_all: bpy.props.BoolProperty(default=False)
    mode: bpy.props.EnumProperty(default = "1", items = (("0", "Add", "Add"),("1", "Replace", "Replace"), ("2", "Average", "Average")))

    def execute(self, context):

        scn = context.scene
        multi_vg = scn.Multi_VG_Picker
        mode = context.mode

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        if self.VG1:
            if self.merge_all:
                for vg in context.object.vertex_groups:
                    if vg.name == self.VG1:
                        continue

                    VGU_Functions.MergeVertexGroup(self, context, context.object, self.VG1, vg.name, self.mode)

            else:
                for vg in multi_vg:
                    if vg.Name == self.VG1:
                        continue

                    if vg.Bool:
                        VGU_Functions.MergeVertexGroup(self, context, context.object, self.VG1, vg.Name, self.mode)
                    # context.view_layer.update()

        if mode == "OBJECT":
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        if mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if mode == "PAINT_WEIGHT":
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)


        multi_vg.clear()

        return{"FINISHED"}


    def invoke(self, context, event):


        scn = context.scene
        multi_vg = scn.Multi_VG_Picker
        object = context.object
        if object:

            multi_vg.clear()
            for vg in object.vertex_groups:
                item = multi_vg.add()
                item.Name = vg.name
                item.Index = vg.index

            return context.window_manager.invoke_props_dialog(self)

        return{"FINISHED"}


    def draw(self, context):
        layout = self.layout

        scn = context.scene
        multi_vg = scn.Multi_VG_Picker

        layout.prop_search(self, "VG1", context.active_object,  "vertex_groups", text="Main")
        layout.prop(self, "merge_all", text="Merge All")
        if not self.merge_all:
            if len(multi_vg) > 0:
                box = layout.box()
                box.label(text="Vertex Groups")
                if not self.merge_all:
                    for vg in multi_vg:
                        if vg.Name == self.VG1:
                            continue
                        box.prop(vg, "Bool", text=vg.Name)

        layout.prop(self, "mode")



class VGU_Multi_VG_Picker(bpy.types.PropertyGroup):
    Index: bpy.props.IntProperty()
    Color: bpy.props.FloatProperty()
    Name: bpy.props.StringProperty()
    Bool: bpy.props.BoolProperty()


#Sharp
#Smooth
#Affect By Weight
#Weight As None / Hue / Saturation / Value / Red / Green / Blue
#Vertex Paint Mode
def list_compare(list1, list2):
    for val in list2:
        if val in list1:
            pass
        else:
            return False

    return True


#Fix Out of Bound
#Fix Mode Changing

ENUM_VG_Color_Weight=[("NONE","None","None"),None, ("HUE","Hue","Hue"),("SATURATION","Saturation","Saturation"),("VALUE","Value","Value"),None, ("RED","Red","Red"),("GREEN","Green","Green"),("BLUE","Blue","Blue")]
ENUM_mode = [("VERTEX","Vertex","Vertex"),("FACE","Face","Face")]

class VGU_OT_Vertex_Color_From_Vertex_Group(bpy.types.Operator):
    """Vertex Color From Vertex Group"""

    bl_idname = "vgu.vertex_color_from_vertex_group"
    bl_label = "Vertex Color From Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    use_weight_as: bpy.props.EnumProperty(items=ENUM_VG_Color_Weight)
    color: bpy.props.FloatVectorProperty(default=(1, 0, 0), size=3, subtype="COLOR", min=0, max=1)
    vertex_group: bpy.props.StringProperty()
    mode: bpy.props.EnumProperty(items=ENUM_mode)

    def draw(self, context):
        object = context.object
        if object:
            if object.type == "MESH":
                layout = self.layout
                layout.prop(self, "color", text="Color")
                layout.prop(self, "mode", expand=True)
                layout.prop(self, "use_weight_as", text="Use Weight As")
                layout.prop_search(self, "vertex_group", object, "vertex_groups", text="Vertex Group")



    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    @classmethod
    def poll(cls, context):
        object = context.object
        if object:
            if object.type == "MESH":
                return True


    def execute(self, context):


        object = context.object
        mode = context.mode

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        # context.space_data.shading.color_type = 'VERTEX'

        if object:
            if object.type == "MESH":
                if self.vertex_group:

                    vertex_group = object.vertex_groups.get(self.vertex_group)

                    mesh = object.data

                    vertices =  [ v.index for v in mesh.vertices if vertex_group.index in [ vg.group for vg in v.groups ] ]
                    faces = [f for f in mesh.polygons if list_compare(vertices, f.vertices)]

                    loops = [loop for loop in mesh.loops if loop.vertex_index in vertices]


                    if vertex_group:

                        if not mesh.vertex_colors:
                            mesh.vertex_colors.new()

                        color_layer = mesh.vertex_colors.active

                        if len(color_layer.data) > 0:
                            if self.mode == "VERTEX":
                                for loop in loops:
                                    if self.use_weight_as == "NONE":
                                        color = self.color

                                    if self.use_weight_as == "HUE":
                                        color = self.color
                                        hsv= colorsys.rgb_to_hsv(color[0], color[1], color[2])
                                        hsv_color = [hsv[0], hsv[1], hsv[2]]

                                        for g in mesh.vertices[loop.vertex_index].groups:
                                            if g.group == vertex_group.index:
                                                hsv_color[0] = g.weight
                                                color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                                                break
                                                # hsv_color[0] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                # color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])

                                    if self.use_weight_as == "SATURATION":
                                        color = self.color
                                        hsv= colorsys.rgb_to_hsv(color[0], color[1], color[2])
                                        hsv_color = [hsv[0], hsv[1], hsv[2]]

                                        for g in mesh.vertices[loop.vertex_index].groups:
                                            if g.group == vertex_group.index:
                                                hsv_color[1] = g.weight
                                                color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                                                break

                                                # hsv_color[1] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                # color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])

                                    if self.use_weight_as == "VALUE":
                                        color = self.color
                                        hsv= colorsys.rgb_to_hsv(color[0], color[1], color[2])
                                        hsv_color = [hsv[0], hsv[1], hsv[2]]

                                        for g in mesh.vertices[loop.vertex_index].groups:
                                            if g.group == vertex_group.index:
                                                hsv_color[2] = g.weight
                                                color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                                                break
                                                # hsv_color[2] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                # color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])

                                    if self.use_weight_as == "RED":
                                        color = self.color

                                        for g in mesh.vertices[loop.vertex_index].groups:
                                            if g.group == vertex_group.index:
                                                color[0] = g.weight
                                                break
                                                # color[0] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight

                                    if self.use_weight_as == "GREEN":
                                        color = self.color

                                        for g in mesh.vertices[loop.vertex_index].groups:
                                            if g.group == vertex_group.index:
                                                color[1] = g.weight
                                                # color[1] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                break


                                    if self.use_weight_as == "BLUE":
                                        color = self.color
                                        for g in mesh.vertices[loop.vertex_index].groups:
                                            if g.group == vertex_group.index:
                                                color[2] = g.weight
                                                break
                                                # color[2] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight



                                    color = (color[0], color[1], color[2], 1.0)
                                    color_layer.data[loop.index].color = color

                            if self.mode == "FACE":
                                for face in faces:
                                    for loop_index in face.loop_indices:

                                        loop = mesh.loops[loop_index]

                                        if self.use_weight_as == "NONE":
                                            color = self.color

                                        if self.use_weight_as == "HUE":
                                            color = self.color
                                            hsv= colorsys.rgb_to_hsv(color[0], color[1], color[2])
                                            hsv_color = [hsv[0], hsv[1], hsv[2]]



                                            for g in mesh.vertices[loop.vertex_index].groups:
                                                if g.group == vertex_group.index:
                                                    hsv_color[0] = g.weight
                                                    color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])

                                                    # hsv_color[0] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                    # color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                                                    break







                                        if self.use_weight_as == "SATURATION":
                                            color = self.color
                                            hsv= colorsys.rgb_to_hsv(color[0], color[1], color[2])
                                            hsv_color = [hsv[0], hsv[1], hsv[2]]

                                            for g in mesh.vertices[loop.vertex_index].groups:
                                                if g.group == vertex_group.index:

                                                    hsv_color[1] = g.weight
                                                    # hsv_color[1] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                    color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                                                    break

                                        if self.use_weight_as == "VALUE":
                                            color = self.color
                                            hsv= colorsys.rgb_to_hsv(color[0], color[1], color[2])
                                            hsv_color = [hsv[0], hsv[1], hsv[2]]

                                            for g in mesh.vertices[loop.vertex_index].groups:
                                                if g.group == vertex_group.index:

                                                    hsv_color[2] = g.weight
                                                    color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])
                                                    break
                                                    # hsv_color[2] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight
                                                    # color = colorsys.hsv_to_rgb(hsv_color[0], hsv_color[1], hsv_color[2])

                                        if self.use_weight_as == "RED":
                                            color = self.color

                                            for g in mesh.vertices[loop.vertex_index].groups:
                                                if g.group == vertex_group.index:
                                                    color[0] = g.weight
                                                    break

                                        if self.use_weight_as == "GREEN":
                                            color = self.color

                                            for g in mesh.vertices[loop.vertex_index].groups:
                                                if g.group == vertex_group.index:
                                                    color[1] = g.weight
                                                    break

                                                    # color[1] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight

                                        if self.use_weight_as == "BLUE":
                                            color = self.color

                                            for g in mesh.vertices[loop.vertex_index].groups:
                                                if g.group == vertex_group.index:
                                                    color[2] = g.weight
                                                    break

                                                    # color[2] = mesh.vertices[loop.vertex_index].groups[vertex_group.index].weight

                                        color = (color[0], color[1], color[2], 1.0)
                                        color_layer.data[loop_index].color = color

        if mode == "OBJECT":
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        if mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if mode == "PAINT_WEIGHT":
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)
        if mode == "PAINT_VERTEX":
            bpy.ops.object.mode_set(mode='VERTEX_PAINT', toggle=False)

        return {'FINISHED'}

class VGU_OT_Random_Vertex_Color_From_All_Vertex_Groups(bpy.types.Operator):
    """Random Vertex Color From All Vertex Groups"""

    bl_idname = "vgu.random_vertex_color_from_all_vertex_groups"
    bl_label = "Random Vertex Color From All Vertex Groups"
    bl_options = {'UNDO', 'REGISTER'}

    seed_offset: bpy.props.IntProperty(default=0, min=0)
    use_object_level_seed: bpy.props.BoolProperty(default=False)
    include_name_for_seed: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout
        
        layout.prop(self, "use_object_level_seed", text="Use Object Level Seed Offset")
        layout.prop(self, "include_name_for_seed", text="Include Name in Seed")

        if not self.use_object_level_seed:
        
            layout.prop(self, "seed_offset", text="Seed Offset")
        

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)

    @classmethod
    def poll(cls, context):
        object = context.object
        if object:
            if object.type == "MESH":
                return True

    def execute(self, context):

        object = context.object
        mode = context.mode

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        for object in context.selected_objects:
            if object:
                if object.type == "MESH":
                    for vertex_group in object.vertex_groups:

                        mesh = object.data

                        vertices =  [ v.index for v in mesh.vertices if vertex_group.index in [ vg.group for vg in v.groups ] ]
                        faces = [f for f in mesh.polygons if list_compare(vertices, f.vertices)]

                        loops = [loop for loop in mesh.loops if loop.vertex_index in vertices]


                        if vertex_group:

                            color = None
                            h = hash(vertex_group.name)
                            if h < 0:
                                h = h * -1
                            
                            # final_seed = h+self.seed_offset
                            final_seed = 0 
                            final_offset = 0

                            if self.use_object_level_seed:
                                final_offset = object.VGU_Object_Seed_Offset 
                            else:
                                final_offset = self.seed_offset

                            if self.include_name_for_seed:
                                final_seed = h + final_offset

                            else:
                                final_seed = final_offset

                            # random.seed(h+self.seed_offset)
                            random.seed(final_seed)
                            hue_random = random.random()
                            hue_random = round(hue_random, 6)

                            color = [hue_random, 1, 1]
                            rgb= colorsys.hsv_to_rgb(color[0], color[1], color[2])

                            if not mesh.vertex_colors:
                                mesh.vertex_colors.new()

                            color_layer = mesh.vertex_colors.active

                            if len(color_layer.data) > 0:

                                for face in faces:
                                    for loop_index in face.loop_indices:

                                        loop = mesh.loops[loop_index]


                                        vcolor = (rgb[0], rgb[1], rgb[2], 1.0)
                                        color_layer.data[loop_index].color = vcolor

        if mode == "OBJECT":
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        if mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        if mode == "PAINT_WEIGHT":
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT', toggle=False)
        if mode == "PAINT_VERTEX":
            bpy.ops.object.mode_set(mode='VERTEX_PAINT', toggle=False)


        return {'FINISHED'}



class VGU_OT_Unhide_All_Visibility(bpy.types.Operator):
    """Unhide All Visibility"""

    bl_idname = "vgu.unhide_all_visibility"
    bl_label = "Unhide All Visibility"
    bl_options = {'UNDO', 'REGISTER'}


    def execute(self, context):

        if context.object:
            if context.mode == "EDIT_MESH":
                bpy.ops.mesh.reveal()
            for modifier in context.object.modifiers:
                if modifier.type == 'MASK':
                    modifier.show_viewport = False
                    modifier.show_render = False
            
        return {'FINISHED'}



















ENUM_Mode = [("UP","Round Up","Round Up"),("DOWN","Round Down","Round Down"),("BOTH","Both","Both")]



class VGU_Round_Vertex_Weight(bpy.types.Operator):
    """Round Up or Down All Vertex's Weight in all Vertex Group"""
    bl_idname = "vgu.round_vertex_weight"
    bl_label = "Round All Vertex Weight"

    mode: bpy.props.EnumProperty(items=ENUM_Mode)
    roundup_threshold: bpy.props.FloatProperty(default=0, soft_min=0, soft_max=1)
    roundup_setvalue: bpy.props.FloatProperty(default=1, soft_min=0, soft_max=1)
    
    roundown_threshold: bpy.props.FloatProperty(default=0, soft_min=0, soft_max=1)
    roundown_setvalue: bpy.props.FloatProperty(default=0, soft_min=0, soft_max=1)

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)


    def draw(self, context):
        
        layout = self.layout
        layout.prop(self, "mode", text="Mode")
        
        if self.mode == "UP":
            layout.prop(self, "roundup_threshold", text="Round Up Threshold")
            layout.prop(self, "roundup_setvalue", text="Round Up To")
              
        if self.mode == "DOWN":
            layout.prop(self, "roundown_threshold", text="Round Down Threshold")
            layout.prop(self, "roundown_setvalue", text="Round Down To")
              
        if self.mode == "BOTH":
            layout.label(text="Round Up Threshold  Round Down Threshold")
            layout.label(text="Needs to Be Higher than")
            layout.label(text="Round Down Threshold")
            layout.label(text="Round Up")
            layout.prop(self, "roundup_threshold", text="Round Up Threshold")
            layout.prop(self, "roundup_setvalue", text="Round Up To")
            layout.label(text="Round Down")
            layout.prop(self, "roundown_threshold", text="Round Down Threshold")
            layout.prop(self, "roundown_setvalue", text="Round Down To")
            
            
            
    def execute(self, context):


        mode = self.mode
        report = False
        current_mode = context.mode 

        selected_mesh_object = [object for object in context.selected_objects if object.type == "MESH"]

        bpy.ops.object.mode_set(mode='OBJECT')

        for object in selected_mesh_object:

            if object.type == "MESH":
                
                
                
                
                roundup_threshold = self.roundup_threshold
                roundup_setvalue = self.roundup_setvalue

                roundown_threshold = self.roundown_threshold
                roundown_setvalue = self.roundown_setvalue

                me = object.data

                bm = bmesh.new()
                bm.from_mesh(me)

                bm.verts.layers.deform.verify()
                deform = bm.verts.layers.deform.active


                for v in bm.verts:
                    g = v[deform]
                    for index, vertex_group in enumerate(object.vertex_groups):
                        try:
                            weight = g[index]
                            if mode == "UP":
                                
                                if weight > roundup_threshold:
                                    g[index] = roundup_setvalue
                                    
                            if mode == "DOWN":
                                
                                if weight < roundown_threshold:
                                    g[index] = roundown_setvalue

                            if mode == "BOTH":
                                if roundup_threshold > roundown_threshold:
                                    if weight > roundup_threshold:
                                        g[index] = roundup_setvalue
                                    elif weight < roundown_threshold:
                                        g[index] = roundown_setvalue
                                else:
                                    report = True
                        except:
                            pass



                bm.to_mesh(me)
                bm.free()
                bpy.context.view_layer.update()

        if report:
            self.report({"ERROR"}, "On 'Both' mode, Please Make Sure Roundup Threshold is Higher than Roundown Threshold")
        
        if current_mode == "EDIT":
            bpy.ops.object.mode_set(mode='EDIT')

        if current_mode == "WEIGHT_PAINT":
            bpy.ops.object.mode_set(mode='WEIGHT_PAINT')

        return {'FINISHED'}












class VGU_OT_Lock_All_But_This(bpy.types.Operator):
    """Lock All Weight But This"""

    bl_idname = "vgu.lock_all_weight_but_this"
    bl_label = "Lock All Weight But This"
    bl_options = {'UNDO', 'REGISTER'}

    index: bpy.props.IntProperty()

    def execute(self, context):

        obj = context.object

        if obj is not None:
            for vertex_group in obj.vertex_groups:
                vertex_group.lock_weight = True

            if len(obj.vertex_groups) > self.index:
                vg = obj.vertex_groups[self.index]
                vg.lock_weight = False

        return {'FINISHED'}









ENUM_Rename_Mode = [("NUMBER_INCREMENT","Number Increment","Number Increment"),("FIND_AND_REPLACE","Find And Replace","Find And Replace")]

class VGU_OT_Duplicate_Selected_Objects_Mesh_And_Rename_Vertex_Groups(bpy.types.Operator):
    """Duplicate Selected Objects Mesh And Rename Vertex Groups"""

    bl_idname = "vgu.duplicate_selected_objects_mesh_and_rename_vertex_groups"
    bl_label = "Duplicate Selected Objects Mesh And Rename Vertex Groups"
    bl_options = {'UNDO', 'REGISTER'}


    Mode: bpy.props.EnumProperty(items=ENUM_Rename_Mode)
    Find: bpy.props.StringProperty()
    Replace: bpy.props.StringProperty()
    Pad_Number: bpy.props.BoolProperty()
    Join_Object: bpy.props.BoolProperty(default=True)

    def draw(self, context):
        layout = self.layout

        row = layout.row()
        row.prop(self, "Mode")

        if self.Mode == "FIND_AND_REPLACE":
            layout.prop(self, "Find", text="Find")
            layout.prop(self, "Replace", text="Replace")
        else:
            layout.prop(self, "Pad_Number", text="Pad Number")

        layout.prop(self, "Join_Object", text="Rejoin Object")

    def execute(self, context):


        if context.mode == "OBJECT":

            selected = [obj for obj in context.selected_objects if obj.type == "MESH"]

            if self.Mode == "FIND_AND_REPLACE":

                if not self.Find == "" and not self.Replace == "":

                    for obj in selected:

                        if obj.type == "MESH":

                            for select in context.selected_objects:
                                select.select_set(False)

                            context.view_layer.objects.active = obj
                            obj.select_set(True)
                        
                            new_mesh = obj.data.copy()
                            new_obj = obj.copy()

                            new_obj.data = new_mesh
                            context.scene.collection.objects.link(new_obj)

                            VGU_Functions.Find_And_Replace_Name(obj, self.Find, self.Replace)

                            bpy.ops.object.join()


            if self.Mode == "NUMBER_INCREMENT":


                for obj in selected:

                    if obj.type == "MESH":

                        for select in context.selected_objects:
                            select.select_set(False)

                        context.view_layer.objects.active = obj
                        obj.select_set(True)
                    
                        new_mesh = obj.data.copy()
                        new_obj = obj.copy()

                        new_obj.data = new_mesh
                        context.scene.collection.objects.link(new_obj)

                        vg_rename_pair = []

                        for vg in obj.vertex_groups:

                            name = vg.name
                            vg.name = "TEMP"
                            vg_rename_pair.append([vg, name])

                        for pair in vg_rename_pair:
                            
                            vg = pair[0]
                            name = pair[1]

                            name = increment_string_number(name, self.Pad_Number)

                            vg.name = name


                        # for vertex_group in obj.vertex_groups:
                        #      
                        #     name = vertex_group.name
                        #     vertex_group.name = name

                        if self.Join_Object:
                            bpy.ops.object.join()






        else:
            self.report({"INFO"}, "Please Switch To Object Mode")
        

        return {'FINISHED'}

    def invoke(self, context, event):

        return context.window_manager.invoke_props_dialog(self)



class VGU_OT_PANEL_Batch_Rename_Selected_Objects_Vertex_Group(bpy.types.Operator):
    """Find and Replace words in Vertex Group Of Selected Objects"""
    bl_idname= "vgu.panel_batch_rename_selected_objects_vertex_group"
    bl_label = "Find and Replace Selected Objects Vertex Group"
    bl_options = {'UNDO', 'REGISTER'}

    Find: bpy.props.StringProperty()
    Replace: bpy.props.StringProperty()

    def execute(self, context):


        for obj in context.selected_objects:

            if obj.type == "MESH":
                VGU_Functions.Find_And_Replace_Name(obj, self.Find, self.Replace)

        return {"FINISHED"}


    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)








classes = (
            VGU_OT_Duplicate_Selected_Objects_Mesh_And_Rename_Vertex_Groups,
            VGU_OT_PANEL_Batch_Rename_Selected_Objects_Vertex_Group,
            VGU_Round_Vertex_Weight,
            VGU_OT_Unhide_All_Visibility, 
            VGU_OT_Random_Vertex_Color_From_All_Vertex_Groups,
            VGU_OT_Vertex_Color_From_Vertex_Group,
            VGU_OT_PANEL_Merge_Multiple_Groups,
            VGU_Multi_VG_Picker,
            VGU_OT_LIST_Visibility_Toogle,
            VGU_OT_LIST_Selection_Toogle,
            VGU_OT_LIST_Remove,
            VGU_OT_LIST_Solo,
            VGU_OT_LIST_Assign,
            VGU_OT_LIST_Unassign,
            VGU_OT_LIST_Seperate,
            VGU_OT_LIST_Set_Origin,

            VGU_OT_LIST_Add_Modifier,

            VGU_OT_PANEL_New_VertexGroup,
            VGU_OT_PANEL_Remove_Empty_VertexGroup,
            VGU_OT_PANEL_Separate_All,
            VGU_OT_PANEL_Loose_Mesh_To_Group,
            VGU_OT_PANEL_Batch_Rename_Group,
            VGU_OT_PANEL_Merge_Group,
            VGU_OT_PANEL_Unassign_Zero_Weight_From_Group,
            VGU_OT_PANEL_Unassign_Zero_Weight_From_All_Group,
            VGU_OT_PANEL_Group_From_Side,
            VGU_OT_PANEL_Group_From_Material,

            VGU_OT_Join_as_Group,

            VGU_MT_PIE_Set_Active_Vertex_Group_Menu,
            VGU_OT_Set_Active_Vertex_Group,
            VGU_OT_PIE_Call_ActiveVertexGroup_Menu,
            VGU_OT_LIST_Create_Bone_at_group,

            VGU_OT_Select_Unlocked_Vertex_Group,
            VGU_OT_Smooth_All_Groups_Weights,

            VGU_OT_Lock_All_But_This,
            )


def register():

    for cls in classes:
        bpy.utils.register_class(cls)

    bpy.types.Scene.Multi_VG_Picker = bpy.props.CollectionProperty(type=VGU_Multi_VG_Picker)
    bpy.types.Object.VGU_Object_Seed_Offset = bpy.props.IntProperty()

def unregister():


    for cls in classes:
        bpy.utils.unregister_class(cls)

    del bpy.types.Scene.Multi_VG_Picker
    del bpy.types.Object.VGU_Object_Seed_Offset

if __name__ == "__main__":
    register()
