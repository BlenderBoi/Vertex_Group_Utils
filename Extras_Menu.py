import bpy


from . import utility_function



class FR_MT_Vertex_Group_Utils_Icon_Expose_Menu(bpy.types.Menu):
    bl_label = "Vertex Group Utils Icon Expose Menu"
    bl_idname = "VGU_MT_icon_expose"

    def draw(self, context):

        scn = context.scene

        preferences = utility_function.get_addon_preferences(context)

        options = [
            ("SoloIcon", "Solo", "SOLO_ON"),                          #
            ("VisibilityIcon", "Visibility", "HIDE_OFF"),    #
            ("SelectionIcon", "Select", "RESTRICT_SELECT_OFF"),                                  #
            ("SetPivotIcon", "Set Pivot", "OBJECT_ORIGIN"),         #
            ("SeperateIcon", "Separate", "MOD_BOOLEAN"),                   #
            ("AssignIcon", "Assign", "ADD"),                     #
            ("UnassignIcon", "Unassign", "REMOVE"),                     #
            ("RemoveIcon", "Remove", "TRASH"),                      #
            ("LockAllButThis", "Lock All But This", "MARKER_HLT"),                      #
            ("AddModifierIcon", "Add Modifier", "MODIFIER"),                      #
            ("LockWeightIcon","Lock Weight","LOCKED"),                    #
        ]

        layout = self.layout

        for option in options:
            
            if option[2]:
                row = layout.row(align=True)
                row.label(text="", icon=option[2])
                row.prop(preferences, option[0], text=option[1], icon=option[2])
                row.separator()
            else:
                row = layout.row(align=True)
                row.label(text="", icon="DOT")
                row.prop(preferences, option[0], text=option[1])
                row.separator()



classes = [FR_MT_Vertex_Group_Utils_Icon_Expose_Menu]



def register():

    for cls in classes:
        bpy.utils.register_class(cls)


def unregister():

    for cls in classes:
        bpy.utils.unregister_class(cls)


if __name__ == "__main__":
    register()
