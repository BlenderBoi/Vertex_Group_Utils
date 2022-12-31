import bpy
from . VGU_Pie import *
import rna_keymap_ui
from . import utility_function


Icon_Expose_Style = [("OLD","Legacy","Legacy"),("PANEL","Icon Panel","Icon Panel")]


ENUM_Tabs = [("PANELS", "Panels", "Panels"), ("KEYMAPS","Keymaps","Keymaps")]


def append_panel_class(panels, cls, category, label):

    panel = cls 
    item = [panel, category, label]
    panels.append(item)

    return panels


def update_panel(self, context):

    addon_preferences = utility_function.get_addon_preferences(context)
    
    message = ": Updating Panel locations has failed"

    panels = []

    from . import VGU_UI_Panel 

    panel_cls = VGU_UI_Panel.VGU_PT_Vertex_Group_List_DATA
    category = addon_preferences.Vertex_Group_List_Category
    label = addon_preferences.Vertex_Group_List_Label

    item = [panel_cls, category, label]
    panels.append(item)


    panel_cls = VGU_UI_Panel.VGU_PT_Vertex_Group_List_SIDE
    category = addon_preferences.Vertex_Group_List_Category
    label = addon_preferences.Vertex_Group_List_Label

    item = [panel_cls, category, label]
    panels.append(item)


    panel_cls = VGU_UI_Panel.VGU_PT_Vertex_Group_Tools
    category = addon_preferences.Vertex_Group_Tools_Category
    label = addon_preferences.Vertex_Group_Tools_Label

    item = [panel_cls, category, label]
    panels.append(item)




    try:
        pass
        for item in panels:

            panel = item[0]
            category = item[1]
            label = item[2]
           
            if "bl_rna" in panel.__dict__:
                bpy.utils.unregister_class(panel)


            panel.bl_category = category
            panel.bl_label = label
            bpy.utils.register_class(panel)

    except Exception as e:
        print("\n[{}]\n{}\n\nError:\n{}".format(__name__, message, e))
        pass



























class VGU_user_preferences(bpy.types.AddonPreferences):
    bl_idname = __package__


    TABS_Preferences: bpy.props.EnumProperty(items=ENUM_Tabs)


    Side_Panel: bpy.props.BoolProperty(default=True)
    Object_Data_Panel: bpy.props.BoolProperty(default=True)

    SoloIcon : bpy.props.BoolProperty(default=True)
    VisibilityIcon : bpy.props.BoolProperty(default=True)
    SelectionIcon : bpy.props.BoolProperty(default=True)
    SeperateIcon : bpy.props.BoolProperty(default=True)
    AssignIcon : bpy.props.BoolProperty(default=True)
    UnassignIcon : bpy.props.BoolProperty(default=True)
    RemoveIcon : bpy.props.BoolProperty(default=True)
    AddModifierIcon : bpy.props.BoolProperty(default=False)
    LockWeightIcon : bpy.props.BoolProperty(default=False)
    SetPivotIcon : bpy.props.BoolProperty(default=False)
    LockAllButThis: bpy.props.BoolProperty(default=False)

    Icon_Expose_Style : bpy.props.EnumProperty(items=Icon_Expose_Style, default="PANEL")
    Show_Icon_Expose_Panel : bpy.props.BoolProperty(default=False)

    
    Vertex_Group_List_Category: bpy.props.StringProperty(default="Vertex Group Utils", update=update_panel)
    Vertex_Group_List_Label: bpy.props.StringProperty(default="Vertex Group List", update=update_panel)

    Vertex_Group_Tools_Category: bpy.props.StringProperty(default="Vertex Group Utils", update=update_panel)
    Vertex_Group_Tools_Label: bpy.props.StringProperty(default="Vertex Group Tools", update=update_panel)


    Vertex_Group_List_Side_Panel: bpy.props.BoolProperty(default=True)
    Vertex_Group_List_Data_Panel: bpy.props.BoolProperty(default=True)
    Vertex_Group_Tools: bpy.props.BoolProperty(default=True)



    def draw(self, context):



        layout = self.layout

        col = layout.column(align=True)
        row = col.row(align=True)
        row.prop(self, "TABS_Preferences", expand=True)

        box = col.box()

        if self.TABS_Preferences == "PANELS":
            self.draw_panel_options(context, box)

        if self.TABS_Preferences == "KEYMAPS":
            self.draw_keymaps(context, box)

    def draw_panel_options(self, context, layout):


        # layout.prop(self, "Side_Panel", text="Display Side Panel")
        # layout.prop(self, "Object_Data_Panel", text="Display Object Data Panel")

        layout.label(text="Vertex Group List")
        row = layout.row()
        row.prop(self, "Vertex_Group_List_Side_Panel", text="Side Panel")
        row.prop(self, "Vertex_Group_List_Data_Panel", text="Object Data Properties Panel")

        if any([self.Vertex_Group_List_Side_Panel, self.Vertex_Group_List_Data_Panel]):

            layout.prop(self, "Vertex_Group_List_Category", text="Category")
            layout.prop(self, "Vertex_Group_List_Label", text="Label")




        layout.label(text="Vertex Group Tools")
        layout.prop(self, "Vertex_Group_Tools", text="Side Panel")
        if self.Vertex_Group_Tools:
            layout.prop(self, "Vertex_Group_Tools_Category", text="Category")
            layout.prop(self, "Vertex_Group_Tools_Label", text="Label")

        layout.separator()

    def draw_keymaps(self, context, layout):

        wm = bpy.context.window_manager
        box = layout

        split = box.split()
        col = split.column()
        col.label(text="Vertex Group Utils Hotkey")
        col.separator()


        # keymap = context.window_manager.keyconfigs.user.keymaps['3D View']
        # keymap_items = keymap.keymap_items
        # km = keymap.active()



        wm = bpy.context.window_manager
        kc = wm.keyconfigs.user

        km = kc.keymaps['3D View']
        kmi = km.keymap_items["vgu.call_pie"]

        # kmi = keymap_items["vgu.call_pie"]
        # kmi.show_expanded = False
        # rna_keymap_ui.draw_kmi(kmi, keymap, km, kmi, col, 0)
        # col.separator(factor=0.5)


        if kmi:
            col.context_pointer_set("keymap", km)
            rna_keymap_ui.draw_kmi([], kc, km, kmi, col, 0)
        else:
            col.operator(Template_Add_Hotkey.bl_idname, text = "Add hotkey entry")




