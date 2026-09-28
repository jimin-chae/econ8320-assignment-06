# Lecture 6 Note
# Week 6 - Pandas, SQL
# Data Handling: What are the ways that we have learned so far to handle data?
# Lists of Lists, Dictionaries: Neither of these are particularly conducive to data explore and quick manipulation.
# Introducting Data Frames: When we want to manipulate data sets in a clean and efficient manner, 
# we want to start thinking about data in terms of tectors:
# Basically excel spreadsheet. We can have BIG DATA
# Each variable can be considered a vecotr
# Operations on a variable can be applied to all observation uniformly
# We can quicky reduce the number of variables for a 
# In Python, the pandas library contains the necessary code to begin working with Data Frames. It is dependent on many functions in the numpy library.
import pandas as pd # Import the library for us: pd = nickname for pandas
# Creating a Data Frame :
# data = pd.DataFrame()
# A Data Frame is a class that accepts the following parametrs:
# Data, Index(for referenceing individual rows), Columns, dtype, copy
data = pd.read_csv("https://github.com/dustywhite7/Econ8310/raw/master/DataSets/pollutionBeijing.csv")

#Referencing a Single Column
data['TEMP']
#dtype: float64
data['cbwd']
#dtype: object - means it's string

#To slice columns at once into a new Data Frame, pass a list of column names;
#using our slicing sintex
data[['datetime','TEMP']]
data[['TEMP','datetime']]

#Slicing the Data Frame
#data.iloc: Our whole data frame gets treated as a matrix with numeric references to both rows and columns, so we start off with row 0 go to row n-1. Start off with column 0 go to column n-1.
data.iloc[:5, :5] # not really useful we'd like to focus on loc

#***data.loc: we can provide integer-based selections, or choose to select all rows or columns, and only subset on a single dimension.
data.loc['TEMP','cbwd'] #data.loc[row_selection, column_selection]
data.loc[:, ['TEMP','cbwd']] #Selects all rows, one column
data.loc[:10, ['TEMP','cbwd']] #Selects 10 rows, one column

# With .loc, we can also provide logic-based selections, creating subsets based on conditions.
data.loc[data['Ir']>0, ['TEMP','datetime']] # Selects Ir >0 columns 'TEMP', 'datetime'
data.loc[(data['Ir']>0)&(data['TEMP']>20), ['TEMP','datetime']] # Selects Ir>0 AND temp >20, columns 'TEMP','datetime'


#------------
# Transforming our Data
# We can quickly transform the data in a given column using the slicing techniques from above:

data['TEMP_F'] = (9/5)*data['TEMP']+32 # Create new calculated column named 'TEMP_F'
data['PRECIP'] = data['Is']+data['Ir']
data['datetime'] = pd.to_datetime(data['datetime']) #Transforming data dtype: object -> datetime64[Ins]
data['datetime'].dt.day_name() # Gives us Monday-Sunday...etc
data['datetime'].dt.weekday # Any peice of information contained here 
data['datetime'].dt.year
data['datetime'].dt.month

# Cleaning Data (1. Filling missing data, 2.)

# Resolve missing values in ALL columns at once
data.fillna(0, inplace = True)
data.fillna(0)
# Resolve missing values in single column
# Few different Method for this.
# Method 'Pad' takes the last valid value, before our observation, and passes it forward to the current missing data. 
# Method 'Backfill' looks forward to the next valid piece of informatoion and brings it backwards.
# Depending on the data.
# data['Column'].fillna(method = 'pad')
data.fillna(method = 'backfill') # only seeing nothing changes

data = data.fillna(0) # USE 'data =' will update/save in memories!!!!!!!


#------------
# Map and Apply
# when we are working with pandas dataframe, oftentimes we want to define a function that does something and then be able to use that function across lots of different elements within our dataframe.
# map and apply allow us to do this.
# .map() is used with a single column., .apply() is used with all columns or all rows.

#Create new column
def snow(snowfall):
    if snowfall > 0:
        return "Snow Time!"
    else:
        return "No snow..."

data['snow'] = data['Is'].map(snow)
data['snow'].value_counts()

def snowboard(row):
    if (row['Is']>0 ) and (row['TEMP'] < 0):
        return "Go Time!"
    else:
        return "No time."

data.apply(snowboard)
#why are we getting error?

# To fix this put axis = 1
data.apply(snowboard, axis =1) # axis = 1 means we're gonna go by row by row rather than column by column through our dataset

data['snowboard'] = data.apply(snowboard, axis = 1)
data['snowboard'].value_counts()

# By using apply function we are getting every column in a single row exposed to us for our function
# so we can make a combination of responses based on all of these columns and then provide that information back to the user
# in this case we're using it to create new columns, we don't have to use it to create new columns 
# we can use it to create a flag that triggers an event so maybe we have information about temperature and movement on motion sensors, and then trigger lights on the room...,

#apply function allow us to apply a function across the entire row for every row in our data set

data.applymap # element by element across all rows across all columns, every single cell on its own

#Generating Summary Statistics
data.describe
# Every data frame is behind the sceneses a matrix
# We can transpose this, so that we can get variables on the rows rather than variables on the column
data.describe().T
# 
data.describe().T[['count','mean','std','min','max']]
summary = data.describe().T[['count','mean','std','min','max']]
# summary dataframe, there is whole different options to export this data to store this information
dir(summary)

summary.to_html()

summary.to_latex()

summary.to_csv("summary.csv") # to save this csv file

# use python and do power lifting and hand csv to our boss




#------------
# Using SQL with Python 
# In order to handle data on a large scale, we frequently rely on SQL databases. In this class, we can practice with MySQL.
# Install MySQL connectors with the following comand
# pip install sqlalchemy mysql-connector-python
#from sqlalchemy import create_engine
#engineStr = 'mysql+mysqlconnector://viewer:'
#engineStr = 'mysql+mysqlconnnector://*username*:*password*'
 

from sqlalchemy import create_engine
# SQL flavor, user, password
engineStr = 'mysql+mysqlconnector://*username*:*password*'
engineStr += '@35.202.92.40:3306' # Server Address
engineStr += '/nfl' # Database Name
engine = create_engine(engineStr) # Start the Engine

import pandas as pd

SELECT = "SELECT * FROM game LIMIT 10"

data = pd.read_sql(SELECT,engine)

# Retrieve SQL Data with Pandas
# Our next step is to wrtie a SELECT statement using SQL, and then to pass it to Pandas for retrieval.


# antoher way to integrate with python and SQL.
# We can use SQL to clean our data
# pandasql library

# pip install pandasql

#from pandasql import sqldf
pysqldf = lambda q: sqldf (q,globals())
# it updates it to give sqldf access everything in memory
# so we can use SQL statements to manipulate data frames

import pandas as pd
data = pd.read_csv("https://github.com/dustywhite7/Econ8310/raw/master/DataSets/pollutionBeijing.csv")
from pandasql import sqldf
pysqldf = lambda q: sqldf(q, globals())

pysqldf("SELECT * FROM data WHERE data.TEMP<0 LIMIT 10")


