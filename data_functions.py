import numpy as np
import argparse
import pandas as pd


def parse_arguments():
    """
    parse file paths, the start and the end of analysing period
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("GDP", help="path to GDP file")
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


def years(gdp, pop, co2, args):
    """
    take intersection of years in three dataframes if -start and -end parameters are not passed
    :return: list of years for forward analysis
    """
    interval = list(range(args[3],args[4]))
    gdp_years = np.array(gdp.columns.tolist())
    gdp_years = gdp_years[4:len(gdp_years)]
    gdp_years = gdp_years.astype(int)
    pop_years = np.array(pop.columns.tolist())
    pop_years = pop_years[4:len(pop_years)]
    pop_years = pop_years.astype(int)
    co2_years = co2["Year"].unique()
    year = np.intersect1d(pop_years, gdp_years)
    year = np.intersect1d(year, co2_years)
    year = np.intersect1d(year,interval)
    return year


def consistent_format(df, statistics_name: str, interval: list):
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
    df = pd.merge(df1, df2, how='left', left_on=["Country", "Year"], right_on=["Country", "Year"])
    return df


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
    save_to_xlsx(df_new, "Emission.xlsx")


def max_revenue(merged_df):
    """
    produce xlsx file with sorted top 5 emission GPD per capita for each year
    """
    df_new = merged_df[["Year", "Country", "GPD", "Total", "POP"]]
    df_new["GPD"] = df_new["GPD"].fillna(0)
    df_new["GPD Per Capita"] = df_new["GPD"].divide(df_new["POP"])
    series = df_new.groupby("Year")["GPD Per Capita"].nlargest(5).reset_index()
    index = series["level_1"]
    df_new = df_new.iloc[index]
    save_to_xlsx(df_new, "Revenue.xlsx")


def emission_change(merged_df, interval):
    """
    prints countries with the biggest increase and decrease in co2 emission
    """
    if len(interval) >= 10:
        end_year = interval[-1]
        start_year = interval[-11]
        df_new = merged_df[merged_df["Year"].isin([end_year, start_year])]
        print(df_new[df_new["Year"] == start_year]["Per Capita"])
        df_new[df_new["Year"] == start_year]["Per Capita"] \
            = -df_new[df_new["Year"] == start_year]["Per Capita"]
        print(df_new[df_new["Year"] == start_year]["Per Capita"])
        biggest = df_new.groupby("Country")["Per Capita"].sum().nlargest(1)
        smallest = df_new.groupby("Country")["Per Capita"].sum().nsmallest(1)
        print(biggest)
        print(smallest)
    else:
        return "Interval length too short to give print 10 year emission change"
