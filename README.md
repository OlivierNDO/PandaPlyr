## <img src="images/PyPlyr_Icon.png" alt="Project Logo" align="middle" width="80" height="80"> PyPlyr

PyPlyr is a Python package designed to provide a familiar and efficient data manipulation experience similar to the popular dplyr package in R. It aims to simplify and streamline the process of working with tabular data by providing a concise and intuitive syntax.

## Features

- Grouping and summarizing: Group your data by one or more columns and perform aggregation operations on them.

```python
import pandas as pd
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60]})

new_df = (
    df >> 
    group_by('A') >> 
    summarise(AVG_B = ('B', 'mean'),
              TOTAL_B = ('B', 'sum'))
    )
```


- DataFrame pipelining: Utilize the power of the pipe operator (`>>`) to chain together data manipulation operations.
- Column-wise transformations: Create new columns or modify existing ones using vectorized operations.
- Filtering and selection: Filter rows based on conditions and select specific columns of interest.
- Joining and merging: Perform various types of joins and merges between multiple DataFrames.
- Sorting and ordering: Arrange your data based on one or more columns in ascending or descending order.

## Install