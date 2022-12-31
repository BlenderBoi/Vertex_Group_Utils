import bpy
import bmesh
from . utility_function import *
from mathutils import Matrix, Vector, Euler

###UTILITYFUNCTION###
def GetVertexGroup_EDIT_Vertex(bm, index, bool=True):

    vertexgroup_list = []

    deform = bm.verts.layers.deform.active

    for v in bm.verts:
        vGroup = v[deform]
        if bool:
            if index in vGroup:
                vertexgroup_list.append(v)
        else:
            if index in vGroup:
                pass
            else:
                vertexgroup_list.append(v)

    return vertexgroup_list

def GetLinkedFace_EDIT_Vertex(bm, vertices):

    linked_faces_set = set()

    for v in vertices:
        for link_face in v.link_faces:
            linked_faces_set.add(link_face)

    return linked_faces_set


def GetFaceFromVerts_EDIT_Vertex(vertices, linkfaces):

    face_set = set()

    for linkface in linkfaces:
        check_counter = 0

        for vert in vertices:
            for link_vert in linkface.verts:
                if vert == link_vert:
                    check_counter += 1

            if len(linkface.verts) == check_counter:
                face_set.add(linkface)

    return face_set

def MeshState(meshes, bool, state):

    if state == "hide":
        for mesh in meshes:
            mesh.hide_set(bool)

    elif state == "select":
        for mesh in meshes:
            mesh.select_set(bool)


def MeshState_Toogle(meshes, state, bm):



    if state == "hide":

        mesh_state_list = all([m.hide for m in meshes])

        if mesh_state_list:
            MeshState(meshes, False, "hide")

        else:
            MeshState(meshes, True, "hide")



    elif state == "select":

        mesh_state_list = all([m.select for m in meshes])

        if mesh_state_list:
            MeshState(meshes, False, "select")
            bm.select_flush(False)
        else:
            MeshState(meshes, True, "select")
            bm.select_flush(True)

    elif state == "solo":

        mesh_state_list = all([m.select for m in meshes])

        if mesh_state_list:
            MeshState(meshes, False, "hide")
        else:
            MeshState(meshes, True, "hide")



def modifier_check(self, context):
    for modifier in context.object.modifiers :
        if "VGU_" in modifier.name:
            if modifier.vertex_group and context.object.vertex_groups.get(modifier.vertex_group):
                pass
            else:
                context.object.modifiers.remove(modifier)



###OPERATOR_FUNCTION###


def Toogle_State_EditMode(self, context, index, state):


    obj = context.object
    data = obj.data


    bm = bmesh.from_edit_mesh(data)


    bm.verts.layers.deform.verify()
    deform = bm.verts.layers.deform.active



    VGroup_Vertices = GetVertexGroup_EDIT_Vertex(bm, index)
    VGroup_LinkedFaces = GetLinkedFace_EDIT_Vertex(bm, VGroup_Vertices)


    MeshState_Toogle(VGroup_Vertices, state, bm)



    # if VGroup_LinkedFaces:
    #     VGroup_Faces = GetFaceFromVerts_EDIT_Vertex(VGroup_Vertices, VGroup_LinkedFaces)
    #     MeshState_Toogle(VGroup_Faces, state)
    # else:


    # bmesh.update_edit_mesh(data, True)
    bmesh.update_edit_mesh(data)


def Solo_Mesh_State(meshes, selected_vertices, bool, state):

    if state == "hide":
        for mesh in meshes:
            if mesh in selected_vertices:
                mesh.hide = not bool
            else:
                mesh.hide_set(bool)


