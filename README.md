## <img src="images/PyPlyr_Icon.png" alt="Project Logo" width="80" height="80"> PyPlyr

PyPlyr is a Python package designed to provide a familiar and efficient data manipulation experience similar to the popular dplyr package in R. It aims to simplify and streamline the process of working with tabular data by providing a concise and intuitive syntax.

## Features

Here's a quick summary of the classes, methods, and functions we'll cover:


#### group_by() and summarise()
These functions allow group-wise aggregations on your DataFrame for one or more columns. The syntax is as follows:
```python
import pandas as pd
from pyplyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'Z' : ['x', 'x', 'y', 'x', 'x', 'y'],
                   'B': [10, 20, 30, 40, 50, 60]})
new_df = df >> group_by('A', 'Z') >> summarise(AVG_B = ('B', 'mean'))
print(new_df)
```

<table>
<tr><td>

|    | A   | Z   |   B |
|---:|:----|:----|----:|
|  0 | foo | x   |  10 |
|  1 | foo | x   |  20 |
|  2 | foo | y   |  30 |
|  3 | bar | x   |  40 |
|  4 | bar | x   |  50 |
|  5 | bar | y   |  60 |


</td><td>
------>
</td><td>

| A   | Z | AVG_B |
|-----|---|-------|
| foo | x | 15.0  |
| foo | y | 30.0  |
| bar | x | 45.0  |
| bar | y | 60.0  |

</td></tr> 
</table>


Note that you can pass the columns as separate arguments, or inside a list. By default, it will not return indices.

---------------------------------------------


#### mutate()
The mutate function lets you add new columns or modify existing ones.
```python
import pandas as pd
from pyplyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> mutate(B_X_2 = 'B * 2', B_PLUS_C = 'B + C')
print(new_df)
```

|    | A   |   B |   C |   B_X_2 |   B_PLUS_C |
|---:|:----|----:|----:|--------:|-----------:|
|  0 | foo |  10 |   1 |      20 |         11 |
|  1 | foo |  20 |   2 |      40 |         22 |
|  2 | foo |  30 |   3 |      60 |         33 |
|  3 | bar |  40 |   4 |      80 |         44 |
|  4 | bar |  50 |   5 |     100 |         55 |
|  5 | bar |  60 |   6 |     120 |         66 |



---------------------------------------------

#### where()
This function allows you to filter rows in your DataFrame based on a condition.
```python
import pandas as pd
from pyplyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> where('A == "foo" | C == 6')
print(new_df)
```

|    | A   |   B |   C |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  5 | bar |  60 |   6 |

---------------------------------------------

#### select()
The select function can be used to select specific columns in your DataFrame.
```python
import pandas as pd
from pyplyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> select('A', 'B')
print(new_df)
```

|    | A   |   B |
|---:|:----|----:|
|  0 | foo |  10 |
|  1 | foo |  20 |
|  2 | foo |  30 |
|  3 | bar |  40 |
|  4 | bar |  50 |
|  5 | bar |  60 |

---------------------------------------------

#### rename()
You can rename columns in your DataFrame using the rename function.
```python
import pandas as pd
from pyplyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> rename(Z = 'C')
print(new_df)
```

|    | A   |   B |   Z |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  3 | bar |  40 |   4 |
|  4 | bar |  50 |   5 |
|  5 | bar |  60 |   6 |


---------------------------------------------

#### arrange() and order_by()
Use arrange or order_by (which are 100% identical) to sort your DataFrame by one or more columns.
```python
import pandas as pd
from pyplyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60]})
new_df = df >> arrange('B', 'desc')
print(new_df)
```

|    | A   |   B |
|---:|:----|----:|
|  5 | bar |  60 |
|  4 | bar |  50 |
|  3 | bar |  40 |
|  2 | foo |  30 |
|  1 | foo |  20 |
|  0 | foo |  10 |


---------------------------------------------

#### left_join(), right_join(), full_join()
These functions allow you to join multiple DataFrames together.
```python
import pandas as pd
df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'],
                    'B': [1, 2, 3]})

df2 = pd.DataFrame({'A': ['foo', 'bar', 'foo'],
                    'C': [10, 20, 30]})

new_df = df1 >> left_join(df2, on = 'A', fill_na = 0)
print(new_df)
```

|    | A     |   B |   C |
|---:|:------|----:|----:|
|  0 | foo   |   1 |  10 |
|  1 | foo   |   1 |  30 |
|  2 | bar   |   2 |  20 |
|  3 | other |   3 |   0 |

Note that left_join and full_join have an optional fill_na argument to replace numpy.nan values from merged fields.

---------------------------------------------

#### union() and union_all()
union and union_all let you concatenate two DataFrames together.

Note that union removes duplicates while union_all doesn't.
```python

```

---------------------------------------------

#### distinct()
distinct removes duplicate rows in your DataFrame.
```python

```

---------------------------------------------

#### Pipe class
```python

```

The Pipe class allows us to use the '>>' operator to chain operations together in a pipeline.

---------------------------------------------




<table>
<tr><td>

|   | A     | B |
|---|-------|---|
| 0 | foo   | 1 |
| 1 | foo   | 1 |
| 2 | bar   | 2 |
| 3 | other | 3 |

</td><td>
------>
</td><td>

|   | A     | B | C |
|---|-------|---|---|
| 0 | foo   | 1 |10 |
| 1 | foo   | 1 |30 |
| 2 | bar   | 2 |20 |
| 3 | other | 3 | 0 |

</td></tr> 
</table>






## Install