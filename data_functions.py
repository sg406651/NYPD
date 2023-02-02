import numpy as np
import argparse


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("GDP", help="path to GDP file")
    parser.add_argument("POP", help="path to population data file")
    parser.add_argument("CO2", help="path to CO2 emission file")
    args = parser.parse_args()
    return args


def clean(df):
    df = df.rename(columns={"Country Name": "Country"})
    df["Country"] = df["Country"].str.upper()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def years(gdp, pop, co2):
    gdp_years = np.array(gdp.columns.tolist())
    gdp_years = gdp_years[4:len(gdp_years)]
    gdp_years = gdp_years.astype(int)
    pop_years = np.array(pop.columns.tolist())
    pop_years = pop_years[4:len(pop_years)]
    pop_years = pop_years.astype(int)
    co2_years = co2["Year"].unique()
    year = np.intersect1d(pop_years, gdp_years)
    year = np.intersect1d(year, co2_years)

    return year