def Solo_EditMode(self, context, index):

    obj = context.object
    data = obj.data


    bm = bmesh.from_edit_mesh(data)


    bm.verts.layers.deform.verify()
    deform = bm.verts.layers.deform.active

    NONVG_Vertices = GetVertexGroup_EDIT_Vertex(bm, index, bool = False)

    VGroup_Vertices = GetVertexGroup_EDIT_Vertex(bm, index)

    # VGroup_LinkedFaces = GetLinkedFace_EDIT_Vertex(bm, VGroup_Vertices)
    # VGroup_Faces = GetFaceFromVerts_EDIT_Vertex(VGroup_Vertices, VGroup_LinkedFaces)


    if VGroup_Vertices:

        vg_state_list = [m.hide for m in VGroup_Vertices]
        nonvg_state_list = [m.hide for m in NONVG_Vertices]

        if any(vg_state_list) == True or all(nonvg_state_list) == False:
            Solo_Mesh_State(bm.verts, VGroup_Vertices,  True, "hide")
            # MeshState(VGroup_Vertices, False ,"hide")

        if all(vg_state_list) == False and all(nonvg_state_list) == True:
            MeshState(bm.verts, False, "hide")

    #
    # if VGroup_LinkedFaces:
    #     vg_state_list = [m.hide for m in VGroup_Faces]
    #     nonvg_state_list = [m.hide for m in NONVG_Vertices]
    #
    #     if any(vg_state_list) == True or all(nonvg_state_list) == False:
    #         MeshState(bm.verts, True, "hide")
    #         MeshState(VGroup_Faces, False ,"hide")
    #
    #     if all(vg_state_list) == False and all(nonvg_state_list) == True:
    #         MeshState(bm.verts, False, "hide")
    # else:
    #     if VGroup_Vertices:
    #
    #         vg_state_list = [m.hide for m in VGroup_Vertices]
    #         nonvg_state_list = [m.hide for m in NONVG_Vertices]
    #
    #         if any(vg_state_list) == True or all(nonvg_state_list) == False:
    #             MeshState(bm.verts, True, "hide")
    #             MeshState(VGroup_Vertices, False ,"hide")
    #
    #         if all(vg_state_list) == False and all(nonvg_state_list) == True:
    #             MeshState(bm.verts, False, "hide")



    bm.select_flush(False)
    # bmesh.update_edit_mesh(data, True)
    bmesh.update_edit_mesh(data)



def Solo_ObjectMode(self, context, index):


    vertexgroup = context.object.vertex_groups[index]
    ModifierName = "VGU_" + vertexgroup.name


    modifier_check(self, context)


    if context.object.modifiers:

        solo_modifier = context.object.modifiers.get(ModifierName)

        if solo_modifier:
            if solo_modifier.type == "MASK":
                if solo_modifier.vertex_group:
                    if solo_modifier.vertex_group == vertexgroup.name:

                        if solo_modifier.show_viewport == True:
                            solo_modifier.show_viewport = False
                            solo_modifier.show_render = False
                            solo_modifier.invert_vertex_group = False
                            return 0

                        elif solo_modifier.show_viewport == False:
                            solo_modifier.show_viewport = True
                            solo_modifier.show_render = True
                            solo_modifier.invert_vertex_group = False
                            return 0
                    else:
                        solo_modifier.vertex_group = vertexgroup.name

                        if solo_modifier.show_viewport == True:
                            solo_modifier.show_viewport = False
                            solo_modifier.show_render = False
                            solo_modifier.invert_vertex_group = False
                            return 0

                        elif solo_modifier.show_viewport == False:
                            solo_modifier.show_viewport = True
                            solo_modifier.show_render = True
                            solo_modifier.invert_vertex_group = False
                            return 0


    new_modifier= context.object.modifiers.new(name=ModifierName, type="MASK")
    new_modifier.show_viewport = True
    new_modifier.show_render = True
    new_modifier.threshold = 0
    new_modifier.vertex_group = context.object.vertex_groups[index].name
    new_modifier.invert_vertex_group = False







def Visibility_ObjectMode(self, context, index):


    vertexgroup = context.object.vertex_groups[index]
    ModifierName = "VGU_" + vertexgroup.name


    modifier_check(self, context)


    if context.object.modifiers:

        solo_modifier = context.object.modifiers.get(ModifierName)

        if solo_modifier:
            if solo_modifier.type == "MASK":
                if solo_modifier.vertex_group:
                    if solo_modifier.vertex_group == vertexgroup.name:

                        if solo_modifier.show_viewport == True:
                            solo_modifier.show_viewport = False
                            solo_modifier.show_render = False
                            solo_modifier.invert_vertex_group = True

                            # solo.modifier.show_on_cage = True
                            # solo.modifier.show_in_editmode = True

                            return 0

                        elif solo_modifier.show_viewport == False:
                            solo_modifier.show_viewport = True
                            solo_modifier.show_render = True
                            solo_modifier.invert_vertex_group = True

                            # solo.modifier.show_on_cage = True
                            # solo.modifier.show_in_editmode = True

                            return 0
                    else:
                        solo_modifier.vertex_group = vertexgroup.name

                        if solo_modifier.show_viewport == True:
                            solo_modifier.show_viewport = False
                            solo_modifier.show_render = False
                            solo_modifier.invert_vertex_group = True

                            # solo.modifier.show_on_cage = True
                            # solo.modifier.show_in_editmode = True



                            return 0

                        elif solo_modifier.show_viewport == False:
                            solo_modifier.show_viewport = True
                            solo_modifier.show_render = True
                            solo_modifier.invert_vertex_group = True

                            # solo.modifier.show_on_cage = True
                            # solo.modifier.show_in_editmode = True





                            return 0


    new_modifier= context.object.modifiers.new(name=ModifierName, type="MASK")
    new_modifier.show_viewport = True
    new_modifier.show_render = True

    new_modifier.show_on_cage = True
    new_modifier.show_in_editmode = True


    new_modifier.threshold = 0
    new_modifier.vertex_group = context.object.vertex_groups[index].name
    new_modifier.invert_vertex_group = True




