### Configuration
###############################################################################
# Import packages
import numpy as np
import pandas as pd
import re

# Import modules
import src.pyplyr as pp



# Import modules
from src.pyplyr import *



@Pipe
def mutate(df, **kwargs):
    """
    Function to create new columns or modify existing columns in a pandas DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    **kwargs : dict
        The column names and corresponding operations.

    Returns:
    --------
    pandas.DataFrame
        The modified DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'B': [10, 20, 30, 40, 50, 60],
                       'C': [1, 2, 3, 4, 5, 6]})
    new_df = df >> mutate(B_X_2 = 'B * 2', B_PLUS_C = 'B + C')
    """
    df_copy = df.copy()
    for column, operation in kwargs.items():
        if isinstance(operation, str):
            # split by operations
            operations = re.split(r'(\W+)', operation)
            # replace column names with df['column_name']
            operations = [f'df_copy["{op}"]' if op in df_copy.columns else op for op in operations]
            # join operations into a single string and evaluate
            df_copy[column] = eval(''.join(operations))
        else:
            df_copy[column] = operation(df_copy)
    return df_copy




from pyplyr import Pipe
import re




    
df = pd.DataFrame({'A': ['foo', 'bar', 'other', 'other']})
new_df = df >> mutate(B = 1)






toy_df = pp.read_titanic_dataset()

toy_df.head()



df = (
    toy_df >>
    pp.drop_na('age') >> 
    pp.mutate(is_child = 'age < 18',
              count_col = 1) >> 
    pp.group_by('is_child', 'survived') >> 
    pp.summarise(Count = ('age', 'count'))
)



df = pd


@Pipe
def median_impute(df, *args):
    """Replace missing values with the median value in the column"""
    for col in args:
        col_median = np.nanmedian(df[col])
        df = df >> fillna(col, value = col_median)
    return df

df = pd.DataFrame({'A': ['foo', None, 'foo', 'bar', 'bar', 'bar'],
                   'B': [10, None, 30, np.inf, 50, 60],
                   'C': [1, 2, 3, None, 5, 6]})

imp_df = df >> median_impute('B', 'C')



df >> fillna('C', 0)

@Pipe
def drop_na(df):
    return df[column_name].str.len.max()


toy_df >> get_max_str_len('sex')




def custom_function(column):
    def wrapper(df, *args, **kwargs):
        df[column] = df[column].apply(lambda x: x * args[0], *args[1:], **kwargs)
        return df
    return wrapper

# Example usage
df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [10, 20, 30, 40]})

# Using the custom function with the pipe
new_df = df >> custom_function('B')(2)




# Example of a custom function
@CustomFunction
def custom_multiply(df, column):
    df[column] = df[column] * 2
    return df



df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [10, 20, 30, 40]})

# Using the custom function with the pipe
new_df = df >> custom_multiply('B')


def custom_function(func):
    def wrapper(*args, **kwargs):
        def inner_func(df):
            return func(df, *args, **kwargs)
        return inner_func
    return wrapper

# Example of a custom function
@custom_function
def custom_multiply(df, column, factor):
    df[column] = df[column] * factor
    return df

# Example usage
df = pd.DataFrame({'A': [1, 2, 3, 4], 'B': [10, 20, 30, 40]})

# Using the custom function with the pipe
new_df = df >> custom_multiply('B', factor=2)






def add_forty(x: float):
    return x + 40
df = pd.DataFrame({'A': [10, 20, 30]})
new_df = df >> mutate(B='add_forty(A)')

print(new_df)


@custom_functions
def add_forty(x: float):
    return x + 40

# Example usage
df = pd.DataFrame({'A': [10, 20, 30]})
new_df = df >> mutate(B='add_forty(A)')

print(new_df)



# Example custom function
@custom_function
def add_forty(x: float):
    return x + 40


# Example usage
df = pd.DataFrame({'A': [10, 20, 30]})
new_df = df >> mutate(B='add_forty(A)')




# Example usage
df = pd.DataFrame({'A': [1, np.nan, 3, np.nan, 5, None, np.inf]})
result_df = df >> fillna('A', 0)
print(result_df)

@Pipe
def add_forty(x : float):
    return x + 40


df = pd.DataFrame({'A' : [10, 20, 30]})


df >> mutate(B = 'add_forty(A)')



survival_by_age_group = (
    toy_df >>
    mutate(age_group = '(age // 10) * 10') >>
    add_forty(age)
    )


survival_by_age_group[['age_group']].drop_duplicates()


survival_by_pclass = (
    toy_df >>
    group_by('pclass') >>
    summarise(n_records = count_records())
    
    )


toy_df >> count_records()

survival_by_pclass = (
    toy_df >>
    group_by('pclass') >>
    summarise(n_records = ('survived', 'count'))
    
    )











df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
    'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
    'C': [1, 2, 3, 4, 5, 6, 7, 8],
    'D': [10, 20, 30, 40, 50, 60, 70, 80],
    'ID': ['a', 'a', 'b', 'b', 'c', 'd', 'e', 'f']
})

summary_df = (
    df >>
    summarize(Records_Count=count_records())
)
























survival_by_pclass



from pyplyr import summarize, count

# Example DataFrame
df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
    'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
    'C': [1, 2, 3, 4, 5, 6, 7, 8],
    'D': [10, 20, 30, 40, 50, 60, 70, 80],
    'ID': ['a', 'a', 'b', 'b', 'c', 'd', 'e', 'f']
})

summary_df = (
    df >>
    summarize(Total_Count=count())#, B_Count=count('B'))
)

print(summary_df)





def count():
    return ('_count', 'size')

# Example usage
df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
    'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
    'C': [1, 2, 3, 4, 5, 6, 7, 8],
    'D': [10, 20, 30, 40, 50, 60, 70, 80],
    'ID': ['a', 'a', 'b', 'b', 'c', 'd', 'e', 'f']
})

summary_df = (
    df >>
    summarise(Total_Count=count())
)

from pyplyr import summarize



# Example usage
df = pd.DataFrame({
    'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
    'B': ['one', 'one', 'two', 'three', 'two', 'two', 'one', 'three'],
    'C': [1, 2, 3, 4, 5, 6, 7, 8],
    'D': [10, 20, 30, 40, 50, 60, 70, 80],
    'ID': ['a', 'a', 'b', 'b', 'c', 'd', 'e', 'f']
})

summary_df = (
    df >>
    summarize(Total_Count=count(), B_Count=count('B'))
)

print(summary_df)



