import sys
import Pyro4
import math
import time
from curses import wrapper

def main():
    sys.excepthook = Pyro4.util.excepthook
    env = Pyro4.Proxy("PYRONAME:Env")

    env.quit()

if __name__ == '__main__':
    main()