def Visibility_Toogle(self, context, index):


    vertexgroup = context.object.vertex_groups[index]
    ModifierName = "VGU_" + vertexgroup.name


    modifier_check(self, context)


    if context.object.modifiers:

        solo_modifier = context.object.modifiers.get(ModifierName)

        if solo_modifier:
            if solo_modifier.type == "MASK":
                if solo_modifier.vertex_group:
                    if solo_modifier.vertex_group == vertexgroup.name:

                        if solo_modifier.show_viewport == True:
                            solo_modifier.show_viewport = False
                            solo_modifier.show_render = False
                            solo_modifier.show_on_cage = True
                            solo_modifier.show_in_editmode = True
                            solo_modifier.invert_vertex_group = True
                            return 0

                        elif solo_modifier.show_viewport == False:
                            solo_modifier.show_viewport = True
                            solo_modifier.show_render = True
                            solo_modifier.show_on_cage = True
                            solo_modifier.show_in_editmode = True
                            solo_modifier.invert_vertex_group = True
                            return 0
                    else:
                        solo_modifier.vertex_group = vertexgroup.name

                        if solo_modifier.show_viewport == True:
                            solo_modifier.show_viewport = False
                            solo_modifier.show_render = False
                            solo_modifier.show_on_cage = True
                            solo_modifier.show_in_editmode = True
                            solo_modifier.invert_vertex_group = True
                            return 0

                        elif solo_modifier.show_viewport == False:
                            solo_modifier.show_viewport = True
                            solo_modifier.show_render = True
                            solo_modifier.show_on_cage = True
                            solo_modifier.show_in_editmode = True
                            solo_modifier.invert_vertex_group = True
                            return 0


    new_modifier= context.object.modifiers.new(name=ModifierName, type="MASK")
    new_modifier.show_viewport = True
    new_modifier.show_render = True
    new_modifier.show_on_cage = True
    new_modifier.show_in_editmode = True


    new_modifier.threshold = 0
    new_modifier.vertex_group = context.object.vertex_groups[index].name
    new_modifier.invert_vertex_group = True



###########################################


def Remove_Empty_Group(self, context):

    if context.mode == "EDIT_MESH":
        print("Changemode")
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    object = context.object
    data = object.data


    count = 0

    for vg in object.vertex_groups:
        EmptyVG = not any(vg.index in [g.group for g in v.groups] for v in data.vertices)
        if EmptyVG:
            count = count + 1
            Remove_VertexGroup(self, context, vg.index)


            # return count

    return count

            # message = "{} Empty Vertex Group Deleted!".format(str(count))

            # self.report({"INFO"}, message)



###Not Working
def Assign_VertexGroup(self, context, index, weight=1.0):

    object_vertices= context.object.data.vertices
    object_vertex_group = context.object.vertex_groups[index]

    # if isReassign:
    #     bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    #     for v in object_vertices:
    #         object_vertex_group.remove([v.index])
    #     bpy.ops.object.mode_set(mode='EDIT', toggle=False)


    object_data = context.edit_object.data
    object_BMesh = bmesh.from_edit_mesh(object_data)

    object_BMesh.verts.layers.deform.verify()

    deform = object_BMesh.verts.layers.deform.active

    for v in object_BMesh.verts:

        g = v[deform]
        if v.select:
            g[index] = weight

    # bmesh.update_edit_mesh(object_data, True)
    bmesh.update_edit_mesh(object_data)


