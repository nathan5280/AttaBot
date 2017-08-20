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
class Render(object):
    def __init__(self):
        # Information on how images rendered to disk will be named and indexed.
        self._image_idx = 1

    def get_render_resolution(self):
        '''
        Get the current render resolution settings.

        Input:

        Output:
            - x resolution
            - y resolution
        '''
        return bpy.data.scenes["Scene"].render.resolution_x, \
                bpy.data.scenes["Scene"].render.resolution_y

    def set_render_resolution(self, new_x_resolution, new_y_resolution):
        '''
        Set the render resolution

        Input:
            - new_x_resolution:
            - new_y_resolution:
        '''
        bpy.data.scenes["Scene"].render.resolution_x = new_x_resolution
        bpy.data.scenes["Scene"].render.resolution_y = new_y_resolution

    def render(self):
        '''
        Render the image to disk.
        '''
        bpy.ops.render.render(use_viewport=True)
        # bpy.context.scene.render.filepath = 'img/n{0:05d}.png'.format(self._image_idx)
        bpy.context.scene.render.filepath = 'img/n.png'.format(self._image_idx)
        self._image_idx += 1
        bpy.ops.render.render(write_still=True)
