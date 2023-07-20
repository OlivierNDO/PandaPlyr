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
        
        # Create another dataframe for testing join and union functions
        self.df2 = pd.DataFrame({
            'B': ['a', 'b', 'd'],
            'D': [10, 20, 30],
            'E': [1, 1, 1]
        })

    def test_arrange(self):
        """
        Tests the arrange function.
        Checks if the function correctly sorts the DataFrame by the specified column.
        """
        arranged_df = self.df >> pp.arrange('A', ascending=False)
        self.assertEqual(arranged_df['A'].tolist(), [5, 4, 3, 2, 1])
        
    def test_distinct(self):
        """
        Tests the distinct function.
        Checks if the function correctly selects distinct rows based on the specified columns.
        """
        distinct_df = self.df >> pp.distinct('B')
        self.assertEqual(distinct_df['B'].tolist(), ['a', 'b', 'c'])
        
    def test_drop_na(self):
        """
        Tests the drop_na function.
        Checks if the function correctly drops rows with NaN values in the specified columns.
        """
        df_with_na = self.df.copy()
        df_with_na.loc[1, 'A'] = np.nan
        dropped_df = df_with_na >> pp.drop_na('A')
        self.assertEqual(dropped_df['A'].tolist(), [1, 3, 4, 5])
        
    def test_fill_na(self):
        """
        Tests the fill_na function.
        Checks if the function correctly replaces NaN values in the specified column with a given value.
        """
        df_with_na = self.df.copy()
        df_with_na.loc[1, 'A'] = np.nan
        filled_df = df_with_na >> pp.fill_na('A', value=99)
        self.assertEqual(filled_df['A'].tolist(), [1, 99, 3, 4, 5])
        
    def test_full_join(self):
        """
        Tests the full_join function.
        Checks if the function correctly performs a full join on the specified column.
        """
        joined_df = self.df >> pp.full_join(self.df2, on='B')
        self.assertEqual(sorted(joined_df['B'].tolist()), ['a', 'a', 'b', 'b', 'c', 'd'])

    def test_group_by(self):
        """
        Tests the group_by function.
        Checks if the function correctly groups the DataFrame by the specified column.
        """
        grouped_df = self.df >> pp.group_by('B')
        self.assertIsInstance(grouped_df, pd.core.groupby.DataFrameGroupBy)
        self.assertEqual(list(grouped_df.groups.keys()), ['a', 'b', 'c'])
        
    def test_inner_join(self):
        """
        Tests the inner_join function.
        Checks if the function correctly performs an inner join on the specified column.
        """
        joined_df = self.df >> pp.inner_join(self.df2, on='B')
        self.assertEqual(joined_df['B'].tolist(), ['a', 'a', 'b', 'b'])
        
    def test_left_join(self):
        """
        Tests the left_join function.
        Checks if the function correctly performs a left join on the specified column.
        """
        joined_df = self.df >> pp.left_join(self.df2, on='B', fill_na = 0)
        self.assertEqual(joined_df['D'].tolist(), [10, 10, 20, 20, 0])

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
        
    def test_rename(self):
        """
        Tests the rename function.
        Checks if the function correctly renames specified columns in the DataFrame.
        """
        renamed_df = self.df >> pp.rename(D='A')
        self.assertListEqual(sorted(list(renamed_df.columns)), ['B', 'C', 'D'])
        
    def test_right_join(self):
        """
        Tests the right_join function.
        Checks if the function correctly performs a right join on the specified column.
        """
        joined_df = self.df >> pp.right_join(self.df2, on='B')
        self.assertEqual(joined_df['B'].tolist(), ['a', 'a', 'b', 'b', 'd'])

    def test_select(self):
        """
        Tests the select function.
        Checks if the function correctly selects specified columns from the DataFrame.
        """
        selected_df = self.df >> pp.select('A', 'B')
        self.assertListEqual(list(selected_df.columns), ['A', 'B'])
        
    def test_summarise(self):
        """
        Tests the summarise function.
        Checks if the function correctly aggregates the grouped DataFrame using the specified aggregation functions.
        """
        summarised_df = self.df >> pp.group_by('B') >> pp.summarise({'A': 'sum', 'C': 'mean'})
        self.assertEqual(summarised_df['A'].tolist(), [3, 7, 5])
        self.assertEqual(summarised_df['C'].tolist(), [1, 1.5, 2])
        
    def test_union(self):
        """
        Tests the union function.
        Checks if the function correctly performs a union operation between two dataframes.
        """
        union_df = self.df >> pp.union(self.df2)
        self.assertEqual(len(union_df), len(self.df) + len(self.df2))

    def test_union_all(self):
        """
        Tests the union_all function.
        Checks if the function correctly performs a union all operation between two dataframes.
        """
        union_all_df = self.df >> pp.union_all(self.df2)
        self.assertEqual(len(union_all_df), len(self.df) + len(self.df2))
        
    def test_where(self):
        """
        Tests the where function.
        Checks if the function correctly filters rows in the DataFrame based on the specified condition.
        """
        filtered_df = self.df >> pp.where('A > 2')
        self.assertEqual(filtered_df['A'].tolist(), [3, 4, 5])
        

    


if __name__ == '__main__':
    unittest.main()