def Reassign_VertexGroup(self, context, index, weight=1.0):

    object_vertices= context.object.data.vertices
    object_vertex_group = context.object.vertex_groups[index]


    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    for v in object_vertices:
        object_vertex_group.remove([v.index])
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)


    object_data = context.edit_object.data
    object_BMesh = bmesh.from_edit_mesh(object_data)

    object_BMesh.verts.layers.deform.verify()

    deform = object_BMesh.verts.layers.deform.active

    for v in object_BMesh.verts:

        g = v[deform]
        if v.select:
            g[index] = weight

    # bmesh.update_edit_mesh(object_data, True)
    bmesh.update_edit_mesh(object_data)

def Unassign_VertexGroup(self, context, index):

    object_vertices= context.object.data.vertices
    object_vertex_group = context.object.vertex_groups[index]

    object_data = context.edit_object.data
    object_BMesh = bmesh.from_edit_mesh(object_data)

    object_BMesh.verts.layers.deform.verify()

    deform = object_BMesh.verts.layers.deform.active




    selected_vertices = [v.index for v in object_vertices if v.select]


    previousindex = context.object.vertex_groups.active_index

    bpy.context.object.vertex_groups.active_index=index

    bpy.ops.object.vertex_group_remove_from()

    bpy.context.object.vertex_groups.active_index=previousindex

def Unassign_All_VertexGroup(self, context, index):

    object_vertices= context.object.data.vertices
    object_vertex_group = context.object.vertex_groups[index]

    object_data = context.edit_object.data
    object_BMesh = bmesh.from_edit_mesh(object_data)

    object_BMesh.verts.layers.deform.verify()

    deform = object_BMesh.verts.layers.deform.active



    selected_vertices = object_vertices

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    for v in selected_vertices:
        object_vertex_group.remove([v.index])

    bpy.ops.object.mode_set(mode='EDIT', toggle=False)














def New_VertexGroup(self, context, Name, weight):


    if context.mode == "EDIT_MESH":

        object_vertices= context.object.data.vertices

        NewVertexGroup = bpy.context.object.vertex_groups.new(name=Name)

        selected_vertices = [v.index for v in object_vertices if v.select]

        object_data = context.object.data
        object_BMesh = bmesh.from_edit_mesh(object_data)

        object_BMesh.verts.layers.deform.verify()

        deform = object_BMesh.verts.layers.deform.active

        for v in object_BMesh.verts:

            g = v[deform]
            if v.select:
                g[NewVertexGroup.index] = weight

        bmesh.update_edit_mesh(object_data)
        # bmesh.update_edit_mesh(object_data, True)


    elif context.mode == "OBJECT":
        context.object.vertex_groups.new(name=Name)



def Remove_VertexGroup(self, context, index):



    object = context.object
    VertexGroup = object.vertex_groups[index]
    object.vertex_groups.remove(VertexGroup)

    modifier_check(self, context)


















# def Seperate_From_VertexGroup(self, context, index=0, centerpivot=True, mode="EXTRACT"):


#     obj = context.object.data

#     VertexGroup_Name = context.object.vertex_groups[index].name

#     check_Counter = 0
#     current_mode = context.mode
#     try:

#         bpy.ops.object.mode_set(mode='OBJECT', toggle=False)


#         if mode != "REMOVE":



#             bm = bmesh.new()   # create an empty BMesh
#             bm.from_mesh(obj)

#             #Collecting Mesh Data

#             #Check if Vertex Group is Everything
#             #Todo

#             VGroup_Vertices = GetVertexGroup_EDIT_Vertex(bm, index)



#             if VGroup_Vertices:
#                 VGroup_LinkedFaces = GetLinkedFace_EDIT_Vertex(bm, VGroup_Vertices)

#                 if VGroup_LinkedFaces:
#                     VGroup_Faces = GetFaceFromVerts_EDIT_Vertex(VGroup_Vertices, VGroup_LinkedFaces)
#                 else:
#                     VGroup_Faces = set()




#                 bm.verts.layers.deform.verify()
#                 deform = bm.verts.layers.deform.active

#                 newgeometry = bmesh.ops.split(bm, geom=list(VGroup_Faces))
#                 newgeometryface = newgeometry["geom"]

#                 bm2 = bm.copy()

