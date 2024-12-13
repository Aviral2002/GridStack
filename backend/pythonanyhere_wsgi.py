import sys
import os

path = '/home/avi1004/GridStack'
if path not in sys.path:
    sys.path.append(path)

from app import app as application
