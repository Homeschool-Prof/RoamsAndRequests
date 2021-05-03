import pandas as pd
df = pd.read_csv("/Users/Jared/Desktop/XCC_StationEventsLog.csv")

def roams(df):
    event = df['Event Type'][:]
    mac = df['MAC Address'][:]
    ap = df['AP Name'][:]
    roamCount = 0
    roamSet = set()
    MacRoamCount = {} # for number of times each MAC was responded to
    ApResponseCount = {} # for number of roams to which each AP responded  
    for i in range(len(event)):
        if event[i] == "Roam":
            roamSet.add(ap[i])
            roamCount += 1
            if ap[i] in ApResponseCount: 
                ApResponseCount[ap[i]] = ApResponseCount[ap[i]] + 1
            else:
                ApResponseCount[ap[i]] = 1
            if mac[i] in MacRoamCount: 
                MacRoamCount[mac[i]] = MacRoamCount[mac[i]] + 1
            else:
                MacRoamCount[mac[i]] = 1
    busiestAp = max(ApResponseCount, key=lambda key: ApResponseCount[key])
    roamingestMac = max(MacRoamCount, key=lambda key: MacRoamCount[key])
    return ("Total roaming events: %s" %roamCount, 
            "Unique APs roamed to: %s" %roamSet,
            "MAC: number of times it roamed: %s" %MacRoamCount,
            "AP: number of roams to which it responded: %s" %ApResponseCount,
            "The award for most roaming MAC goes to... %s" %roamingestMac,
            "The award for busiest AP goes to... %s" %busiestAp)
roams(df)        
#################################################################################
dffw = pd.read_fwf("/Users/Jared/Desktop/gateway_134.141.123.1.txt", header=None)
import re
import math

def requests(dffw):
    rows = len(dffw.index)
    ms = dffw[4][:].dropna()  # drop nans (which are the timed-out requests)
    ms = ms.reset_index(drop=True)
    pattern = "[^0-9]"
    timeArray = []
    for i in range(len(ms)):
        old = ms[i]
        timeArray.append(int(re.sub(pattern,"", old)))           
    tsum = 0
    tsumsq = 0
    for i in range(len(timeArray)):
        tsum  += timeArray[i]
        tsumsq += timeArray[i]*timeArray[i]
    sd = math.sqrt((tsumsq - (tsum*tsum)/(len(timeArray)))/(len(timeArray)-1))
    mean = tsum/len(timeArray)
    outlierCount = 0
    outliers = []
    for i in range(len(timeArray)):
        if (timeArray[i]-mean)/sd > 1.96:
            outliers.append(timeArray[i])
            outlierCount += 1
    outList = list(sorted(outliers))[::-1]
    gateTimeOuts = rows - len(ms)    
    gateSuccess = rows - gateTimeOuts
    percOutliers = ((outlierCount+gateTimeOuts)/rows)*100
    return ("Total successes: %s" %gateSuccess, 
            "Total time-outs: %s" %gateTimeOuts,
            "Mean time to reply: %s" %mean,
            "SD of time to reply: %s" %sd,
            "Number of outliers (2 SDs above mean): %s" %outlierCount,
            "Percentage of outliers including time-outs: %s" %percOutliers,
            "Outliers (largest to smallest): %s" %outList)
requests(dffw)