#                 VertexGroup_Non=[f for f in bm.faces]
#                 VertexGroup_Non = [f for f in VertexGroup_Non if f not in newgeometryface]

#                 bmesh.ops.delete(bm, geom=VertexGroup_Non, context="FACES")


#                 #Creates a New Object
#                 newmesh = bpy.data.meshes.new(VertexGroup_Name)
#                 newobj = bpy.data.objects.new(VertexGroup_Name, newmesh)
#                 bpy.context.scene.collection.objects.link(newobj)


#                 newobj.matrix_world = bpy.context.object.matrix_world

#                 collections = context.object.users_collection

#                 for collection in collections:
#                     collection.objects.link(newobj)


#                 #Done with the Master Object
#                 bm.to_mesh(newobj.data)
#                 bm.free()




#                 ###############################################################################

#                 #add options for centerpivot
#                 #Delete Group after seperate
#                 #Duplicate or remove

#                 if centerpivot:
#                     centerpoint = find_center_point(newobj)
#                     moveOrigin(newobj, centerpoint)



#             ###############################################################################

#         if mode != "DUPLICATE":


#             bm_ori = bmesh.new()
#             bm_ori.from_mesh(obj)



#             VGroup_Vertices = GetVertexGroup_EDIT_Vertex(bm_ori, index)
#             VGroup_LinkedFaces = GetLinkedFace_EDIT_Vertex(bm_ori, VGroup_Vertices)

#             if VGroup_LinkedFaces:
#                 VGroup_Faces = GetFaceFromVerts_EDIT_Vertex(VGroup_Vertices, VGroup_LinkedFaces)


#             bm_ori.verts.layers.deform.verify()
#             deform = bm_ori.verts.layers.deform.active

#             bmesh.ops.delete(bm_ori, geom=list(VGroup_Faces), context="FACES")



#             NONVG_Vertices = GetVertexGroup_EDIT_Vertex(bm_ori, index, bool = False)


#             bm_ori.to_mesh(obj)
#             bm_ori.free()


#             if NONVG_Vertices == False:
#                 Remove_VertexGroup(self, context, index)


#         if current_mode == "EDIT_MESH":
#             bpy.ops.object.mode_set(mode='EDIT', toggle=False)



#         if mode != "DUPLICATE":
#             context.object.vertex_groups.remove(context.object.vertex_groups[index])


#     except:

#         if current_mode == "EDIT_MESH":
#             bpy.ops.object.mode_set(mode='EDIT', toggle=False)
#         else:
#             bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

#         self.report({"INFO"}, "Vertex Group is Empty")

#     updateUI()












def Seperate_From_VertexGroup(self, context, index=0, centerpivot=True, mode="EXTRACT"):

    object = context.object



        # duplicate_obj.select_set(True)

    obj = context.object.data
    VertexGroup_Name = object.vertex_groups[index].name

    check_Counter = 0
    current_mode = object.mode


    try:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



        if mode != "REMOVE":


            duplicate_obj = object.copy()
            duplicate_obj.data = duplicate_obj.data.copy()

            collections = object.users_collection
            for collection in collections:
                collection.objects.link(duplicate_obj)

            duplicate_obj.update_from_editmode()

            duplicate_obj.name = VertexGroup_Name

            bm = bmesh.new()   # create an empty BMesh
            bm.from_mesh(duplicate_obj.data)

            #Collecting Mesh Data

            #Check if Vertex Group is Everything
            #Todo



            VGroup_Vertices = GetVertexGroup_EDIT_Vertex(bm, index)




            if VGroup_Vertices:
                VGroup_LinkedFaces = GetLinkedFace_EDIT_Vertex(bm, VGroup_Vertices)

                if VGroup_LinkedFaces:
                    VGroup_Faces = GetFaceFromVerts_EDIT_Vertex(VGroup_Vertices, VGroup_LinkedFaces)
                else:
                    VGroup_Faces = set()




                bm.verts.layers.deform.verify()
                deform = bm.verts.layers.deform.active

                newgeometry = bmesh.ops.split(bm, geom=list(VGroup_Faces))
                newgeometryface = newgeometry["geom"]

                VertexGroup_Non=[f for f in bm.faces]
                VertexGroup_Non = [f for f in VertexGroup_Non if f not in newgeometryface]

                bmesh.ops.delete(bm, geom=VertexGroup_Non, context="FACES")

                #Done with the Master Object
                bm.to_mesh(duplicate_obj.data)
                bm.free()




                ###############################################################################

                #add options for centerpivot
                #Delete Group after seperate
                #Duplicate or remove

                if centerpivot:
                    centerpoint = find_center_point(duplicate_obj)
                    moveOrigin(duplicate_obj, centerpoint)



            ###############################################################################

        if mode != "DUPLICATE":


            bm_ori = bmesh.new()
            bm_ori.from_mesh(obj)



            VGroup_Vertices = GetVertexGroup_EDIT_Vertex(bm_ori, index)
            VGroup_LinkedFaces = GetLinkedFace_EDIT_Vertex(bm_ori, VGroup_Vertices)

            if VGroup_LinkedFaces:
                VGroup_Faces = GetFaceFromVerts_EDIT_Vertex(VGroup_Vertices, VGroup_LinkedFaces)


            bm_ori.verts.layers.deform.verify()
            deform = bm_ori.verts.layers.deform.active

            bmesh.ops.delete(bm_ori, geom=list(VGroup_Faces), context="FACES")



            NONVG_Vertices = GetVertexGroup_EDIT_Vertex(bm_ori, index, bool = False)


            bm_ori.to_mesh(obj)
            bm_ori.free()


            if NONVG_Vertices == False:
                Remove_VertexGroup(self, context, index)


        if current_mode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)



        if mode != "DUPLICATE":
            context.object.vertex_groups.remove(context.object.vertex_groups[index])


    except:
        self.report({"INFO"}, "Vertex Group is Empty")



    if current_mode == "EDIT":
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    else:
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)



    updateUI()





















