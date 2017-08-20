# Blender API, and math helper methods
import bpy, mathutils
import os, math
from snakeshake.Render import Render

# Py Remote Object Module to support the RPC connection.
import Pyro4

'''
This is the working part of the Snake Shake implementation.  This is where
the code is that runs inside of Blender.   Create methods here and expose them
through Pyro so that the client can call them as if they were local methods in
the same Python environment.

Be careful about what object are passed in the method calls as Pyro need to be
able to serialize them.  See the Pyro documentation for information on how to
set the serializer and security notices.
'''

# Expose this interface to external clients.
# Let Pyro manage the instance of this class.  (One per proxy connection.)
@Pyro4.expose
@Pyro4.behavior(instance_mode="single")
class Env(object):
    def __init__(self, quit_request):
        '''
        Set up the Environment.

        Input:
            - quit_request: Server method to request shutdown.
        '''
        print('Env: Initializing')
        self._render = Render()

        self._quit_request = quit_request

        # Get the Environmentto a known state.
        self.reset()

    def ping(self, s):
        '''
        Respond to ping request from client to verify the Env is running.
        '''
        print('Env: Ping',s)
        return s

    def reset(self):
        # This will all get replaced when we get the methods to create and
        # configure the Env from imported objects.
        print('Env: Resetting Camera')
        cam = bpy.data.objects['Camera']
        cam_p = cam.location
        cam_r = cam.rotation_euler

        cam_p.x, cam_p.y, cam_p.z = 15, 15, 0
        cam_r.x, cam_r.y, cam_r.z = math.pi/2, 0, math.pi*3/4
        self._render.render()
        return cam_p.x, cam_p.y, cam_r.z

    def quit(self):
        '''
        Request to shutdown the Env.
        '''
        print('Env: Quitting')
        # Call back to the server provided method to request it to quit.
        self._quit_request()
