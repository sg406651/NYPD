# data analysis script
import argparse
import configparser
import os
import pandas as pd

dir_name = os.path.dirname(__file__)
config = configparser.ConfigParser()
config.read(os.path.join(dir_name), "config.ini")

parser = argparse.ArgumentParser()
parser.add_argument("GDP", help="path to GDP file")
parser.add_argument("population_file", help="path to population data file")
parser.add_argument("CO2", help="path to CO2 emission file")

args = parser.parse_args()
print("GDP parser to: ", args.GDP)

#GDP = pd.read_csv(args.GDP)
#print(pd.GDP.head(5))
