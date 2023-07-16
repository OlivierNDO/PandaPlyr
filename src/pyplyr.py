### Configuration
###############################################################################
# Import packages
import numpy as np
import pandas as pd
import re


### Define Classes & Functions
###############################################################################
class Pipe:
    """
    A class to enable functionality similar to R dplyr on pandas dataframes.
    Instead of the pipe operator in R %>%, this class uses >>.

    Parameters:
    -----------
    func : function
        The function to be executed in the pipeline.
    """
    def __init__(self, func):
        self.func = func

    def __call__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        return self

    def __rrshift__(self, other):
        return self.func(other, *self.args, **self.kwargs)


@Pipe
def group_by(df, *args, **kwargs):
    """
    Function to group a pandas DataFrame by one or more columns.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    *args : str or list
        The column(s) to group by.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the groupby function.

    Returns:
    --------
    pandas.DataFrameGroupBy
        The grouped DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'Z' : ['x', 'x', 'y', 'x', 'x', 'y'],
                       'B': [10, 20, 30, 40, 50, 60]})
    new_df = df >> group_by('A', 'Z') >> summarise(AVG_B = ('B', 'mean'))
    """
    kwargs.setdefault('as_index', False)
    if isinstance(args[0], list):
        group_columns = args[0]
    else:
        group_columns = list(args)
    return df.groupby(group_columns, **kwargs)


@Pipe
def summarise(df, *args, **kwargs):
    """
    Function to aggregate a pandas DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    *args : tuple
        The aggregation functions and columns to apply.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the aggregate function.

    Returns:
    --------
    pandas.DataFrame
        The aggregated DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'B': [10, 20, 30, 40, 50, 60]})
    new_df = df >> group_by('A') >> summarise(AVG_B = ('B', 'mean'))
    """
    return df.aggregate(*args, **kwargs)


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


@Pipe
def where(df, condition):
    """
    Function to filter rows of a pandas DataFrame based on a condition.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    condition : str
        The filtering condition.

    Returns:
    --------
    pandas.DataFrame
        The filtered DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'B': [10, 20, 30, 40, 50, 60],
                       'C': [1, 2, 3, 4, 5, 6]})
    new_df = df >> where('A == "foo" | C == 6')
    """
    return df.query(condition)


@Pipe
def select(df, *args):
    """
    Function to select specific columns from a pandas DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    *args : str
        The column names to select.

    Returns:
    --------
    pandas.DataFrame
        The DataFrame with selected columns.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'B': [10, 20, 30, 40, 50, 60],
                       'C': [1, 2, 3, 4, 5, 6]})

    new_df = df >> select('A', 'B')
    """
    return df.loc[:, list(args)]


@Pipe
def rename(df, **kwargs):
    """
    Function to rename columns in a pandas DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    **kwargs : dict
        The old and new column names.

    Returns:
    --------
    pandas.DataFrame
        The DataFrame with renamed columns.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'B': [10, 20, 30, 40, 50, 60],
                       'C': [1, 2, 3, 4, 5, 6]})

    new_df = df >> rename(Z = 'C')
    """
    df_copy = df.copy()
    for column, operation in kwargs.items():
        df_copy[column] = df_copy[operation]
        df_copy = df_copy.drop([operation], axis = 1)
    return df_copy



@Pipe
def arrange(df, column_name, order=None, ascending=None):
    """
    Function to sort a pandas DataFrame by a column. This function is synonymous with order_by().

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    column_name : str
        The column name to sort by.
    order : str, optional
        String indicating sort order - either "asc" or "desc". If not provided or invalid, ascending sort order is assumed.
    ascending : bool, optional
        Boolean indicating whether to sort in ascending order. If provided, this argument takes precedence over 'order'.

    Returns:
    --------
    pandas.DataFrame
        The sorted DataFrame.

    Raises:
    -------
    ValueError
        If 'order' is not either "asc" or "desc" or if 'ascending' is not a boolean.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                       'B': [10, 20, 30, 40, 50, 60]})
    new_df = df >> arrange('B', 'desc')
    """
    # If ascending argument provided, use it. Else, use order argument
    if ascending is None:
        if isinstance(order, str):
            if order.lower() == 'desc':
                ascending = False
            elif order.lower() == 'asc':
                ascending = True
            else:
                raise ValueError('Order should be either "asc" or "desc".')
        else:
            ascending = True  # Default behavior
    elif not isinstance(ascending, bool):
        raise ValueError('Ascending should be either True or False.')
    return df.sort_values(by=column_name, ascending=ascending)



