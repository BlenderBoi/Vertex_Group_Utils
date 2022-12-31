

bl_info = {
    "name": "Vertex Group Utils",
    "author": "BlenderBoi",
    "version": (2, 5, 8),
    "blender": (3, 1, 0),
    "description": "Enhance vertex group by adding some utility.",
    "warning": "",
    "wiki_url": "",
    "category": "Vertex Group",
}


import bpy

from . import VGU_UI_Panel
from . import VGU_Operators
from . import VGU_Pie
from . import VGU_Preferences
from . import Extras_Menu

def register():

    VGU_Operators.register()
    VGU_UI_Panel.register()
    VGU_Pie.register()
    Extras_Menu.register()
    VGU_Preferences.register()


def unregister():

    VGU_Operators.unregister()
    VGU_UI_Panel.unregister()
    VGU_Pie.unregister()
    Extras_Menu.unregister()

    VGU_Preferences.unregister()

if __name__ == "__main__":
    register()
