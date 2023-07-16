### Configuration
###############################################################################
# Import packages
import numpy as np
import pandas as pd
import re

# Import modules
from src import pyplyr as pp




df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60]})

new_df = (
    df >> 
    pp.group_by('A') >> 
    pp.summarise(AVG_B = ('B', 'mean'),
              TOTAL_B = ('B', 'sum'))
    )







