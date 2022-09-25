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
df['DATESTAMP_MOD'].dtypes # view column types
df[['DATESTAMP', 'DATESTAMP_MOD']] # view both columns

df['DATESTAMP_MOD_DATE'] = df['DATESTAMP_MOD'].dt.date # extracting just the date
df['DATESTAMP_MOD_DATE']

df['DATESTAMP_MOD_YEAR'] = df['DATESTAMP_MOD'].dt.year # extracting just the year
df['DATESTAMP_MOD_YEAR']
df['DATESTAMP_MOD_MONTH'] = df['DATESTAMP_MOD'].dt.month # extracting just the month
df['DATESTAMP_MOD_MONTH']
df['DATESTAMP_MOD_WEEK'] = df['DATESTAMP_MOD'].dt.week # extracting just the week
df['DATESTAMP_MOD_WEEK']
df['DATESTAMP_MOD_DAY'] = df['DATESTAMP_MOD'].dt.day # extracting just the day
df['DATESTAMP_MOD_DAY']

df['DATESTAMP_MOD_MONTH_YEAR'] = df['DATESTAMP_MOD'].dt.to_period('M') # extracting month and year
df['DATESTAMP_MOD_MONTH_YEAR'].sort_values()

df['DATESTAMP_MOD_QUARTER'] = df['DATESTAMP_MOD'].dt.to_period('Q') # change datetime to year and quarter
df['DATESTAMP_MOD_QUARTER']

# change column type to strings + make new column
df['DATESTAMP_MOD_DAY_STRING'] = df['DATESTAMP_MOD_DAY'].astype(str)
df['DATESTAMP_MOD_WEEK_STRING'] = df['DATESTAMP_MOD_WEEK'].astype(str)
df['DATETIME_STRING'] = df['DATESTAMP_MOD_MONTH_YEAR'].astype(str)



###### filtering out data ######

# counties we want to analyze: Cobb, DeKalb, Fulton, Gwinnett, Hall
countList =['COBB', 'DEKALB', 'FULTON', 'GWINNETT', 'HALL' ]

# filter df based on counties of interest
selectCounties = df[df['COUNTY'].isin(countList)]
len(selectCounties)

# filter df based on time of interest
selectCountyTime = selectCounties # make a copy so we don't override

# select rows from april and may 2020. choose both via |. put parenthesis around ecach month
selectCountyTime_aprilmay2020 = selectCountyTime[(selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-04') | (selectCountyTime['DATESTAMP_MOD_MONTH_YEAR'] == '2020-05')]
len(selectCountyTime_aprilmay2020)
selectCountyTime_aprilmay2020.head(50)


# filter by the columns that you want
finaldf = selectCountyTime_aprilmay2020[['COUNTY', 
                                        'DATESTAMP_MOD', 
                                        'DATESTAMP_MOD_DATE',
                                        'DATESTAMP_MOD_DAY_STRING',
                                        'DATESTAMP_MOD_MONTH_YEAR', 
                                        'DATETIME_STRING',
                                        'C_New', #new cases
                                        'C_Cum', #cumulative cases
                                        'H_New', #new hospitalizations
                                        'H_Cum', #cumulative hospitalizations
                                        'D_New',
                                        'D_Cum'  #total deaths
                                        ]]




###### visualizing data ######

### look at total covid cases by month ###

# drop duplicate rows because we only want cumulative at the end of the month
finaldf_dropdups = finaldf.drop_duplicates(subset = ['COUNTY', 'DATETIME_STRING'], keep='last')
finaldf_dropdups

# create pivot table to see data 
pd.pivot_table(finaldf_dropdups, values = 'C_Cum', index = ['COUNTY'], 
                columns = ['DATESTAMP_MOD_MONTH_YEAR'], aggfunc=np.sum)



# create barplot to visualize using seaborn
vis1 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', data=finaldf_dropdups)
plt.show()

# create barplot but add county
vis2 = sns.barplot(x='DATESTAMP_MOD_MONTH_YEAR', y='C_Cum', hue ='COUNTY', data=finaldf_dropdups)
plt.show()

# create same barplot but using plotly 
plotly1 = px.bar(finaldf_dropdups, x='DATETIME_STRING', y='C_Cum', color='COUNTY', barmode='group') #barmode = group, overlay, stack
plotly1.show()


### total covid cases by date ###

daily = finaldf
len(daily)

# create pivot table
pd.pivot_table(daily, values = 'C_Cum', index = ['COUNTY'], 
                columns = ['DATESTAMP_MOD_DATE'], aggfunc=np.sum)

# switch index and value and the column and row headers switch
pd.pivot_table(daily, values = 'C_Cum', index = ['DATESTAMP_MOD_DATE'], 
                columns = ['COUNTY'], aggfunc=np.sum)


# filter only the dates that are wanted
startdate = pd.to_datetime('2020-04-26').date()
enddate = pd.to_datetime('2020-05-09').date()

maskFilter = (daily['DATESTAMP_MOD_DATE'] >= startdate) & (daily['DATESTAMP_MOD_DATE'] <= enddate)
dailyspecific = daily.loc[maskFilter]
print(dailyspecific)



##### creating graphs with the desired data #####

# create line plot with seaborn
vis3 = sns.lineplot(data=dailyspecific, x='DATESTAMP_MOD_DATE', y='C_Cum')
plt.show()

# add counties
vis3 = sns.lineplot(data=dailyspecific, x='DATESTAMP_MOD_DATE', y='C_Cum', hue = 'COUNTY')
plt.show()

# create bar plot with plotly
plotly2 = px.bar(dailyspecific, x='DATESTAMP_MOD_DATE', y='C_Cum', color='COUNTY')
plotly2.show()

# look at another variable- H_New
plotly3 = px.bar(dailyspecific, x='DATESTAMP_MOD_DATE', y='H_New', color='COUNTY', barmode = 'group')
plotly3.show()

# look at another variable- H_Cum
plotly4 = px.bar(dailyspecific, x='DATESTAMP_MOD_DATE', y='H_Cum', color='COUNTY', barmode = 'group')
plotly4.show()

# look at another variable- D_New
plotly5 = px.bar(dailyspecific, x='DATESTAMP_MOD_DATE', y='D_New', color='COUNTY', barmode = 'group')
plotly5.show()

# look at another variable- D_Cum
plotly6 = px.bar(dailyspecific, x='DATESTAMP_MOD_DATE', y='D_Cum', color='COUNTY', barmode = 'group')
plotly6.show()



#### recreating graph ####

# the actual graph looks like it is H and D and C data so we are going to combine those into a new column
dailyspecific['newHandDandC'] = dailyspecific['H_New'].astype(int) + dailyspecific['D_New'].astype(int) + dailyspecific['C_New'].astype(int)
dailyspecific

# create a bar plot 
plotly7 = px.bar(dailyspecific, x='DATESTAMP_MOD_DATE', y='newHandDandC', color='COUNTY',
title= 'Georgia 2020 COVID Data: Total New Hospitalizations, Deaths, and Cases by County', 
labels= {"DATESTAMP_MOD_DATE" : "Date: Month, Day, Year", "newHandDandC" : "Total Count"}, 
barmode = 'group')

# can update axis labels using update_layout
plotly7.update_layout(
    xaxis = dict (
        tickmode = 'linear',
        type='category'
    )
)

plotly7.show()



