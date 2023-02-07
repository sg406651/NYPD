Repository contains final project for NYPD in 2023.

It contains data from:

https://data.worldbank.org/indicator/NY.GDP.MKTP.CD

https://data.worldbank.org/indicator/SP.POP.TOTL

https://datahub.io/core/co2-fossil-by-nation

Available package has run_analysis.py script that runs analysis for the data in this format for a given period.
It gives three xlsx files as an output:
- merged_data.xlsx - contains merged data from those 3 sources
- top_5_GPD.xlsx - contains dataframe with 5 countries having the highest GPD per capita for each year
- top_5_emission.xlsx - contains datagrame with 5 countries having highest emission per capita for each year

It also prints country with the biggest decrease and increase in emission in last 10 years.