order_by = arrange

@Pipe
def left_join(df1, df2, on=None, fill_na = None, **kwargs):
    """
    Function to perform a left join between two pandas DataFrames.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    on : str or list, optional
        The column(s) to join on.
    fill_na : dict, optional
        A dictionary where keys are column names in `df2` and values are the corresponding fill values.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the merge function.

    Returns:
    --------
    pandas.DataFrame
        The joined DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    df1 = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                        'B': [1, 2, 3, 4, 5, 6, 7, 8]})

    df2 = pd.DataFrame({'A': ['foo', 'bar', 'foo', 'bar', 'foo', 'bar', 'foo', 'foo'],
                        'C': [10, 20, 30, 40, 50, 60, 70, 80]})

    df3 = df1 >> left_join(df2, on = 'A')
    """
    merged_df = df1.merge(df2, how='left', left_on=on, right_on=on, **kwargs)
    return 



@Pipe
def left_join(df1, df2, on=None, fill_na=None, **kwargs):
    """
    Function to perform a left join between two pandas DataFrames.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    on : str or list, optional
        The column(s) to join on.
    fill_na : dict or any, optional
        A dictionary or a single value where keys are column names in `df2` and values are the corresponding fill values,
        or a single value to be applied to all columns in `df2` that are not present in `df1`.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the merge function.

    Returns:
    --------
    pandas.DataFrame
        The joined DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    # Default value of None for fill_na leaves np.nan values as is
    df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df2 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df3 = df1 >> left_join(df2, on = ['A'])

    # Using a single value for fill_na will replace values in all right dataframe columns the same way
    df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df2 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df3 = df1 >> left_join(df2, on = ['A'], fill_na = 0)

    # Using a dictionary for fill_na will use custom values for each right dataframe column
    df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df2 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df3 = df1 >> left_join(df2, on = ['A'], fill_na = {'C' : 0, 'D' : -999})
    """
    merged_df = df1.merge(df2, how='left', left_on=on, right_on=on, **kwargs)
    if fill_na is not None:
        if isinstance(fill_na, dict):
            for col, value in fill_na.items():
                if col not in df1.columns:
                    merged_df[col] = merged_df[col].fillna(value)
        else:
            merged_df = merged_df.fillna(fill_na)
    return merged_df



@Pipe
def inner_join(df1, df2, on=None, **kwargs):
    """
    Function to perform an inner join between two pandas DataFrames.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    on : str or list, optional
        The column(s) to join on.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the merge function.

    Returns:
    --------
    pandas.DataFrame
        The joined DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    df1 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df2 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df3 = df1 >> inner_join(df2, on = ['A'])
    """
    return df1.merge(df2, how='inner', on=on, **kwargs)


@Pipe
def right_join(df1, df2, on=None, fill_na=None, **kwargs):
    """
    Function to perform a right join between two pandas DataFrames.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    on : str or list, optional
        The column(s) to join on.
    fill_na : dict or any, optional
        A dictionary or a single value where keys are column names in `df1` and values are the corresponding fill values,
        or a single value to be applied to all columns in `df1` that are not present in `df2`.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the merge function.

    Returns:
    --------
    pandas.DataFrame
        The joined DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    # Default value of None for fill_na leaves np.nan values as is
    df1 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df2 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df3 = df1 >> right_join(df2, on = ['A'])
    
    # Using a single value for fill_na will replace values in all left dataframe columns the same way
    df1 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df2 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    
    df3 = df1 >> right_join(df2, on = ['A'], fill_na = 0)
    
    # Using a dictionary for fill_na will use custom values for each left dataframe column
    df1 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df2 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df3 = df1 >> right_join(df2, on = ['A'], fill_na = {'C' : 0, 'D' : -999})
    """
    merged_df = df1.merge(df2, how='right', left_on=on, right_on=on, **kwargs)

    if fill_na is not None:
        if isinstance(fill_na, dict):
            for col, value in fill_na.items():
                if col not in df2.columns:
                    merged_df[col] = merged_df[col].fillna(value)
        else:
            merged_df = merged_df.fillna(fill_na)

    return merged_df


