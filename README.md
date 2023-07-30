## <img src="images/PyPlyr_Icon.png" alt="Project Logo" width="80" height="80"> PandaPlyr

[![PyPI version](https://badge.fury.io/py/pandaplyr.svg)](https://badge.fury.io/py/pandaplyr)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

PandaPlyr is a Python package designed to provide a familiar and efficient data manipulation experience similar to the popular dplyr package in R. It aims to simplify and streamline the process of working with tabular data by providing a concise and intuitive syntax. The purpose of pandaplyr is to make chained operations on pandas DataFrames easier and more readable.

## Table of Contents

- [Installing](#installing)
- [Features](#features)
    - [group_by and summarise / summarize](#group_by-and-summarise--summarize)
    - [mutate](#mutate)
    - [where](#where)
    - [select](#select)
    - [rename](#rename)
    - [arrange and order_by](#arrange-and-order_by)
    - [left_join, right_join, full_join](#left_join-right_join-full_join)
    - [union and union_all](#union-and-union_all)
    - [distinct](#distinct)
    - [fill_na](#fill_na)
    - [drop_na](#drop_na)
    - [sample_n and sample_frac](#sample_n-and-sample_frac)
    - [head and tail](#head-and-tail)
- [User-defined functions](#user-defined-functions)
- [Future features](#future-features)
- [Contact](#contact)

## Installing

Installers for the latest version are available at the [Python
Package Index (PyPI)](https://pypi.org/project/pandaplyr/).

```bash
pip install PandaPlyr
```


## Use case and example
Given the student grades by year dataset, find the 5 students with the most improved average grade across all subjects.

```python
import PandaPlyr
from PandaPlyr import *
df = PandaPlyr.utils.read_grades_by_year_dataset()
```

| StudentID | Year | Subject | Grade |
|-----------|------|---------|-------|
| 1         | 1    | Math    | 100   |
| 1         | 2    | Math    | 87    |
| 1         | 1    | Science | 89    |
| 1         | 2    | Science | 93    |
| 2         | 1    | English | 78    |
| 2         | 2    | English | 86    |
| 2         | 1    | Math    | 78    |
| 2         | 2    | Math    | 79    |
| 2         | 1    | Science | 89    |
| 2         | 2    | Science | 64    |


##### PandaPlyr
-----------------
```python
top_five_improved = (
    df >>
    group_by('StudentID', 'Year') >>
    summarise(AvgGrade = ('Grade', 'mean')) >>
    mutate(GradeChange = 'np.where(Year == 1, -1 * AvgGrade, AvgGrade)') >>
    group_by('StudentID') >>
    summarise(GradeChange = ('GradeChange', 'sum')) >>
    order_by('GradeChange', 'desc') >>
    head(5)                        
)
```

| StudentID | GradeChange |
|-----------|-------------|
| 66        | 26.0        |
| 205       | 23.5        |
| 380       | 22.0        |
| 40        | 22.0        |
| 170       | 22.0        |


##### Pandas
-----------------
```python
avg_grades = df.groupby(['StudentID', 'Year'])['Grade'].mean().reset_index()

avg_grades['GradeChange'] = avg_grades.groupby('StudentID')['Grade'].diff()

top_five_improved = (
    avg_grades[avg_grades['Year'] == 2]
    .sort_values('GradeChange', ascending=False)
    .head(5)
    [['StudentID', 'GradeChange']]
)
```

The pandas code is fine, but PandaPlyr lets you use a single chained command that's more readable.


## Features

Here's a quick summary of the classes, methods, and functions we'll cover:


#### group_by() and summarise() / summarize()
These functions allow group-wise aggregations on your DataFrame for one or more columns. The syntax is as follows:
```python
import pandas as pd
from PandaPlyr import *
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
Functions summarize() and summarise() are identical.


---------------------------------------------


#### mutate()
The mutate function lets you add new columns or modify existing ones.
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> mutate(B_X_2 = 'B * 2',
                      B_PLUS_C = 'B + C',
                      CONST = 1)
print(new_df)
```

|    | A   |   B |   C |   B_X_2 |   B_PLUS_C | CONST |
|---:|:----|----:|----:|--------:|-----------:|------:|
|  0 | foo |  10 |   1 |      20 |         11 |   1   |
|  1 | foo |  20 |   2 |      40 |         22 |   1   |
|  2 | foo |  30 |   3 |      60 |         33 |   1   |
|  3 | bar |  40 |   4 |      80 |         44 |   1   |
|  4 | bar |  50 |   5 |     100 |         55 |   1   |
|  5 | bar |  60 |   6 |     120 |         66 |   1   |



---------------------------------------------

#### where()
This function allows you to filter rows in your DataFrame based on a condition.
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> where('A == "foo" | C == 6')
print(new_df)
```

<table>
<tr><td>

|    | A   |   B |   C |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  3 | bar |  40 |   4 |
|  4 | bar |  50 |   5 |
|  5 | bar |  60 |   6 |

</td><td>

------>

</td><td>

|    | A   |   B |   C |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  5 | bar |  60 |   6 |

</td></tr> 
</table>



---------------------------------------------

#### select()
The select function can be used to select specific columns in your DataFrame.
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> select('A', 'B')
print(new_df)
```

<table>
<tr><td>

|    | A   |   B |   C |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  3 | bar |  40 |   4 |
|  4 | bar |  50 |   5 |
|  5 | bar |  60 |   6 |

</td><td>

------>

</td><td>

|    | A   |   B |
|---:|:----|----:|
|  0 | foo |  10 |
|  1 | foo |  20 |
|  2 | foo |  30 |
|  3 | bar |  40 |
|  4 | bar |  50 |
|  5 | bar |  60 |

</td></tr> 
</table>




---------------------------------------------

#### rename()
You can rename columns in your DataFrame using the rename function.
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60],
                   'C': [1, 2, 3, 4, 5, 6]})
new_df = df >> rename(Z = 'C')
print(new_df)
```

<table>
<tr><td>

|    | A   |   B |   C |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  3 | bar |  40 |   4 |
|  4 | bar |  50 |   5 |
|  5 | bar |  60 |   6 |

</td><td>

------>

</td><td>

|    | A   |   B |   Z |
|---:|:----|----:|----:|
|  0 | foo |  10 |   1 |
|  1 | foo |  20 |   2 |
|  2 | foo |  30 |   3 |
|  3 | bar |  40 |   4 |
|  4 | bar |  50 |   5 |
|  5 | bar |  60 |   6 |

</td></tr> 
</table>

---------------------------------------------

#### arrange() and order_by()
Use arrange or order_by (which are 100% identical) to sort your DataFrame by one or more columns.
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, 20, 30, 40, 50, 60]})
new_df = df >> arrange('B', 'desc')
print(new_df)
```
<table>
<tr><td>

|    | A   |   B |
|---:|:----|----:|
|  0 | foo |  10 |
|  1 | foo |  20 |
|  2 | foo |  30 |
|  3 | bar |  40 |
|  4 | bar |  50 |
|  5 | bar |  60 |

</td><td>

------>

</td><td>

|    | A   |   B |
|---:|:----|----:|
|  5 | bar |  60 |
|  4 | bar |  50 |
|  3 | bar |  40 |
|  2 | foo |  30 |
|  1 | foo |  20 |
|  0 | foo |  10 |

</td></tr> 
</table>





---------------------------------------------

#### left_join(), right_join(), full_join()
These functions allow you to join multiple DataFrames together.
```python
import pandas as pd
from PandaPlyr import *
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
import pandas as pd
from PandaPlyr import *
df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'],
                    'B': [1, 2, 3]})

df2 = pd.DataFrame({'A': ['other', 'bar', 'foo'],
                    'B': [3, 4, 5]})

new_df = df1 >> union(df2)
print(new_df)
```

|    | A     |   B |
|---:|:------|----:|
|  0 | foo   |   1 |
|  1 | bar   |   2 |
|  2 | other |   3 |
|  3 | bar   |   4 |
|  4 | foo   |   5 |


```python
import pandas as pd
from PandaPlyr import *
df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'],
                    'B': [1, 2, 3]})

df2 = pd.DataFrame({'A': ['other', 'bar', 'foo'],
                    'B': [3, 4, 5]})

new_df = df1 >> union_all(df2)
print(new_df)
```

|    | A     |   B |
|---:|:------|----:|
|  0 | foo   |   1 |
|  1 | bar   |   2 |
|  2 | other |   3 |
|  3 | other |   3 |
|  4 | bar   |   4 |
|  5 | foo   |   5 |



---------------------------------------------

#### distinct()
distinct removes duplicate rows in your DataFrame.
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': ['foo', 'bar', 'other', 'other']})

new_df = df >> distinct()
print(new_df)
```

<table>
<tr><td>

|    | A     |
|---:|:------|
|  0 | foo   |
|  1 | bar   |
|  2 | other |
|  3 | other |


</td><td>

------>

</td><td>

|    | A     |
|---:|:------|
|  0 | foo   |
|  1 | bar   |
|  2 | other |

</td></tr> 
</table>


---------------------------------------------

#### fill_na()
replaces numpy.nan, None, and (unlike pandas fillna) it works on numpy.inf and -numpy.inf
```python
import pandas as pd
from PandaPlyr import *
df = pd.DataFrame({'A': [1, np.nan, None, np.inf, -np.inf]})
new_df = df >> fill_na('A', 0)
print(new_df)
```

|    | A     |
|---:|:------|
|  0 | 1.0   |
|  1 | 0.0   |
|  2 | 0.0   |
|  3 | 0.0   |
|  4 | 0.0   |

---------------------------------------------


#### drop_na()
Removes records with numpy.nan, None, and (unlike pandas dropna) it works on numpy.inf and -numpy.inf
```python
import pandas as pd
from src.PandaPlyr import *
df = pd.DataFrame({'A': [1, np.nan, None, np.inf, -np.inf]})
new_df = df >> drop_na()
print(new_df)
```

|    | A     |
|---:|:------|
|  0 | 1.0   |


---------------------------------------------


#### sample_n() and sample_frac()
Randomly samples n rows (sample_n) or a fraction of rows (sample_frac) from the DataFrame. The random_state argument ensures reproducible results.
```python
import pandas as pd
from src.PandaPlyr import *
df = pd.DataFrame({'A': range(10)})
new_df = df >> sample_n(5, random_state=42)
print(new_df)
```

|    | A     |
|---:|:------|
|  0 | 8.0   |
|  0 | 1.0   |
|  0 | 5.0   |
|  0 | 0.0   |
|  0 | 2.0   |

---------------------------------------------


#### head() and tail()
Return the first or last n rows of a DataFrame, respectively.
```python
import pandas as pd
from src.PandaPlyr import *
df = pd.DataFrame({'A': range(10)})
new_df = df >> head(5) >> tail(2)
print(new_df)
```

|    | A   |
|---:|:----|
|  0 | 3   |
|  0 | 4   |

---------------------------------------------



The Pipe class allows us to use the '>>' operator to chain operations together in a pipeline.

---------------------------------------------


## User-defined functions

You can define your own functions using the @Pipe decorator


```python
import pandas as pd
from PandaPlyr import *

@Pipe
def median_impute(df, *args):
    """Replace missing values with the median value in the column"""
    for col in args:
        col_median = np.nanmedian(df[col])
        df = df >> fillna(col, value = col_median)
    return df

df = pd.DataFrame({'A': ['X', None, 'Y', np.inf, 'X', 'Y'],
                   'B': [1, 2, 3, None, 5, 6]})

new_df = df >> fillna('A', 'Missing') >> median_impute('B')
print(new_df)
```

<table>
<tr><td>

|    | A      |   B |
|---:|:-------|----:|
|  0 | X      |   1 |
|  1 | None   |   2 |
|  2 | Y      |   3 |
|  3 | np.inf |None |
|  4 | X      |   5 |
|  5 | Y      |   6 |


</td><td>

------>

</td><td>

|    | A      |   B |
|---:|:-------|----:|
|  0 | X      |   1 |
|  1 | Missing|   2 |
|  2 | Y      |   3 |
|  3 | Missing|   3 |
|  4 | X      |   4 |
|  5 | Y      |   5 |

</td></tr> 
</table>



## Future features
- [ ] Benchmarking module
- [ ] Polars backend
- [ ] Intelligent multiprocessing


## Contact
[![LinkedIn Badge](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/oliviernicholas/)

<!-- Keywords: dplyr for Python, dplyr for pandas, PandaPlyr, data analysis, R for python, tidyverse for Python, magrittr, dplyr, pandas-->
