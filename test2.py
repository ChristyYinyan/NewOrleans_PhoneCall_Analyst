__author__ = 'yinyan'
from io import StringIO
import csv
import numpy as np
import pandas as pd
import glob
import matplotlib.pyplot as plt
import collections
import operator
import math
###############################################################################################
"""combine file files into one"""
def data_preprocess():
    path=r"NewOrleans"
    allFiles=glob.glob(path+'/*.csv')
    frames=[]
    for file in allFiles:
        df=pd.read_csv(file, index_col=None, header=None)
        frames.append(df)
    final=pd.concat(frames).drop_duplicates()
    final=final[0:10000]
    final.to_csv("data_sample.csv", sep='\t', header=None)
##############################################################################
"""most frequent type"""
def most_frequent_type(data):
    all_type=data['Type_']
    all_type=all_type[1:]
    # print all_type.shape #
    dict=collections.defaultdict(int)
    for type in all_type:
        dict[type]+=1
    value=dict.values()
    maxV=max(value)
    print maxV
    return (maxV*1.0)/len(all_type)#0.245395473953
###################################################################################
"""time to process created to close"""
def time_process(data):
    data_new = data.dropna(subset=['PoliceDistrict','TimeCreate','TimeClosed'])
    district=np.array(data_new['PoliceDistrict'])
    # print set(district)
    # print district.shape
    # print district[1440850:1440854]
    timeS=np.array(data_new['TimeCreate'])
    timeE=np.array(data_new['TimeClosed'])
    districtDict=collections.defaultdict(list)
    for i in range(len(district)):
        # print (timeEFinal[i]-timeSFinal[i]), i
        diff=time_helper(timeS[i], timeE[i])
        districtDict[district[i]]+=[diff]
    mean=[0]*9
    #print districtDict[1]
    for key in districtDict:
        mean[key]=np.mean(districtDict[key])
    return mean
########################################################################################
"""time to process created to close dispatch to arrive"""
def time_process1(data):
    data_new = data.dropna(subset=['TimeDispatch','TimeArrive'])
    timeS=np.array(data_new['TimeDispatch'])
    timeE=np.array(data_new['TimeArrive'])
    lg=len(timeS)
    timeRst=[]
    for i in range(lg):
        temp=time_helper(timeS[i], timeE[i])
        if temp>0:
            timeRst.append(temp)
    return np.median(timeRst)#306.0

def time_helper(timeS, timeE):
    a=pd.Timestamp(timeS)
    b=pd.Timestamp(timeE)
    return (b-a).seconds
########################################################################################
"""the larget increase type from 2011 to 2015"""
def increse_type():
    filePath="NewOrleans"
    data2011=pd.read_csv(filePath+"/Calls_for_Service_2011.csv")
    data2015=pd.read_csv(filePath+"/Calls_for_Service_2015.csv")
    type2011, type2015=data2011['Type_'], data2015['Type_']
    typeTotal=list(set(type2011))+list(set(type2015))
    # print typeTotal, len(typeTotal)#295 types in total
    dict1=collections.defaultdict(int)
    dict2=collections.defaultdict(int)
    for t in type2011:
        dict1[t]+=1
    for t in type2015:
        dict2[t]+=1
    ref1, ref2=percentage_helper(dict1,len(type2011)), percentage_helper(dict2, len(type2015))
    maxDif=-2**31
    for type in typeTotal:
        if type in ref1 and type in ref2:
            maxDif=max(maxDif, ref1[type]-ref2[type])
    return maxDif#0.0731536073115
def percentage_helper(dict,total):
    for key, values in dict.items():
        dict[key]=float(values)/total
    return dict
######################################################################################
def largestRatio(data):

    MaxRatio=0

    data_new = data.dropna(subset=['Type_','PoliceDistrict'])
    events=np.array(data_new['Type_'])
    num_events=events.shape[0]

    event=set(events)
    d=dict()
    for i in events:
        if i not in d:
            d[i]=1
        else:
            d[i]+=1
    district=np.array(data_new['PoliceDistrict'])
    dict_list=collections.defaultdict(list)
    for i in range(district.shape[0]):
        dict_list[district[i]]+=[events[i]]
    for key, value in dict_list.items():
        dic=dict()
        for i in value:
            if i not in dic:
                dic[i]=1
            else:
                dic[i]+=1
        for d_key in dic:
            if d[d_key]>10:
                ratio=(dic[d_key]/(len(value)*1.0))/(d[d_key]/(num_events*1.0))
                MaxRatio=max(ratio,MaxRatio)
    return MaxRatio

