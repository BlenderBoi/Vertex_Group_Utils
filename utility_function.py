import bpy
import numpy as np

import bmesh
from mathutils import Matrix, Vector
import re
import os


script_file = os.path.realpath(__file__)
addon_directory = os.path.dirname(script_file)
addon_name = os.path.basename(addon_directory)


def get_addon_preferences(context):
    addon_preferences = context.preferences.addons[addon_name].preferences
    return addon_preferences










def find_center_point(obj):

    pts = [(obj.matrix_world @ v.co) for v in obj.data.vertices]
    center_pt = np.average(pts, 0)

    return center_pt



def find_center_point_from_verts(obj, verts):

    pts = [(obj.matrix_world @ v.co) for v in verts]
    center_pt = np.average(pts, 0)

    return center_pt




def find_lowest_point(obj, center=False):

    lowest_pt = min([(obj.matrix_world @ v.co).z for v in obj.data.vertices])
    lowest_z = min([(obj.matrix_world @ v.co).z for v in obj.data.vertices])
    lowest_pts = [(obj.matrix_world @ v.co) for v in obj.data.vertices if (obj.matrix_world @ v.co).z == lowest_z]
    lowest_pt = np.average(lowest_pts, 0)

    if center == True:
        lowest_pt_center = find_center_point(obj)
        lowest_pt_center[2] = lowest_pt[2]
        return lowest_pt_center

    else:
        return lowest_pt


def create_empty(name, input):

    o = bpy.data.objects.new( name, None )
    bpy.context.scene.collection.objects.link( o )
    o.empty_display_size = 2
    o.empty_display_type = 'PLAIN_AXES'

    try:
        o.matrix_world = input.matrix_world
        return o
    except:
        try:
            o.matrix_world = input
            return o
        except:
            try:
                o.location = input
                return o
            except:
                print("Wrong Type")


def moveOrigin(obj, location):

    currentMode = bpy.context.mode

    if currentMode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode='OBJECT')


    location = Vector(location)

    ob = obj
    cursor_world_loc = location
    cursor_local_loc = ob.matrix_world.inverted() @ cursor_world_loc

    mat = Matrix.Translation(-cursor_local_loc)

    me = ob.data

    me.transform(mat)
    me.update()

    ob.matrix_world.translation = cursor_world_loc

    if currentMode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode='EDIT')





def updateUI():
    for screen in bpy.data.screens:
        for area in screen.areas:
            area.tag_redraw()



def create_armature(name, input):

    data = bpy.data.armatures.new(name)
    o = bpy.data.objects.new( name, data)
    bpy.context.scene.collection.objects.link( o )
    # o.empty_display_size = 2
    # o.empty_display_type = 'PLAIN_AXES'

    try:
        o.matrix_world = input.matrix_world
        return o
    except:
        try:
            o.matrix_world = input
            return o
        except:
            try:
                o.location = input
                return o
            except:
                print("Wrong Type")


def increment_number(n, padding=True):

    number = str(int(n) + 1)
    if padding:
        number = number.zfill(len(n)) 

    return number 


def increment_string_number(n, pad):

    # final = re.sub('\d+', lambda x: str(int(x.group(0))+1),n)
    final = re.sub('\d+', lambda x: increment_number(x.group(0), pad), n)

    return final
