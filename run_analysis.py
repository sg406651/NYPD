# data analysis script
import pandas as pd
import data_functions as f


# get arguments from parser
args = f.parse_arguments()
# get dataframes from argparse paths
GDP = pd.read_csv(args.GDP, skiprows=4)
POP = pd.read_csv(args.POP, skiprows=4)
CO2 = pd.read_csv(args.CO2)
# clean GDP P
GDP = f.clean(GDP)
POP = f.clean(POP)

interval = f.years(GDP, POP, CO2, args)

GDP = f.consistent_format(GDP, "GPD", interval)
POP = f.consistent_format(POP, "POP", interval)
CO2 = CO2[CO2["Year"].isin(interval)]

merged_df = f.merge(GDP, POP)
merged_df = f.merge(merged_df, CO2)
f.max_revenue(merged_df)
f.emission_change(merged_df, interval)


