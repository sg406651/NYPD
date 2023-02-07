import numpy as np
import pandas as pd
import data_functions as f


# disable false positive warnings
pd.options.mode.chained_assignment = None
# get arguments from parser
args = f.parse_arguments()
# get dataframes from argparse paths
GPD = pd.read_csv(args.GPD, skiprows=4)
POP = pd.read_csv(args.POP, skiprows=4)
CO2 = pd.read_csv(args.CO2)
# clean GDP and POP dataframes
GPD = f.clean(GPD)
POP = f.clean(POP)

# set interval
if args.start > args.end:
    args.start, args.end = args.end, args.start
    print("start parameter > end parameter, switched parameters' values")


interval = list(range(args.start, args.end+1))
interval2 = f.years(GPD, POP, CO2)
interval = np.intersect1d(interval, interval2)

# change dataframes into consistent format and merge them
GPD = f.consistent_format(GPD, "GPD", interval)
POP = f.consistent_format(POP, "POP", interval)
CO2 = CO2[CO2["Year"].isin(interval)]
merged_df = f.merge(GPD, POP)
merged_df = f.merge(merged_df, CO2)

f.data_loss(GPD, POP, CO2, merged_df)

# create xlsx files with merged data, GPD per capita and max emission
f.save_to_xlsx(merged_df, "merged_data.xlsx")
f.max_emission(merged_df)
f.max_gpd(merged_df)

# print in console countries with the biggest increase and decrease in emission
f.emission_change(merged_df, interval)
