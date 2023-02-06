import numpy as np
import argparse
import numpy as np
import pandas as pd


def parse_arguments():

    parser = argparse.ArgumentParser()
    parser.add_argument("GDP", help="path to GDP file")
    parser.add_argument("POP", help="path to population data file")
    parser.add_argument("CO2", help="path to CO2 emission file")
    parser.add_argument("--start", type=int,
                        default=None, help="start of the analyzing interval")
    parser.add_argument("--end", type=int,
                        default=None, help="end of the analyzing interval")
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


def consistent_format(df, statistics_name: str, interval):
    df_years = np.array(df.columns)
    df_years = df_years[4:len(df_years)]
    df = pd.melt(df, id_vars=["Country"], value_vars=df_years)
    df.columns = ["Country", "Year", statistics_name]
    df = df.astype({"Year": int})
    df = df[df["Year"].isin(interval)]
    return df


def merge(df1, df2):
    df = pd.merge(df1, df2, how='left', left_on=["Country", "Year"], right_on=["Country", "Year"])
    return df


def save_to_xlsx(df, output_name: str):
    with pd.ExcelWriter(output_name) as writer:
        df.to_excel(writer, sheet_name=output_name)


def max_emission(merged_df):
    df_new = merged_df[["Year", "Country", "Per Capita", "Total"]]
    df_to_xlsx = df_new.groupby("Year")["Per Capita"].nlargest(5)
    #save_to_xlsx(df_to_xlsx, "Emission.xlsx")
    return df_to_xlsx
