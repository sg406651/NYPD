# data analysis script
import argparse
import numpy as np
import pandas as pd
import data_functions

args = parse_arguments()

GDP = pd.read_csv(args.GDP, skiprows=4)
POP = pd.read_csv(args.POP, skiprows=4)
CO2 = pd.read_csv(args.CO2)
