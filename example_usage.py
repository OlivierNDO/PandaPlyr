### Configuration
###############################################################################
# Import packages
import numpy as np
import pandas as pd
import re

# Import modules
import src.pyplyr as pp

"""
I have two dataframes - grade_df and subject_df.

Merge the dataframes and find the student with
the highest average grade for Humanities classes only,
but exclude any students ('StudentID') who are not
enrolled in at least 2 humanities courses.

Do this in pandas in as few lines as possible.


grade_df.head()
   StudentID     Subject  Grade
0          1     CompSci     80
1          1     English     85
2          1     History     75
3          1   LinearAlg     75
4          1  Philosophy     85


subject_df.head()




      Subject SubjectType
0     CompSci        STEM
1   LinearAlg        STEM
2  Philosophy  Humanities
3     English  Humanities
4     History  Humanities


   StudentID     Subject  Grade
0          1     CompSci     80
1          1     English     85
2          1     History     75
3          1   LinearAlg     75
4          1  Philosophy     85

"""






grade_df = pp.read_grades_dataset()
subject_df = pp.read_subject_dataset()


### PyPlyr
top_student_pyplyr = (
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



### Pandas
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



student_highest_avg_grade = avg_grades['StudentID'][avg_grades['AverageGrade'].idxmax()]
student_details = grade_df.loc[grade_df['StudentID'] == student_highest_avg_grade]

print(student_details)



agg_df.head()

>>
pp.where('AverageGrade == max(AverageGrade)')

grade_df = grade_df.loc[(grade_df['StudentID'] != 3) | (grade_df['Subject'].isin(['CompSci', 'LinearAlg', 'English']))]

grade_df.to_csv('D:/PyPlyr/data/student_grades.csv', index = False)


df = pd.DataFrame({
    'StudentID': [1, 2, 3, 4, 5],
    'SubjectA': [80, 70, 90, 85, 75],
    'SubjectB': [75, 65, 85, 80, 70],
    'SubjectC': [85, 75, 95, 90, 80]
})




df = pd.DataFrame({
    'StudentID': [1, 2, 3, 4, 5],
    'SubjectA': [80, 70, 90, 85, 75],
    'SubjectB': [75, 65, 85, 80, 70],
    'SubjectC': [85, 75, 95, 90, 80]
})

df = pd.DataFrame({
    'StudentID': [1, 2, 3, 4, 5],
    'CompSci': [80, 70, 90, 85, 75],
    'LinearAlg': [75, 65, 85, 80, 70],
    'Philosophy': [85, 75, 95, 90, 80],
    'English': [85, 75, 95, 90, 80],
    'History': [75, 72, 82, 81, 60]
})

df = df.melt(id_vars='StudentID', var_name='Subject', value_name='Grade').sort_values(['StudentID', 'Subject'])



sub_df = pd.DataFrame({'Subject' : ['CompSci', 'LinearAlg', 'Philosophy', 'English', 'History'],
                       'SubjectType' : ['STEM', 'STEM', 'Humanities', 'Humanities', 'Humanities']})



df.to_csv('D:/PyPlyr/data/student_grades.csv', index = False)

sub_df.to_csv('D:/PyPlyr/data/subject_categories.csv', index = False)


df['avg_grade'] = df.groupby('StudentID')['Grade'].transform('mean')
df['grade_category'] = np.where(df['avg_grade'] >= 80, 'Excellent', 'Average')




'D:/PyPlyr/data/'













toy_df = pp.read_titanic_dataset()

toy_df.head()


df = (
    toy_df >>
    pp.mutate(age_group = 'np.where(age < 18, "Child", "Adult")') >> 
    pp.group_by('age_group') >> 
    pp.summarise(n_passengers = ('age_group', 'count'),
                 n_survivors = ('survived', 'sum')) >>
    pp.mutate(percent_survivors = 'n_survivors / n_passengers')
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



