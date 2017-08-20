# Blender API, and math helper methods
import bpy, mathutils
import os, math

# Py Remote Object Module to support the RPC connection.
import Pyro4

from snakeshake.Render import Render

'''
'''

# Expose this interface to external clients.
# Let Pyro manage the instance of this class.  (One per proxy connection.)
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Camera(object):
    def __init__(self):
        self._render = Render()

    def get_camera_position(self):
        '''
        Get the x, y, z location of the camera.
        '''
        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler
        return cam_p.x, cam_p.y, cam_r.z

    def move_camera(self, dx, dy, drz):
        '''
        Move the camera by the delta position and rotation in the
        XY plane.

        Input:
            - dx: Change along the X-axis
            - dy: Change along the Y-axis
            - drz: Change in rotation about the Z-axis
        Return:
            - x, y, rz: the new position of the camera.
        '''

        print('Env: Move dx={}, dy={}, rz={}'.format(dx,dy,drz))

        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x += dx
        cam_p.y += dy
        cam_p.z = 0

        cam_r.x = math.pi/2
        cam_r.y = 0
        cam_r.z += drz

        self._render.render()

        return cam_p.x, cam_p.y, cam_r.z
