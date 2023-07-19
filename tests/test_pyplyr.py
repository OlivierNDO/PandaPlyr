### Configuration
###############################################################################
# Import packages
import unittest
import pandas as pd
import numpy as np

# Import modules
from src import pandaplyr as pp


### Define Functions and Classes
###############################################################################
class TestDataManipulation(unittest.TestCase):
    """
    A class for unit testing the data manipulation functions in the PyPlyr package.
    
    This class is a subclass of unittest.TestCase which provides a set of assertion methods useful
    for writing tests to make sure the code behaves as expected.
    """
    def setUp(self):
        """
        Special method called before each test.
        Sets up a DataFrame for use in testing the data manipulation functions.
        """
        # create a dataframe for testing
        self.df = pd.DataFrame({
            'A': [1, 2, 3, 4, 5],
            'B': ['a', 'a', 'b', 'b', 'c'],
            'C': [1, 1, 1, 2, 2]
        })

    def test_group_by(self):
        """
        Tests the group_by function.
        Checks if the function correctly groups the DataFrame by the specified column.
        """
        grouped_df = self.df >> pp.group_by('B')
        self.assertIsInstance(grouped_df, pd.core.groupby.DataFrameGroupBy)
        self.assertEqual(list(grouped_df.groups.keys()), ['a', 'b', 'c'])

    def test_summarise(self):
        """
        Tests the summarise function.
        Checks if the function correctly aggregates the grouped DataFrame using the specified aggregation functions.
        """
        summarised_df = self.df >> pp.group_by('B') >> pp.summarise({'A': 'sum', 'C': 'mean'})
        self.assertEqual(summarised_df['A'].tolist(), [3, 7, 5])
        self.assertEqual(summarised_df['C'].tolist(), [1, 1.5, 2])

    def test_mutate(self):
        """
        Tests the mutate function.
        Checks if the function correctly adds or modifies variables in the DataFrame.
        """
        mutated_df = (self.df >> 
                      pp.mutate(D = 'A * 2') >>
                      pp.mutate(A_X_C_PLUS_TWO = '(A * C) + 2')
            )
        self.assertEqual(mutated_df['D'].tolist(), [2, 4, 6, 8, 10])
        self.assertEqual(mutated_df['A_X_C_PLUS_TWO'].tolist(), [3, 4, 5, 10, 12])

    def test_where(self):
        """
        Tests the where function.
        Checks if the function correctly filters rows in the DataFrame based on the specified condition.
        """
        filtered_df = self.df >> pp.where('A > 2')
        self.assertEqual(filtered_df['A'].tolist(), [3, 4, 5])

    def test_select(self):
        """
        Tests the select function.
        Checks if the function correctly selects specified columns from the DataFrame.
        """
        selected_df = self.df >> pp.select('A', 'B')
        self.assertListEqual(list(selected_df.columns), ['A', 'B'])

    def test_rename(self):
        """
        Tests the rename function.
        Checks if the function correctly renames specified columns in the DataFrame.
        """
        renamed_df = self.df >> pp.rename(D='A')
        self.assertListEqual(sorted(list(renamed_df.columns)), ['B', 'C', 'D'])

    def test_arrange(self):
        """
        Tests the arrange function.
        Checks if the function correctly sorts the DataFrame by the specified column.
        """
        arranged_df = self.df >> pp.arrange('A', ascending=False)
        self.assertEqual(arranged_df['A'].tolist(), [5, 4, 3, 2, 1])


if __name__ == '__main__':
    unittest.main()







