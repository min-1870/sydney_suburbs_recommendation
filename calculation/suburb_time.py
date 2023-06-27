import pandas as pd
import time
from googlemap_api import getTravelTime, getCoordinates
import psutil
import os

def print_memory_usage():
    process = psutil.Process(os.getpid())
    print(process.memory_info().rss)  # in bytes 

'''
def calculateSuburbsTravelTime(suburbsDF):
    suburbs = suburbsDF['suburb'].tolist()
    df = pd.DataFrame(columns=suburbs)
    times = []

    for departure in range(len(suburbs)):
        start_time = time.time()
        row = {}
        for destination in range(len(suburbs)):
            if departure == destination:
                row[suburbs[destination]] = 0
            else:
                row[suburbs[destination]] = getTravelTime(getCoordinates(suburbs[departure]), getCoordinates(suburbs[destination]))
        df.loc[departure] = row
        end_time = time.time()
        times.append(end_time - start_time)
        estimate_execution_time = round((sum(times)/len(times)) * (len(suburbs) - departure) / 60, 2)
        print(str(round(departure/len(suburbs)*100)) + '%'+'        '+str(estimate_execution_time)+' minutes')
    return df
'''
def calculateSuburbsTravelTime(suburbsDF):
    suburbs = suburbsDF['suburb'].tolist()
    df = pd.DataFrame(columns=range(len(suburbs)))
    times = []

    for i in range(len(suburbs)):
        start_time = time.time()
        row = {}
        for j in range(i+1, len(suburbs)):
            row[j] = getTravelTime(getCoordinates(suburbs[j]), getCoordinates(suburbs[i]))
            print(str(j)+'/'+str(len(suburbs)))
            print_memory_usage()
        df.loc[i] = row
        df.to_csv("suburb_time.csv", index=False)
        end_time = time.time()
        remain = len(suburbs)-1-i
        if remain != 0:
            times.append((end_time - start_time)/remain)
            estimate_execution_time = round((sum(times)/len(times)) * (remain**2/2) / 60, 2)
        print(str(round(i/len(suburbs)*100)) + '%'+'        '+str(estimate_execution_time)+' minutes')

    dfT = df.T
    resultDF = df.combine_first(dfT).fillna(0)
    resultDF.columns = suburbs
    return resultDF


res = calculateSuburbsTravelTime(pd.read_csv('./original_data/sydney_suburbs.csv'))

res.to_csv("suburb_time.csv", index=False)