#Corey Brewer Casper Take Home Test Analysis
#10/2/17

#First I import the necessary packages
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime as dt

#Next I download the data from the excel file
xl = pd.ExcelFile('C:\\Users\\cjbdi\\Documents\\Casper\\XLS_takehome_NA_(1)_(1).xlsx')

df = xl.parse(0)
#print(df.head())

#Here I make a numpy array of the dates from Aug 1st 2016 to Dec 31st 2016 without duplicates
dates = np.arange(dt.datetime(2016,12,31), dt.datetime(2016,7,31), dt.timedelta(days= -1)).astype(dt.datetime)
#print(dates)

#Here I make an array with just the total number of orders placed for each day...
# Do this so it is of the same length as our dates array
ords = np.empty(shape = [0])
count = 0

for status in df.iloc[:,2]:
    if count != len(df.iloc[:,0]) - 1:
        if status == 'complete':    #If the status is 'complete', the number of orders is appended to the ords array
            ords = np.append(ords, df.iloc[count, 3])
            count = count + 1
        else:
            count = count + 1

ords = np.append(ords, df.iloc[count, 3])

#print(ords)
#print(len(df.iloc[:,0]))
#print(len(dates))
#print(len(ords))

#Now I make an array with just the total number of returns for each day
# based on when the returned order was originally placed, NOT when it was returned
rets = np.empty(shape = [0])
count = 0
sum_up = 0
for status in df.iloc[:,2]:
    if count != len(df.iloc[:,0]) - 1:
        if status == 'complete' :
            if df.iloc[count - 1,2] == 'complete':
                # If the status is 'complete' and the the previous status is also 'complete',
                # append the rets array with a 0
                rets = np.append(rets, 0)
            count = count + 1
            sum_up = 0
        elif status == 'returned':
            sum_up = sum_up + 1     #Here we add up the number of returns for a given date
            if df.iloc[count + 1, 2] == 'complete':
                #If the status is 'returned' and the next status is 'complete',
                # append the rets array with the total sum for that date
                rets = np.append(rets, sum_up)
            else:
                pass
            count = count + 1
rets = np.append(rets, 0)

#print(rets)
#print(len(rets))

#perc_ret = rets/ords
#print(perc_ret)

#plt.plot(dates, ords)
#plt.show()

#Here I am converting all of my arrays to their 'by month' equivalent

#First I'm putting the dates in a more readable form
months = np.empty(shape = [0])
for d in dates:
    months = np.append(months, d.strftime('%B-%y'))
#print(months)

#Here I am pulling out each month once, while not sorting them alphabetically
mon_array_inds = np.unique(months, return_index=True)[1]
mon_array = [months[index] for index in sorted(mon_array_inds)]
#print(mon_array)

#Now I am getting the sum of the total orders for each month
count = 0
sum_up = 0
ord_per_mon = np.empty(shape = [0])
for mon in months:
    if count != len(months) - 1:
        if mon == months[count + 1]:
            #If the month is the same as the next month, add the number of orders completed to sum_up
            sum_up = sum_up + ords[count]
        elif mon != months[count + 1]:
            #If not, add the final number of orders completed for that month to su_up,
            # then append ord_per_mon with that sum
            sum_up = sum_up + ords[count]
            ord_per_mon = np.append(ord_per_mon, sum_up)
            sum_up = 0
        count = count + 1
    else:
        ord_per_mon = np.append(ord_per_mon, sum_up + ords[-1])

#print(ord_per_mon)
#print(sum(ords[0:31]))
#print(sum(ords[31:61]))
#print(sum(ords[61:92]))
#print(sum(ords[92:122]))
#print(sum(ords[122:153]))

#Now I do the same for the returns per month
count = 0
sum_up = 0
rets_per_mon = np.empty(shape = [0])
for mon in months:      #Here we are doing the same process as the previous for loop
    if count != len(months) - 1:
        if mon == months[count + 1]:
            sum_up = sum_up + rets[count]
        elif mon != months[count + 1]:
            sum_up = sum_up + rets[count]
            rets_per_mon = np.append(rets_per_mon, sum_up)
            sum_up = 0
        count = count + 1
    else:
        rets_per_mon = np.append(rets_per_mon, sum_up + ords[-1])

#print(rets_per_mon)
#print(sum(rets[0:31]))
#print(sum(rets[31:61]))
#print(sum(rets[61:92]))
#print(sum(rets[92:122]))
#print(sum(rets[122:153]))

#Now I am reversing the order of the months list and the returns per month and orders per month arrays
# so they are in the appropriate chronological order
mon_array.reverse()
#print(mon_array)
rets_per_mon = rets_per_mon[::-1]
ord_per_mon = ord_per_mon[::-1]

#here I am simply finding the percent of orders returned each month
perc_ret_per_mon = rets_per_mon/ord_per_mon * 100
#print(perc_ret_per_mon)

#Finally I can plot these arrays by month

x = range(len(mon_array))
plt.xticks(x, mon_array)
plt.plot_date(x, ord_per_mon, 'o-')
plt.title('Orders per Month')
plt.xlabel('Month')
plt.ylabel('Number of Orders')
plt.show()

x = range(len(mon_array))
plt.xticks(x, mon_array)
plt.plot_date(x, rets_per_mon, 'o-')
plt.title('Returns per Month')
plt.xlabel('Month')
plt.ylabel('Number of Returns')
plt.show()

#I decided that the percent of orders returned per month plot would give us the best idea of our return rate by month
x = range(len(mon_array))
plt.xticks(x, mon_array)
plt.plot_date(x, perc_ret_per_mon, 'o-')
plt.title('Percent Returned per Month')
plt.xlabel('Month')
plt.ylabel('Percent of Orders Returned (%)')
plt.show()