
import pandas as pd
import numpy as np
import pymysql as mdb
from sklearn import datasets, linear_model
import pickle


#query the database for each NYC zipcode
def getzipslope(zipcode):  
    con = mdb.connect('localhost', 'root', '', 'noisecomplaintsnewcoord2')
    data = pd.read_sql('SELECT * FROM noisecomplaintsnewcoordtable2 WHERE incident_zip = "%s"' %(zipcode), con)
    #convert date to datetime
    data['created_date']=pd.to_datetime(data['created_date'])
    #make the datetime the index
    data.index = data.created_date
    #give a count of 1 for each complaint
    data['count'] = 1
    dateandcount = data['count']
    #resample the counts by month
    dfmonth=dateandcount.resample('M',how='sum')
    #i have 70 months of data total and need to make a month array
    montharray=np.arange(0,70).reshape(70,1)
    countarray=dfmonth.values
    #make nan values zero
    countarray[np.isnan(countarray)] = 0
    regr = linear_model.LinearRegression()
    regr.fit(montharray, countarray)
    return float(regr.coef_)

#list of all NYC zipcodes
ziplist = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 11005, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697]
#list of zipcodes which fail work
failist = []
#dictionary of zipcode and slope as keys and values respectively
slopedict = {}
for zipcode in ziplist:
    try:
        slopedict[zipcode] = getzipslope(zipcode)
        print "ok",zipcode
    except:
        failist.append(zipcode)
        print "failed", zipcode
        continue

#pickle the dictionary of zipcodes and slopes to call in the main views.py
pickle.dump( slopedict, open( "slopedict.p", "wb" ) )