#####################################################################################################################################################





def Join_as_VertexGroup(context, isParentVGroup=True, isApplyModifier=True, IncludeVertexGroup=False, isCenterPivot=True, isMergeVertex=False):

    obj = context.active_object
    sel = context.selected_objects

    counter = 0

    for ob in sel:
        counter = counter + 1
        if ob != obj:
            if ob.type == "MESH":



                if IncludeVertexGroup:
                    if isApplyModifier:

                        old_mesh = ob.data

                        depsgraph = bpy.context.evaluated_depsgraph_get()

                        object_eval = ob.evaluated_get(depsgraph)

                        apply_mesh = bpy.data.meshes.new_from_object(object_eval)

                        ob.modifiers.clear()
                        ob.data = apply_mesh

                        bpy.data.meshes.remove(old_mesh)
                    else:
                        ob.modifiers.clear()

                else:
                    if isApplyModifier:

                        old_mesh = ob.data

                        depsgraph = bpy.context.evaluated_depsgraph_get()

                        object_eval = ob.evaluated_get(depsgraph)

                        apply_mesh = bpy.data.meshes.new_from_object(object_eval)

                        ob.modifiers.clear()
                        ob.data = apply_mesh

                        bpy.data.meshes.remove(old_mesh)
                    else:
                        ob.modifiers.clear()

                    for vg in ob.vertex_groups:
                        ob.vertex_groups.remove(vg)



                VG = ob.vertex_groups.new(name=ob.name_full)
                for v in ob.data.vertices:
                    ob.vertex_groups[VG.name].add([v.index], 1.0, "ADD")


    if isParentVGroup:
        try:
            obj.vertex_groups[obj.name_full]
        except:

            PVG = obj.vertex_groups.new(name=obj.name_full)
            for v in obj.data.vertices:
                obj.vertex_groups[PVG.name].add([v.index], 1.0, "ADD")

    bpy.ops.object.join()
    if isCenterPivot:
        bpy.ops.object.origin_set(type='ORIGIN_CENTER_OF_MASS', center='MEDIAN')

    if isMergeVertex:
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)
        bpy.ops.mesh.select_all(action='SELECT')
        bpy.ops.mesh.remove_doubles()
        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
    else:
        pass


    return counter


#    bm.to_mesh(obj.data)
#    bm.free()

#
#    bm.verts.layers.deform.verify()
#    deform = bm.verts.layers.deform.active





def Split_Loose_to_Group(context, isResetGroup=True, name="group"):

    obj = bpy.context.object
    obj_VG = bpy.context.object.vertex_groups
    obj_name = bpy.context.object.name_full

    obj.modifiers.clear()

    if isResetGroup:
        obj_VG.clear()

    obj.name = name

    bpy.ops.mesh.separate(type='LOOSE')

    bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

    Join_as_VertexGroup(context, isParentVGroup=True, isApplyModifier=False, IncludeVertexGroup=False, isCenterPivot=False, isMergeVertex=False)

    obj.name = obj_name




