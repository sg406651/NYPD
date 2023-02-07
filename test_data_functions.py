import pytest
import pandas as pd
from NYPD_package import data_functions as f


def test_clean():
    df1 = {"Country Name": ["Poland", "USA", "Mexico"], "Country Code": ["1", "2", "3"], "col3": ["1", "2", "3"],
           "col4": ["1", "2", "3"], "1960": [3, 4, 5], "1961": [4, 5, 6]}
    df1 = pd.DataFrame(df1)
    df1 = f.clean(df1)
    assert list(df1["Country"]) == ["POLAND", "USA", "MEXICO"]


def test_years():
    df1 = {"Country Name": ["Poland", "USA", "Mexico"], "Country Code": ["1", "2", "3"], "col3": ["1", "2", "3"],
           "col4": ["1", "2", "3"], "1960": [3, 4, 5], "1961": [4, 5, 6]}
    df2 = {"Country Name": ["Poland", "USA"], "Country Code": ["1", "2"], "col3": ["1", "2"],
           "col4": ["1", "2"], "1960": [3, 4], "1961": [4, 5], "1962": [7, 8]}
    df3 = {"Year": [1961, 1962], "Total": [2552, 2662]}
    df1 = pd.DataFrame(df1)
    df2 = pd.DataFrame(df2)
    df3 = pd.DataFrame(df3)
    assert f.years(df1, df2, df3) == [1961]


def test_merge():
    df1 = {"Country": ["Poland", "USA", "Mexico"], "Year": [1960, 1960, 1960], "POP": [1, 2, 3]}
    df2 = {"Country": ["Canada", "USA", "Mexico"], "Year": [1960, 1960, 1961], "GPD": [4, 5, 6]}
    df1 = pd.DataFrame(df1)
    df2 = pd.DataFrame(df2)
    df = f.merge(df1, df2)
    df3 = {"Country": "USA", "Year": [1960], "POP": [2], "GPD": [5]}
    df3 = pd.DataFrame(df3)
    assert df.equals(df3)
