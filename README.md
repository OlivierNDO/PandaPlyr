## <img src="images/PyPlyr_Icon.png" alt="Project Logo" width="80" height="80"> PandaPlyr

PandaPlyr is a Python package designed to provide a familiar and efficient data manipulation experience similar to the popular dplyr package in R. It aims to simplify and streamline the process of working with tabular data by providing a concise and intuitive syntax.



## Overview and vision for PandaPlyr
The purpose of PyPlyr is to make chained operations on pandas DataFrames easier and more readable.

Use case and example
--------------------
I have two dataframes - grade_df (left) and subject_df (right).


<table>
<tr><td>

| StudentID |   Subject   | Grade  |
|:---------:|:-----------:|:------:|
|     1     |   CompSci   |   80   |
|     1     |   English   |   85   |
|     1     |   History   |   75   |
|     1     | LinearAlg   |   75   |
|    ...    |     ...     |   ...  |



</td><td>
                 
</td>
<td>

|      Subject     | SubjectType |
|:----------------:|:-----------:|
|     CompSci      |     STEM    |
|   LinearAlg      |     STEM    |
|    Philosophy    |  Humanities |
|     English      |  Humanities |
|     History      |  Humanities |


</td></tr> 
</table>

Merge the dataframes and find the student with the highest average grade for Humanities classes only,
but exclude any students ('StudentID') who are not enrolled in at least 2 humanities courses.

```python
import pandas as pd
import PandaPlyr as pp
grade_df = pp.read_grades_dataset()
subject_df = pp.read_subject_dataset()
```

In pandas
----------
```python
merged_df = pd.merge(grade_df, subject_df, on='Subject')

humanities_df = merged_df[merged_df['SubjectType'] == 'Humanities']

course_counts = (
    humanities_df
    .groupby('StudentID', as_index = False)
    .agg(CourseCount = ('Subject', 'count'))
)

filtered_students =  course_counts.loc[course_counts['CourseCount'] >= 2][['StudentID']]

top_student_pandas = (
    humanities_df.loc[humanities_df['StudentID'].isin(filtered_students['StudentID'])]
    .groupby('StudentID', as_index=False)
    .agg(AverageGrade = ('Grade', 'mean'))
    .sort_values('AverageGrade', ascending = False)
    .head(1)
)
```

In PyPlyr
----------
```python
top_student_pp = (
    grade_df >>
    pp.inner_join(subject_df, 'Subject') >>
    pp.where('SubjectType == "Humanities"') >>
    pp.group_by('StudentID', 'SubjectType') >>
    pp.summarise(AverageGrade = ('Grade', 'mean'), CourseCount = ('Grade', 'count')) >>
    pp.where('(CourseCount >= 2)') >>
    pp.mutate(MaxAverageGrade = 'AverageGrade.max()') >>
    pp.where('MaxAverageGrade == AverageGrade') >>
    pp.select('StudentID', 'AverageGrade')
    )
```

The same answer takes 8 fewer lines, ~ 145 fewer characters, and is lot more readable.

| StudentID | AverageGrade |
|:---------:|:------------:|
|     2     |     87.0     |




## Features

Here's a quick summary of the classes, methods, and functions we'll cover:


#### group_by() and summarise() / summarize()
These functions allow group-wise aggregations on your DataFrame for one or more columns. The syntax is as follows:
```python
import pandas as pd
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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
from pandaplyr import *
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

#### fillna()
replaces numpy.nan, None, and (unlike pandas fillna) it works on numpy.inf and -numpy.inf
```python
import pandas as pd
from pandaplyr import *
df = pd.DataFrame({'A': [1, np.nan, None, np.inf, -np.inf]})
new_df = df >> fillna('A', 0)
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


#### dropna()
replaces numpy.nan, None, and (unlike pandas fillna) it works on numpy.inf and -numpy.inf
```python
import pandas as pd
from pandaplyr import *
df = pd.DataFrame({'A': [1, np.nan, None, np.inf, -np.inf]})
new_df = df >> fillna('A', 0)
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




The Pipe class allows us to use the '>>' operator to chain operations together in a pipeline.

---------------------------------------------


## User-defined functions

You can define your own functions using the @Pipe decorator


```python
import pandas as pd
from pandaplyr import *

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




## Install
```bash
pip install PandaPlyr
```


## To-do list

- [X] Add error handling to pyplyr.py
- [ ] Add unit tests for new functions


## Future features

- [ ] Polars backend
- [ ] Intelligent multiprocessing
