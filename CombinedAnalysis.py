#import necessary libraries
import numpy as np
import pandas as pd
from pandas import read_csv
from glob import glob

#################################################################
###########set parameters for our battery##################
dischargePowerCap = float(100) #max discharge power capacity in kW
chargePowerCap = float(100) #max charge power capacity in kW
dischargeEnergyCap = float(200) #max discharge energy capacity in kWh
RTefficiency = 0.8 #AC-AC roundtrip efficiency
maxDailyThroughput = float(200) #max daily discharge throughput in kWh
chargeTime = 1 #hour
dischargeTime = 1 #hr
#initializing variables:
storedEnergy = 0
dischargedEnergy = 0
SOE = storedEnergy - dischargedEnergy #state of energy

#############################################################
############market revenue data

#read in all csv files at once from directory
filenames = glob('2017*.csv')
#get list of dataframes for each day
df1= [pd.read_csv(f, header= 0, index_col=0) for f in filenames]

zone ='N.Y.C.' #specify the desired zone
df1 =df1[0]
df1 = df1[df1.Name ==zone]
table = df1.sort_values(by='LBMP ($/MWHr)', ascending=True)
times = table.index.values
#add columns to dataframe containing desired output data
df1 = df1.assign(Battery_Power_Output= np.nan, SOE= np.nan, Hourly_Revenue_Generation= np.nan,
               Hourly_Charging_Cost= np.nan, Throughput= np.nan, IntIndex= np.nan)

#initialize arrays of data that will be inserted into our dataframe
SOE_array = np.zeros(len(table))
Battery_Output_array = np.zeros(len(table))
Hourly_Revenue_array = np.zeros(len(table))
Hourly_Charging_Cost = np.zeros(len(table))
Throughput_array = np.zeros(len(table))
#scale our LBMP values to kW:
LBMPvals = df1['Marginal Cost Congestion ($/MWHr)'].values
#put in a numerical index
l = [i for i in range(24)]
df1['IntIndex'] = l

#sort our given data by price (from lowest to highest price)
table = df1.sort_values(by= 'LBMP ($/MWHr)',ascending= True)

#get our sorted time values into an array
times = table.index.values

#get the integer indexes for highest and lowest prices
chargeIndex = table.iloc[0:2]
chargeIndex = chargeIndex['IntIndex'].sort_values(ascending= True)
dischargeIndex = table.iloc[-2:]
dischargeIndex = dischargeIndex['IntIndex'].sort_values(ascending= True)

#take out highest and lowest prices into separate
#chargingTimes = times[0:2]
#dischargingTimes = times[-2:]

num = len(table)
#create a loop to go through each hour of the day

w = 0
y = 1
q = 1
# create an iterator for charge index
r = 0
# create an iterator of discharge index
k = 0
for z in range(1,len(LBMPvals)):
    print('Z:',z)
    #save date values in variable for comparison with index of lowest/highest hourly LBMP
    #date = df1.index[w]
    #print('DATE: ', date)
    #result = date == chargingTimes
    #result = result[0] | result[1]
    #result2 = date == dischargingTimes
    #result2 = result2[0] | result2[1]



    #create an integer index for each day we iterate through
    #intIndex = table.iloc[w]
    #intIndex = intIndex['IntIndex']
    intIndex = y
    print('IntIndex: ', intIndex)
    print('ChargeIndex: ', chargeIndex[r])
    print('dischargeIndex: ', dischargeIndex[k])

    #conditions where we can charge the battery
    if intIndex == chargeIndex[r]:
        #if SOE_array[y-1]<dischargeEnergyCap:
        SOE_array[y] = SOE_array[y-1] + (chargeTime * chargePowerCap)
        Battery_Output_array[y] = 0 #we do not discharge while charging
        Hourly_Revenue_array[y] = 0 #no revenue is generated while charging
        Hourly_Charging_Cost[y] = -1*LBMPvals[y]*chargeTime
        Throughput_array[y] = 0 #no discharge throughput while charging
        if r == 0:
            r += 1
        print('CHARGE')
        print(SOE_array[y], Battery_Output_array[y], Hourly_Revenue_array[y], Hourly_Charging_Cost[y],
              Throughput_array[y])
        #conditions where we discharge the battery
    elif intIndex == dischargeIndex[k]:
        #if SOE_array[y-1]>float(0):
                #if Throughput_array[y]<maxDailyThroughput:
        SOE_array[y] = SOE_array[y - 1] - dischargePowerCap*dischargeTime
        Battery_Output_array[y] = dischargePowerCap*dischargeTime
        Hourly_Revenue_array[y] = LBMPvals[y] * dischargeTime
        Hourly_Charging_Cost[y] = 0 #no cost for charging while batterry is outputting
        Throughput_array[y] = dischargePowerCap*dischargeTime
        if k == 0:
            k += 1
        print('DISCHARGE')
        print(SOE_array[y], Battery_Output_array[y], Hourly_Revenue_array[y], Hourly_Charging_Cost[y],
              Throughput_array[y])
        #conditions when we are not charging or discharging
    else:
        prevVal = SOE_array[y - 1]
        SOE_array[y] = prevVal
        Battery_Output_array[y] = 0
        Hourly_Revenue_array[y] = 0
        Hourly_Charging_Cost[y] = 0
        Throughput_array[y] = 0  # no discharge throughput while charging
        print('ELSE')
        print(SOE_array[y], Battery_Output_array[y], Hourly_Revenue_array[y], Hourly_Charging_Cost[y],
              Throughput_array[y])



    print('#####################################################')
    #dfName = 'day' + str(q) + '.csv'
    #df1.to_csv(dfName, sep= ',')

    q += 1
    w += 1
    y += 1

df1['Battery_Power_Output'] = Battery_Output_array
df1['SOE'] = SOE_array
df1['Hourly_Revenue_Generation'] = Hourly_Revenue_array
df1['Hourly_Charging_Cost'] = Hourly_Charging_Cost
df1['Throughput'] = Throughput_array
print('FINISHED LOOP')
print(df1)
print('x')
