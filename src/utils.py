### Configuration
###############################################################################
# Import packages
import pandas as pd
import pkg_resources


### Define Classes & Functions
###############################################################################
def read_titanic_dataset():
    """
    Read the Titanic dataset from the CSV file into a pandas Dataframe

    Returns:
    -------
    pandas.DataFrame:
        The loaded Titanic dataset.
    """
    data_path = pkg_resources.resource_filename('PandaPlyr', 'data/titanic.csv')
    return pd.read_csv(data_path)

def read_grades_dataset():
    """
    Read the Grades dataset from the CSV file into a pandas Dataframe

    Returns:
    -------
    pandas.DataFrame:
        The loaded Grades dataset.
    """
    data_path = pkg_resources.resource_filename('PandaPlyr', 'data/student_grades.csv')
    return pd.read_csv(data_path)

def read_subject_dataset():
    """
    Read the Subject dataset from the CSV file into a pandas Dataframe

    Returns:
    -------
    pandas.DataFrame:
        The loaded Subject dataset.
    """
    data_path = pkg_resources.resource_filename('PandaPlyr', 'data/subject_categories.csv')
    return pd.read_csv(data_path)