def Find_And_Replace_Name(object, find, replace):

    for VG in object.vertex_groups:

        VertexGroup_name = VG.name
        VertexGroup_new_name = VertexGroup_name.replace(find, replace)
        VG.name = VertexGroup_new_name

    
def batch_rename_vertex_group(object, mode, string_a, string_b):

    vertex_groups = object.vertex_groups

    if mode == "REPLACE":

        for vg in vertex_groups:

            vg_name = vg.name
            new_name = vg_name.replace(string_a, string_b)
            vg.name = new_name 


    if mode == "PREFIX":

        for vg in vertex_groups:

            vg_name = vg.name
            new_name = string_a + vg_name
            vg.name = new_name 



    if mode == "SUFFIX":

        for vg in vertex_groups:

            vg_name = vg.name
            new_name = vg_name + string_a
            vg.name = new_name 




def MergeVertexGroup(self, context, object, VG1, VG2, mode):


    if mode == "OBJECT":
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    VG1_VG = bpy.context.object.vertex_groups.get(VG1)
    VG2_VG = bpy.context.object.vertex_groups.get(VG2)


    mode_dict = {
    "0": "ADD",
    "1": "SET",
    "2": "AVG"
    }

    mode_key = mode_dict.get(mode)

    # try:
    #     VG1_VG = bpy.context.object.vertex_groups.get(VG1)
    #     a = VG1_VG.name
    # except:
    #     print("Main Vertex Group Not Found")
    #     return 0
    # try:
    #     VG2_VG = bpy.context.object.vertex_groups.get(VG2)
    #     a = VG2_VG.name
    # except:
    #     print("Other Vertex Group Not Found")
    #     return 0

    if VG1_VG and VG2_VG:

        cmode = bpy.context.mode

        if cmode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='OBJECT', toggle=False)

        Modifier = bpy.context.object.modifiers.new("mix", "VERTEX_WEIGHT_MIX")
        Modifier.vertex_group_a = VG1_VG.name
        Modifier.vertex_group_b = VG2_VG.name
        Modifier.mix_mode = mode_key
        Modifier.mix_set = "B"


    ################################################################

        #2.83 API
        # bpy.ops.object.modifier_apply(apply_as='DATA', modifier=Modifier.name)

        #2.90 API
        #bpy.ops.object.modifier_apply(modifier=Modifier.name)


        if bpy.app.version > (2, 90, 0):
            bpy.ops.object.modifier_apply(modifier=Modifier.name)
        else:
            bpy.ops.object.modifier_apply(apply_as='DATA', modifier=Modifier.name)


    ################################################################

        #
        # if VG1_VG == VG2_VG:
        #     pass
        # else:
        #     Remove_VertexGroup(self, context, VG2_VG.index)
        VG1_VG = bpy.context.object.vertex_groups.get(VG1)
        VG2_VG = bpy.context.object.vertex_groups.get(VG2)
        
        object.vertex_groups.remove(VG2_VG)


        if cmode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='EDIT', toggle=False)




def Set_As_Origin(self, context, index):

        currentMode = context.mode

        if currentMode == "EDIT_MESH":
            bpy.ops.object.mode_set(mode='OBJECT')
            bpy.ops.object.mode_set(mode='EDIT')

        obj = context.object
        verts = [ v for v in obj.data.vertices if index in [ vg.group for vg in v.groups ] ]

        if verts:
            location = find_center_point_from_verts(obj, verts)

            # create_empty("name", location)

            moveOrigin(obj, location)
        else:


            self.report({"INFO"}, "Group is Empty")




def Unassign_Zero_Weight_From_Group(self, context, index):

    currentMode = context.mode
    if currentMode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode='OBJECT')


    object_vertices= context.object.data.vertices
    object_vertex_group = context.object.vertex_groups[index]

    object_data = context.object.data


    selected_vertices = set()



    for vertex in object_vertices:

        for G in vertex.groups:
            if G.group == object_vertex_group.index:
                if G.weight == 0:
                    selected_vertices.add(vertex.index)


    context.object.vertex_groups[index].remove(list(selected_vertices))

    if currentMode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode='EDIT')

    return len(selected_vertices)
    #self.report({"INFO"}, "Removed %s vertices from vetex group" %(len(selected_vertices)))




