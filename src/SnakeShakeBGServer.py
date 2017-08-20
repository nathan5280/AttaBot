# Py Remote Object Module to support the RPC connection.
import Pyro4

# Support for sockets
import select

# The Class that is remotely exposed through RPC to the client outside of Blender.
from snakeshake.Env import Env
from snakeshake.Render import Render
from snakeshake.Camera import Camera
from snakeshake.Objects import Objects

# Make sure the server is only using one thread to not confuse Blender
Pyro4.config.SERVERTYPE="multiplex"

class SnakeShakeBGServer(object):
    '''
    Pyro4 server implementation that runs in a background Blender environment.
    The server waits on the socket for client requests and delegates them to
    the Env.

    The client/environment can request that the Server stop through the
    quit_request() method.

    Note that this script loads immediately within the Blender Python environment
    and has total control of the environment.  Control is not passed back to
    Blender until the script exits.
    '''

    def __init__(self):
        '''
        Initialize the server, create the Env.
        '''
        self._daemon = Pyro4.Daemon()

        # Time to wait on the socket for a client request.
        # Timeout periodically to see if a quit request has been reeived.
        self._socket_wait = 5
        self._quit = False

        # Create the Env object that we are exposing and tell it
        # where to call if a quit request is received from the client.
        self._env = Env(self._quit_request)
        self._render = Render()
        self._camera = Camera()
        self._objects = Objects()

        env_uri = self._daemon.register(self._env, 'Env')
        render_uri = self._daemon.register(self._render, 'Render')
        camera_uri = self._daemon.register(self._camera, 'Camera')
        objects_uri = self._daemon.register(self._objects, 'Objects')

        # Register the server with the name server so that clients can the
        # server on the network.
        ns = Pyro4.locateNS()
        ns.register('Env', env_uri)
        ns.register('Render', render_uri)
        ns.register('Camera', camera_uri)
        ns.register('Objects', objects_uri)

    def process_events(self):
        '''
        Start the server event loop.  Run until quit_request is called.
        '''
        while not self._quit:
            s,_,_ = select.select(self._daemon.sockets,[],[], self._socket_wait)
            self._daemon.events(s)

    def _quit_request(self):
        '''
        Request he server to quit at its next available opportunity.  This
        opportunity is when it is processing the next request or when the sockets
        times out.
        '''
        print('SnakeShakeServer: Quit request')
        self._quit = True

    def shutdown(self):
        '''
        Finish shutting down the server.
        '''
        # Unregister the server so that the name server doesn't hand out dead connections.
        self._daemon.unregister(self._env)
        self._deamon.unregister(self._render)
        self._deamon.unregister(self._camera)
        self._deamon.unregister(self._objects)
        self._daemon.close()
        self._daemon = None
        print('SnakeShakeServer: Stopped')


if __name__ == '__main__':
    # Create the server and register with the name server.
    s = SnakeShakeBGServer()

    # Start the event loop.
    s.process_events()

    # Shutdown the server.
    s.shutdown()