addon_keymaps = []



def get_addon_preferences():
    ''' quick wrapper for referencing addon preferences '''
    # addon_preferences = bpy.context.user_preferences.addons[__name__].preferences
    addon_preferences = utility_function.get_addon_preferences(bpy.context)

    return addon_preferences


def get_hotkey_entry_item(km, kmi_name, kmi_value):
    '''
    returns hotkey of specific type, with specific properties.name (keymap is not a dict, so referencing by keys is not enough
    if there are multiple hotkeys!)
    '''
    for i, km_item in enumerate(km.keymap_items):
        if km.keymap_items.keys()[i] == kmi_name:
            if km.keymap_items[i].properties.name == kmi_value:
                return km_item
    return None



def add_hotkey():
    user_preferences = bpy.context.preferences

    addon_prefs = utility_function.get_addon_preferences(bpy.context)
    # addon_prefs = user_preferences.addons["Vertex Group Utils"].preferences

    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps.new(name="3D View", space_type='VIEW_3D', region_type='WINDOW')
    kmi = km.keymap_items.new("vgu.call_pie", type="V", value="PRESS", shift=True, alt=True)
    # kmi.active = True
    addon_keymaps.append((km, kmi))


class Template_Add_Hotkey(bpy.types.Operator):
    ''' Add hotkey entry '''
    bl_idname = "template.add_hotkey"
    bl_label = "Addon Preferences Example"
    bl_options = {'REGISTER', 'INTERNAL'}

    def execute(self, context):
        add_hotkey()
        # self.report({'INFO'}, "Hotkey added in User Preferences -> Input -> Screen -> Screen (Global)")
        return {'FINISHED'}

def remove_hotkey():
    ''' clears all addon level keymap hotkeys stored in addon_keymaps '''
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    km = kc.keymaps['3D View']



    for km, kmi in addon_keymaps:
        km.keymap_items.remove(kmi)
        wm.keyconfigs.addon.keymaps.remove(km)
    addon_keymaps.clear()



classes = [VGU_user_preferences, Template_Add_Hotkey]

def register():

    add_hotkey()



    for cls in classes:
        bpy.utils.register_class(cls)


    update_panel(None, bpy.context)


    # bpy.types.Scene.BoolBasedVisibility = bpy.props.BoolProperty(default=False)






def unregister():

    remove_hotkey()

    update_panel(None, bpy.context)

    for cls in classes:
        bpy.utils.unregister_class(cls)

    # del bpy.types.Scene.BoolBasedVisibility



if __name__ == "__main__":
    register()
