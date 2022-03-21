## Libraries

# Installing the libraries
# !pip install pandas
# !pip install numpy
# !pip install matplotlib
# !pip install seaborn
# !pip install pandas

# importing the libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import math

## Read and view data

# importing dataset
data = pd.read_csv('crimes_against_women_2001-2014.csv')
# view the dataset
# data

# dropping the unorganised index column
data.drop(['Unnamed: 0'], axis=1, inplace=True)
# data

# overview of data
print(data.info())

# data statistics
print(data.describe())

## Clean data

# unique state names
print(data['STATE/UT'].unique())
print(len(data['STATE/UT'].unique()))

# we see some repeat names and hence we need to fix that
# first we change the names that have a space missing or some extra characters
data.replace({'A&N Islands':'A & N Islands','D&N Haveli':'D & N HAVELI','Delhi UT':'DELHI'},inplace=True)
# next we make the case consistent
data['STATE/UT'] = data['STATE/UT'].str.title()
print(data['STATE/UT'].unique())
print(len(data['STATE/UT'].unique()))

# District column has a field called total which sums up the value for all districts
# in that particular state. This needs to be removed in order to prevent double counting
data["DISTRICT"]=data["DISTRICT"].str.lower()
data.drop(list(data[data["DISTRICT"]=="total"].index), inplace=True)
data.drop(list(data[data["DISTRICT"]=="zz total"].index), inplace=True)
data.drop(list(data[data["DISTRICT"]=="total district(s)"].index), inplace=True)
data.drop(list(data[data["DISTRICT"]=="delhi ut total"].index), inplace=True)

# sum of crimes
data["Total"] = data["Rape"] + data["Kidnapping and Abduction"] + data["Dowry Deaths"]+ data["Assault on women with intent to outrage her modesty"] + data["Insult to modesty of Women"]+ data["Cruelty by Husband or his Relatives"] + data["Importation of Girls"]

## View cleaned data

print(data)

# overview of data
print(data.info())

# overview of data
print(data.describe())

# as we can see we have the correct statistics now after removing overcounting

## Visualisations

# plotting crimes committed in each year for various types of crimes
plt.figure(figsize=(10,8))
plt.plot(data.groupby("Year")["Rape"].sum())
plt.plot(data.groupby("Year")["Kidnapping and Abduction"].sum())
plt.plot(data.groupby("Year")["Dowry Deaths"].sum())
plt.plot(data.groupby("Year")["Assault on women with intent to outrage her modesty"].sum())
plt.plot(data.groupby("Year")["Insult to modesty of Women"].sum())
plt.plot(data.groupby("Year")["Cruelty by Husband or his Relatives"].sum())
plt.plot(data.groupby("Year")["Importation of Girls"].sum())
plt.grid()
plt.title('Crimes over the years')
plt.xlabel('Year')
plt.ylabel('Number of Crimes')
plt.legend(["Rape","Kidnapping and Abduction","Dowry Deaths","Assault on women with intent to outrage her modesty",
            "Insult to modesty of Women","Cruelty by Husband or his Relatives","Importation of Girls"])
plt.show()

# total crimes committed in each state over all years
print("Total Crimes till date: " + str(data.groupby("STATE/UT")["Total"].sum().sum()))
plt.figure(figsize=(16,8))
data.groupby("STATE/UT")["Total"].sum().sort_values(ascending=False).plot.bar()
plt.grid()
plt.title('Total crimes in each state till date')
plt.xlabel('STATE/UT')
plt.ylabel('Number of Crimes')
plt.show()

# top7_df

# top 7 states in terms of total crimes
top7 = data.groupby("STATE/UT")["Total"].sum().sort_values(ascending=False).index[0:7]
top7_df = data[data["STATE/UT"].isin(top7)].drop('Total', axis=1).reset_index(drop=True)
top7_df = top7_df.groupby("STATE/UT").sum().reset_index()

top7_df.drop('Year', axis=1).plot(kind='barh', stacked=True, figsize= (16,8), x = "STATE/UT")
plt.grid()
plt.legend(loc = 4)
plt.show()

colors = ['maroon','red','black','saddlebrown','orange','gold','olive','green','cyan','teal','navy','purple','deeppink','slategray']
plot_data = data.groupby("Year").sum()
plt.figure(figsize=(15,6))
for i in range(len(data['Year'].unique())):
    plt.plot(plot_data.iloc[i,:-1], color=colors[i])
plt.xticks(rotation=90)
plt.title('Type of crime distribution for every year')
plt.xlabel('Type of Crime')
plt.ylabel('Number of Crimes')
plt.legend(['2001','2002','2003','2004','2005','2006','2007','2008','2009','2010','2011','2012','2013','2014'])
plt.grid()
plt.show()

# sum of crimes till date for each category of crime
type_sum = plot_data.sum().to_list()[0:-1]
crime_types = plot_data.sum().index.to_list()[0:-1]
# total crimes till date distribution based on type of crime
plt.figure(figsize=(15,6))
plt.pie(type_sum, labels=crime_types, autopct='%1.1f%%', startangle=90)
plt.title('Type of crime distribution for all total crimes till date')
plt.show()

# total crimes in each year distribution
years = plot_data.sum(axis=1).index.to_list()
year_total = plot_data.sum(axis=1).to_list()
plt.figure(figsize=(15,6))
plt.pie(year_total, labels=years, autopct='%1.1f%%', startangle=90)
plt.title('Total crimes distribution in each year')
plt.show()

for i in range(len(crime_types)):
    # total crimes for each type in each state over all years
    print("Total " + crime_types[i] + " crimes till date: " + str(type_sum[i]))
    plt.figure(figsize=(16,32))
    plt.subplot(7,1,i+1)
    data.groupby("STATE/UT")[crime_types[i]].sum().sort_values(ascending=False).plot.bar()
    plt.grid()
    plt.title('Total ' + crime_types[i] + ' crimes in each state for all years')
    plt.xlabel('STATE/UT')
    plt.ylabel('Number')
plt.show()