def Remove_Zero_Weight_Group(self, context):


    if context.mode == "EDIT_MESH":

        bpy.ops.object.mode_set(mode='OBJECT', toggle=False)
        bpy.ops.object.mode_set(mode='EDIT', toggle=False)

    object = context.object
    data = object.data



    Zero_Weight_Group = set()





    for vg in object.vertex_groups:

        Zero_Weight_Vert = []

        for vertex in object.data.vertices:
            for G in vertex.groups:
                if G.group == vg.index:
                    if G.weight == 0:
                        Zero_Weight_Vert.append(True)
                    else:
                        Zero_Weight_Vert.append(False)

        if all(Zero_Weight_Vert):
            Zero_Weight_Group.add(vg)

    count = len(Zero_Weight_Group)

    for vg in Zero_Weight_Group:
        Remove_VertexGroup(self, context, vg.index)

    if count is not None:
        return count
    else:
        return 0




def Vertex_Group_From_Side(self, context, createCenter=False,includeCenter=True, center="ORIGIN"):

    obj = context.object

    current_mode = context.mode

    if current_mode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode = 'OBJECT')


    if center == "ORIGIN":
        compare = 0

    if center == "CENTER":

        compare = find_center_point(obj)[0]

        self.report({"INFO"}, "Center option is not working yet")


    if center == "WORLD":
        self.report({"INFO"}, "World option is not working yet")
        compare = 0

    leftVertex = []
    rightVertex = []
    centerVertex = []

    for vertex in obj.data.vertices:

        if vertex.co[0] > compare:
            rightVertex.append(vertex.index)

        if vertex.co[0] < compare:
            leftVertex.append(vertex.index)

        if vertex.co[0] == compare:
            centerVertex.append(vertex.index)

    left_vg = obj.vertex_groups.new(name="Left")
    right_vg = obj.vertex_groups.new(name="Right")

    if createCenter:
        center_vg = obj.vertex_groups.new(name="center")
        center_vg.add(centerVertex, 1, "REPLACE")


    if includeCenter:
        left_vg.add(centerVertex, 1, "REPLACE")
        right_vg.add(centerVertex, 1, "REPLACE")

    left_vg.add(leftVertex, 1, "REPLACE")
    right_vg.add(rightVertex, 1, "REPLACE")

    if current_mode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode = 'EDIT')




def Vertex_Group_From_Material(self, context):

    obj = context.object
    data = obj.data

    current_mode = context.mode

    if current_mode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode = 'OBJECT')

    vertex_groups = []

    for slot in obj.material_slots:

        vg = obj.vertex_groups.new(name=slot.name)

        vertex_add = []

        for polygon in data.polygons:
            if slot == obj.material_slots[polygon.material_index]:

                for vertex in polygon.vertices:
                    vertex_add.append(vertex)

        vg.add(vertex_add, 1, "REPLACE")


    if current_mode == "EDIT_MESH":
        bpy.ops.object.mode_set(mode = 'EDIT')




def Bone_from_Vertex_Group(self, context, index, use_armature, direction):

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        obj = context.object
        armature_name = "armature_" + obj.name
        armature = create_armature(armature_name, [0,0,0])
        armature.show_in_front = True
        armature.select_set(True)
        bpy.context.view_layer.objects.active = armature
        bpy.ops.object.mode_set(mode='EDIT')

        for vertex_group in obj.vertex_groups:

            verts = [ v for v in obj.data.vertices if vertex_group.index in [ vg.group for vg in v.groups ] ]

            if verts:

                location = find_center_point_from_verts(obj, verts)
                edit_bones = armature.data.edit_bones
                newbone = edit_bones.new(vertex_group.name)
                newbone.head = location
                newbone.tail = location

                if direction == "UP":
                    newbone.tail[2] = location[2] + 1

                if direction == "FRONT":
                    newbone.tail[1] = location[1] - 1





                # armature.data.edit_bones

            else:


                self.report({"INFO"}, "Group is Empty")

        bpy.ops.object.mode_set(mode='OBJECT')
        if use_armature:
            modifier = obj.modifiers.new("Armature", "ARMATURE")
            modifier.object = armature
