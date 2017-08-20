import sys
import Pyro4
import math
import time
from curses import wrapper

def main():
    sys.excepthook = Pyro4.util.excepthook
    env = Pyro4.Proxy("PYRONAME:Env")
    render = Pyro4.Proxy("PYRONAME:Render")
    camera = Pyro4.Proxy("PYRONAME:Camera")
    objects = Pyro4.Proxy("PYRONAME:Objects")

    obj_names = objects.get_object_names()
    print(obj_names)

    keep_list = ['Camera', 'Lamp']
    for obj_name in obj_names:
        if obj_name not in keep_list:
            objects.remove(obj_name)

    floor_name = objects.add_plane(10, (0,0,0))
    objects.color_plane(floor_name, )


if __name__ == '__main__':
    main()
