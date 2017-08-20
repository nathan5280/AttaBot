# Blender API, and math helper methods
import bpy, mathutils
import os, math

# Py Remote Object Module to support the RPC connection.
import Pyro4

'''
'''

# Expose this interface to external clients.
# Let Pyro manage the instance of this class.  (One per proxy connection.)
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Objects(object):
    def __init__(self):
        pass

    def _select_object(self, object_name):
        # deselect all
        bpy.ops.object.select_all(action='DESELECT')

        # selection
        bpy.data.objects[object_name].select = True

    def remove(self, object_name):
        self._select_object(object_name)

        # remove it
        bpy.ops.object.delete()

    def get_object_names(self):
        return bpy.data.objects.keys()

    def add_plane(self, radius, location):
        '''
        Add a plane to the environment

        Input:
            - radius: 1/2 the length of the side.
            - location: Tuple of (X, Y, Z) point at the center of the plane.

        Output:
            - name: Name of the created plane.
        '''
        bpy.ops.mesh.primitive_plane_add(radius=radius, location=location)
        return bpy.context.active_object.name

    def color_plane(self, object_name, color):
        self._select_object(object_name)
        activeObject = bpy.context.active_object #Set active object to variable
        mat = bpy.data.materials.new(name="MaterialName") #set new material to variable
        activeObject.data.materials.append(mat) #add the material to the object
        bpy.context.object.active_material.diffuse_color = color #change color
