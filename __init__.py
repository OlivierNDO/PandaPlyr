# PandaPlyr/__init__.py

# Import statements
import sys
import os.path
sys.path.insert(1, os.path.dirname(sys.path[0]))

from .src import pandaplyr

# Variables
version = "0.0.3"
author = "Nick Olivier"

# Function
def greet():
    print("Welcome to PandaPlyr!")
