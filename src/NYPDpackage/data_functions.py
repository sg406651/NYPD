import numpy as np
import argparse
import pandas as pd


def parse_arguments():
    """
    parse file paths, the start and the end of analysing period
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("GPD", help="path to GPD file")
    parser.add_argument("POP", help="path to population data file")
    parser.add_argument("CO2", help="path to CO2 emission file")
    parser.add_argument("-start", type=int,
                        default=1960, help="start of the analyzing period")
    parser.add_argument("-end", type=int,
                        default=2014, help="end of the analyzing period")
    args = parser.parse_args()
    return args


def clean(df):
    """
    unify dataframes colum names and countries names, deletes empty columns
    """
    df = df.rename(columns={"Country Name": "Country"})
    df["Country"] = df["Country"].str.upper()
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    return df


def years(gpd, pop, co2):
    """
    take intersection of years in three dataframes if -start and -end parameters are not passed
    :return: list of years for forward analysis
    """
    gpd_years = np.array(gpd.columns.tolist())
    gpd_years = gpd_years[4:len(gpd_years)]
    gpd_years = gpd_years.astype(int)
    pop_years = np.array(pop.columns.tolist())
    pop_years = pop_years[4:len(pop_years)]
    pop_years = pop_years.astype(int)
    co2_years = co2["Year"].unique()
    year = np.intersect1d(pop_years, gpd_years)
    year = np.intersect1d(year, co2_years)
    return year


def consistent_format(df, statistics_name: str, interval):
    """
    :param df: name of the dataframe
    :param statistics_name:
    :param interval: list of years we perform analysis on
    """
    df_years = np.array(df.columns)
    df_years = df_years[4:len(df_years)]
    df = pd.melt(df, id_vars=["Country"], value_vars=df_years)
    df.columns = ["Country", "Year", statistics_name]
    df = df.astype({"Year": int})
    df = df[df["Year"].isin(interval)]
    return df


def merge(df1, df2):
    """
    :return: merged dataframe on "Country" and "Year" columns
    """
    df = pd.merge(df1, df2, how='inner', left_on=["Country", "Year"], right_on=["Country", "Year"])
    return df


def data_loss(gpd, pop, co2, merged_df):
    """
    print percentage of countries lost during merge
    """
    gpd_countries = list(gpd["Country"].unique())
    pop_countries = list(pop["Country"].unique())
    co2_countries = list(co2["Country"].unique())
    countries = gpd_countries + pop_countries + co2_countries
    countries = len(list(set(countries)))
    merged_df_countries = len(list(merged_df["Country"].unique()))
    loss = (countries - merged_df_countries) / countries
    print("\n \nLoss in data is equal to:", round(loss, 3), "%\n")


def save_to_xlsx(df, output_name: str):
    """
    :param df: dataframe to save
    :param output_name: output file name in .xlsx format
    :return:
    """
    with pd.ExcelWriter(output_name) as writer:
        df.to_excel(writer, sheet_name=output_name)


def max_emission(merged_df):
    """
    produce xlsx file with sorted top 5 emission per capita countries for each year
    """
    df_new = merged_df[["Year", "Country", "Per Capita", "Total"]]
    series = df_new.groupby("Year")["Per Capita"].nlargest(5).reset_index()
    index = series["level_1"]
    df_new = df_new.iloc[index]
    save_to_xlsx(df_new, "top_5_emission.xlsx")


def max_gpd(merged_df):
    """
    produce xlsx file with sorted top 5 emission GPD per capita for each year
    """
    df_new = merged_df[["Year", "Country", "GPD", "Total", "POP"]]
    df_new["GPD"] = df_new["GPD"].fillna(0)
    df_new["GPD Per Capita"] = df_new["GPD"].divide(df_new["POP"])
    series = df_new.groupby("Year")["GPD Per Capita"].nlargest(5).reset_index()
    index = series["level_1"]
    df_new = df_new.iloc[index]
    df_new = df_new.loc[:, df_new.columns != 'POP']
    df_new = df_new.loc[:, df_new.columns != 'Total']
    save_to_xlsx(df_new, "top_5_GPD.xlsx")


def emission_change(merged_df, interval):
    """
    prints countries with the biggest increase and decrease in co2 emission
    """
    if len(interval) >= 10:
        end_year = interval[-1]
        start_year = interval[-11]
    if len(interval) < 10:
        start_year = interval[0]
        end_year = interval[-1]
    if len(interval) == 1:
        print("Cannot print change in emission for such a short period")
        return 0
    df_new = merged_df[merged_df["Year"].isin([end_year, start_year])]
    negative_start = list(-df_new[df_new["Year"] == start_year]["Per Capita"])
    df_new.loc[df_new["Year"] == start_year, "Per Capita"] = negative_start
    biggest = df_new.groupby("Country")["Per Capita"].sum().nlargest(1).reset_index()
    smallest = df_new.groupby("Country")["Per Capita"].sum().nsmallest(1).reset_index()
    print("Country with the biggest increase in emission per Capita:\n", biggest.head(), "\n")
    print("Country with the biggest decrease in emission per Capita:\n", smallest.head())
