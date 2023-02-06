# data analysis script
import pandas as pd
import data_functions as f
import numpy as np

args = f.parse_arguments()

GDP = pd.read_csv(args.GDP, skiprows=4)
POP = pd.read_csv(args.POP, skiprows=4)
CO2 = pd.read_csv(args.CO2)

GDP = f.clean(GDP)
POP = f.clean(POP)

interval = f.years(GDP, POP, CO2)
GDP = f.consistent_format(GDP, "GPD", interval)
POP = f.consistent_format(POP, "POP", interval)
CO2 = CO2[CO2["Year"].isin(interval)]

merged_df = f.merge(GDP, POP)
merged_df = f.merge(CO2, merged_df)
#f.save_to_xlsx(df, "merged_data.xlsx")
print(f.max_emission(merged_df))