##################################################################################3
def largestDistrict(data):
    largestDis=0
    data_new = data.dropna(subset=['Location','PoliceDistrict'])
    policeDis=np.array(data_new['PoliceDistrict'])
    Location=np.array(data_new['Location'])

    dic= collections.defaultdict(list)

    for i in range(policeDis.shape[0]):
        dic[policeDis[i]]+=[Location[i]]
    for key,value in dic.items():
        x=np.zeros(len(value))
        y=np.zeros(len(value))
        xi=0
        for i in range(len(value)):
            l=value[i][1:-2]
            loc=l.split(",")

            if float(loc[0])>26 and float(loc[0])<30 and float(loc[1])>-93 and float(loc[1])<-87:
                x[xi]=float(loc[0])
                y[xi]=float(loc[1])
                xi+=1
        x=np.trim_zeros(x)
        y=np.trim_zeros(y)
        stdX=np.std(x)
        stdY=np.std(y)
        meanX=np.mean(x)
        meanY=np.mean(y)

        bootom_la=math.radians(meanX-stdX)
        top_la=math.radians(meanX+stdX)
        delta_la=math.radians(2*stdX)
        delta_long=0

        a=math.sin(delta_la)*math.sin(delta_la)+math.cos(bootom_la)*math.cos(top_la)*math.sin(delta_long/2)*math.sin(delta_long/2)
        c=2* math.atan2(math.sqrt(a),math.sqrt(1-a))
        d_x=6371*c/2

        delta_la=0
        delta_long=math.radians(2*stdY)
        la=math.radians(meanX)

        a=math.sin(delta_la)*math.sin(delta_la)+math.cos(la)*math.cos(la)*math.sin(delta_long/2)*math.sin(delta_long/2)
        c=2*math.atan2(math.sqrt(a),math.sqrt(1-a))
        d_y=6371*c/2

        area=math.pi*d_x*d_y
        print area, key, meanX,meanY,stdX,stdY
        largestDis=max(area,largestDis)
    return largestDis


#################################################################################
def largestDisposition(data):
    largestDis=0
    data_new = data.dropna(subset=['TimeCreate','Disposition'])

    disp=np.array(data_new['Disposition'])
    TimeCreate=np.array(data_new['TimeCreate'])

    disc=collections.defaultdict(list)
    hour_disp=np.zeros(24)


    for i in range(disp.shape[0]):
        disc[disp[i]]+=[TimeCreate[i]]
    for i in range(TimeCreate.shape[0]):
        time=pd.Timestamp(TimeCreate[i])
        h=time.hour
        hour_disp[h]+=1
    for key,value in disc.items():
        frac=np.zeros(24)
        for i in value:
            time=pd.Timestamp(i)
            h=time.hour
            frac[h]+=1
        frac=frac*1.0/hour_disp
        #print frac
        change=np.max(frac)-np.min(frac)
        largestDis=max(change,largestDis)
    return largestDis


########################################################
def priorityVariation(data):

    smallest_fraction=1

    data_new = data.dropna(subset=['Type_','Priority'])
    type=np.array(data_new['Type_'])
    prio=np.array(data_new['Priority'])
    disc=collections.defaultdict(list)
    for i in range(len(prio)):
        disc[type[i]]+=[prio[i]]
    for key,value in disc.items():
        d=dict()
        total=len(value)
        for i in value:
            if i not in d:
                d[i]=1
            else:
                d[i]+=1
        s=max(d.values())
        s=s*1.0/total
        smallest_fraction=min(smallest_fraction,s)
    return smallest_fraction



#######################################################################################


if __name__=="__main__":
    """
        ['0' 'NOPD_Item' 'Type_' 'TypeText' 'Priority' 'MapX' 'MapY' 'TimeCreate'
     'TimeDispatch' 'TimeArrive' 'TimeClosed' 'Disposition' 'DispositionText'
     'BLOCK_ADDRESS' 'Zip' 'PoliceDistrict' 'Location']
    """
    data=pd.read_csv("data.csv", sep='\t')
    # print data[1:4]
    #data_preprocess()
    # print most_frequent_type(data)
    #print time_process(data)
    #print "largestRatio",largestRatio(data) #64.8346887192
    #print "largestDistrict", largestDistrict(data) #18.204466952
    #print  "largestDisposition",largestDisposition(data) #0.188089465
    print "prioritVariation",priorityVariation(data)  # 0.3073611
    # print time_process1(data)
    # print increse_type()
    # print frequency_on_each_strict(data)

