### Configuration
###############################################################################
# Import packages
import os
import pandas as pd


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
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_path = current_file_path.split('PandaPlyr')[0] + 'PandaPlyr/data/titanic.csv'
    return pd.read_csv(file_path)

def read_grades_dataset():
    """
    Read the Titanic dataset from the CSV file into a pandas Dataframe

    Returns:
    -------
    pandas.DataFrame:
        The loaded Titanic dataset.
    """
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_path = current_file_path.split('PandaPlyr')[0] + 'PandaPlyr/data/student_grades.csv'
    return pd.read_csv(file_path)

def read_subject_dataset():
    """
    Read the Titanic dataset from the CSV file into a pandas Dataframe

    Returns:
    -------
    pandas.DataFrame:
        The loaded Titanic dataset.
    """
    current_file_path = os.path.dirname(os.path.realpath(__file__))
    file_path = current_file_path.split('PandaPlyr')[0] + 'PandaPlyr/data/subject_categories.csv'
    return pd.read_csv(file_path)