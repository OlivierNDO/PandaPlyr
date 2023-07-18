### Configuration
###############################################################################
# Import packages
import numpy as np
import pandas as pd
import re

# Import modules
from src import pyplyr as pp
from src.pyplyr import *

import importlib
#importlib.reload(src.pyplyr)

df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60]})


df >> arrange('B', 'desc')


new_df = (
    df >> 
    group_by('A') >> 
    summarise(AVG_B = ('B', 'mean'),
              TOTAL_B = ('B', 'sum'))
    )







