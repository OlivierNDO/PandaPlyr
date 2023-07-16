## <img src="images/PyPlyr_Icon.png" alt="Project Logo" width="80" height="80"> PyPlyr

PyPlyr is a Python package designed to provide a familiar and efficient data manipulation experience similar to the popular dplyr package in R. It aims to simplify and streamline the process of working with tabular data by providing a concise and intuitive syntax.

## Features

Here's a quick summary of the classes, methods, and functions we'll cover:


#### group_by()
This function groups your DataFrame by one or more columns. The syntax is as follows:
```python
import pandas as pd
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'Z' : ['x', 'x', 'y', 'x', 'x', 'y'],
                   'B': [10, 20, 30, 40, 50, 60]})
new_df = df >> group_by('A', 'Z') >> summarise(AVG_B = ('B', 'mean'))
print(new_df)
```

| A   | Z | AVG_B |
|-----|---|-------|
| foo | x | 15.0  |
| foo | y | 30.0  |
| bar | x | 45.0  |
| bar | y | 60.0  |


Note that you can pass the columns as separate arguments, or inside a list. By default, it will not return indices.

---------------------------------------------

#### summarise()
This function allows you to perform aggregation operations on your DataFrame.
```python
import pandas as pd
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'Z' : ['x', 'x', 'y', 'x', 'x', 'y'],
                   'B': [10, 20, 30, 40, 50, 60]})
new_df = df >> group_by('A', 'Z') >> summarise(AVG_B = ('B', 'mean'))
```

#### mutate()
The mutate function lets you add new columns or modify existing ones.


---------------------------------------------

#### where()
This function allows you to filter rows in your DataFrame based on a condition.

---------------------------------------------

#### select()
The select function can be used to select specific columns in your DataFrame.

---------------------------------------------

#### rename()
You can rename columns in your DataFrame using the rename function.

---------------------------------------------

#### arrange()
Use arrange to sort your DataFrame by one or more columns.

---------------------------------------------

#### left_join(), right_join(), full_join()
These functions allow you to join multiple DataFrames together.

---------------------------------------------

#### union() and union_all()
union and union_all let you concatenate two DataFrames together.

Note that union removes duplicates while union_all doesn't.

---------------------------------------------

#### distinct()
distinct removes duplicate rows in your DataFrame.

---------------------------------------------

#### Pipe class

The Pipe class allows us to use the '>>' operator to chain operations together in a pipeline.

---------------------------------------------








## Install