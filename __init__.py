# PandaPlyr/__init__.py

# Import statements
import sys
import os.path
sys.path.insert(1, os.path.dirname(sys.path[0]))

from src.pandaplyr import *

# Variables
version = "0.0.6"
author = "Nick Olivier"

# Function
def greet():
    print("Welcome to PandaPlyr!")