@Pipe
def full_join(df1, df2, on=None, fill_na=None, **kwargs):
    """
    Function to perform a full join between two pandas DataFrames.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    on : str or list, optional
        The column(s) to join on.
    fill_na : dict or any, optional
        A dictionary or a single value where keys are column names in `df1` or `df2` (or both) and values are the corresponding fill values,
        or a single value to be applied to all columns in `df1` and `df2` that are not present in each other.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the merge function.

    Returns:
    --------
    pandas.DataFrame
        The joined DataFrame.

    Example Usage:
    --------------
    import pandas as pd
    # Default value of None for fill_na leaves np.nan values as is
    df1 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df2 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df3 = df1 >> full_join(df2, on = ['A'])
    
    # Using a single value for fill_na will replace values in columns unique to either dataframe the same way
    df1 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df2 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df3 = df1 >> full_join(df2, on = ['A'], fill_na = 0)
    
    # Using a dictionary for fill_na will use custom values for each column unique to one of the dataframes
    df1 = pd.DataFrame({'A': ['foo', 'bar'], 'C': [10, 20], 'D' : [25, 50]})
    df2 = pd.DataFrame({'A': ['foo', 'bar', 'other'], 'B': [1, 2, 3]})
    df3 = df1 >> full_join(df2, on = ['A'], fill_na = {'C' : 0, 'D' : -999})
    """

    merged_df = df1.merge(df2, how='outer', left_on=on, right_on=on, **kwargs)

    if fill_na is not None:
        if isinstance(fill_na, dict):
            for col, value in fill_na.items():
                if col not in df1.columns:
                    merged_df[col] = merged_df[col].fillna(value)
                if col not in df2.columns:
                    merged_df[col] = merged_df[col].fillna(value)
        else:
            merged_df = merged_df.fillna(fill_na)

    return merged_df


@Pipe
def union(df1, df2, **kwargs):
    """
    Function to concatenate two pandas DataFrames and remove duplicates.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the concat function.

    Returns:
    --------
    pandas.DataFrame
        The concatenated DataFrame with duplicates removed.

    Example Usage:
    --------------
    import pandas as pd
    df1 = pd.DataFrame({'A': [1, 1, 1], 'B': ['foo', 'bar', 'foo']})
    df2 = pd.DataFrame({'A': [2, 2, 2], 'B': ['foo', 'bar', 'bar']})
    df3 = df1 >> union(df2)
    """
    return pd.concat([df1, df2], **kwargs).drop_duplicates()


@Pipe
def union_all(df1, df2, **kwargs):
    """
    Function to concatenate two pandas DataFrames and without removing duplicates.

    Parameters:
    -----------
    df1 : pandas.DataFrame
        The first DataFrame.
    df2 : pandas.DataFrame
        The second DataFrame.
    **kwargs : dict, optional
        Additional keyword arguments to be passed to the concat function.

    Returns:
    --------
    pandas.DataFrame
        The concatenated DataFrame with duplicates removed.

    Example Usage:
    --------------
    import pandas as pd
    df1 = pd.DataFrame({'A': [1, 1, 1], 'B': ['foo', 'bar', 'foo']})
    df2 = pd.DataFrame({'A': [2, 2, 2], 'B': ['foo', 'bar', 'bar']})
    df3 = df1 >> union(df2)
    """
    return pd.concat([df1, df2], **kwargs)


@Pipe
def distinct(df, *args):
    """
    Function to remove duplicate rows from a pandas DataFrame.

    Parameters:
    -----------
    df : pandas.DataFrame
        The input DataFrame.
    *args : str, optional
        The column(s) to consider when checking for duplicates.

    Returns:
    --------
    pandas.DataFrame
        The DataFrame with duplicate rows removed.

    Example Usage:
    --------------
    import pandas as pd
    df = pd.DataFrame({'A': [2, 2, 2], 'B': ['foo', 'bar', 'bar']})
    new_df = df >> distinct()
    """
    if args:
        return df.drop_duplicates(subset=list(args))
    else:
        return df.drop_duplicates()


