import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

df = pd.read_csv('data\Georgia_COVID-19_Case_Data.csv')

len(df)
df.shape


####### describing variables #####
df.info()
list(df) # column names

df['COUNTY'].value_counts() # count values
df_counties = df['COUNTY'].value_counts() # store in variable
df_counties.head(20)


###### transforming columns #####

df['DATESTAMP']
df['DATESTAMP_MOD'] = df['DATESTAMP'] # make a copy of the column
df['DATESTAMP_MOD'] = pd.to_datetime(df['DATESTAMP_MOD']) # change type to datetime
df['DATESTAMP_MOD'].dtypes
df[['DATESTAMP', 'DATESTAMP_MOD']] # view both columns

df['DATESTAMP_MOD_DATE'] = df['DATESTAMP_MOD'].dt.date # extracting just the date
df['DATESTAMP_MOD_DATE']

df['DATESTAMP_MOD_YEAR'] = df['DATESTAMP_MOD'].dt.year # extracting just the year
df['DATESTAMP_MOD_YEAR']
df['DATESTAMP_MOD_MONTH'] = df['DATESTAMP_MOD'].dt.month # extracting just the month
df['DATESTAMP_MOD_MONTH']
df['DATESTAMP_MOD_WEEK'] = df['DATESTAMP_MOD'].dt.week # extracting just the week
df['DATESTAMP_MOD_WEEK']
df['DATESTAMP_MOD_DAY'] = df['DATESTAMP_MOD'].dt.day # extracting just the week
df['DATESTAMP_MOD_DAY']

df['DATESTAMP_MOD_MONTH_YEAR'] = df['DATESTAMP_MOD'].dt.to_period('M') # extracting month and year
df['DATESTAMP_MOD_MONTH_YEAR'].sort_values()

df['DATESTAMP_MOD_QUARTER'] = df['DATESTAMP_MOD'].dt.to_period('Q') # change datetime to year and quarter
df['DATESTAMP_MOD_QUARTER']

# change to strings
df['DATESTAMP_MOD_DAY_STRING'] = df['DATESTAMP_MOD_DAY'].astype(str)
df['DATESTAMP_MOD_WEEK_STRING'] = df['DATESTAMP_MOD_WEEK'].astype(str)