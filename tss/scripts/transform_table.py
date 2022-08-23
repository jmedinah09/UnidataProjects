import pandas as pd  #Working with matrices (tables)
from datetime import datetime #For working with date and time
import numpy as np #To work with arrays
from dateutil.parser import parse #https://stackoverflow.com/questions/40121822/extracting-year-from-string-in-python
pd.set_option("display.max_rows", 999) # To control the number of rows to be display while working with the dataframe

data_list = []
with open('LA_LC_data-csv.csv', 'r', encoding="ISO-8859-1") as f: #An error raises if this encoding is not specify
    for line in f.readlines(): #Iterating over each line
        # print(line)
        new_line = line.replace(',,,,,,,,,,,,', '') #To better display the output... not needed in the end, should be dropped
        # print(new_line)
        if new_line.startswith('DATOS DIARIOS'): #grepping this line in order to extract the year
            # print(new_line)
            yy = parse(new_line, fuzzy=True).year #Extracting the corresponding yeat
            # print(yy)
        elif new_line[0].isdigit(): # grepping this line in order to extract the data
            data_line = new_line.split(',') #Esplitting the line into a list of coma separated values
            # print(data_line)
#             # data_line.pop(0)
            data_line[-1] = data_line[-1].replace('\n', '') #Droping the new line character attached to the end of the last values
            # print(data_line)
            DAY, ENE, FEB, MAR, ABR, MAY, JUN, JUL, AGO, SEP, OCT, NOV, DIC = data_line #Unpacking the list into its corresponding fields
            data_list.append([yy, DAY, ENE, FEB, MAR, ABR, MAY, JUN, JUL, AGO, SEP, OCT, NOV, DIC]) # Storing each line into a list to contruct the pandas dataframe
            
df = pd.DataFrame(data_list, columns = [
                                   'YEAR', 'DAY', 'ENE', 'FEB', 'MAR', 'ABR', 
                                   'MAY', 'JUN',  'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC'  #Constructing the data frame
                                       ] )
# df.head()  

df2 = pd.DataFrame(columns=['YEAR', 'MONTH', 'DAY', 'TMAX']) #Creating an empty dataframe to store the data into a time series
data = [] #Creating an empty list to store the rows of the time series
months = ['ENE', 'FEB', 'MAR', 'ABR', 'MAY', 'JUN',  'JUL', 'AGO', 'SEP', 'OCT', 'NOV', 'DIC']
grp_df = df.groupby(['YEAR']) #Breaking into tables of each year
for year in range(1960, 2022, 1): #Iterating over each table corresponding into specific year
    # print(year)
    yr = grp_df.get_group(year) #yr is a dataframe containing the data for a single year like in the original file
    # print(yr)
    for month in months: #Iterating over each month of a given year
        # print(yr[month])
        for t, d in zip(yr[month], yr['DAY']): #Extracting the actual data for each month in a given year a its corresponding date
            data.append([year, month, d, t]) #Storing the rows of each coorresponding day to construc the time series
df2 = pd.DataFrame(data, columns = [
                                   'YEAR', 'MONTH', 'DAY', 'TMAX'  #Constructing the time series dataframe
                                       ] )
df2['MONTH_NUM'] = df2['MONTH'] #Creating a column to store the months in number formats from 1 to 12
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('ENE', '1')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('FEB', '2')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('MAR', '3')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('ABR', '4')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('MAY', '5')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('JUN', '6')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('JUL', '7')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('AGO', '8')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('SEP', '9')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('OCT', '10')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('NOV', '11')
df2['MONTH_NUM'] = df2['MONTH_NUM'].replace('DIC', '12')

df2.reset_index() 
# df2.tail()

df2['YEAR'] = df2['YEAR'].map(str) #Converting the year values from integer datatype tu string data type
df2['DAY']  = df2['DAY'].map(str) #Converting the day values from integer datatype tu string data type
for year, month, day in zip(df2["YEAR"], df2["MONTH_NUM"], df2["DAY"]):
        try:
            pd.to_datetime(year + "/" + month + "/" + day) #Cheking if the dates are real as in the original tables febraury  and all the other months reaches 31 days
        except:
            df2 = df2.drop(df2[(df2['YEAR'] == year) & (df2['MONTH_NUM'] == month) & (df2['DAY'] == day)].index) #Dropping the rows containgin bad dates (i.e: 1960/02/31 or 2020/06/31)
df2["DATE"] = pd.to_datetime(df2["YEAR"] + "/" + df2["MONTH_NUM"] + "/" + df2["DAY"]) #Generating the date column with valid dates
df2 = df2[["DATE", "YEAR", "MONTH", "MONTH_NUM", "DAY", "TMAX"]] #Reordering columns
df2 = df2.replace('-', np.nan) #Replacing missing data with nan
# df2.head(100)

writer = pd.ExcelWriter('time_series.xlsx') #Saving into a excel file
df2.to_excel(writer)
writer.save()