import pandas as pd
import pymysql as mdb
import pickle
import scipy.stats as st

#this code returns the counts of complaints per 1000 residents for the year of 2013. This is because the most recent easily available data for population is from 2013.

#list of all NYC zipcodes
ziplist = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 11005, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697]
#my database of 311 noise complaints
con = mdb.connect('localhost', 'root', '', 'noisecomplaintsnewcoord2')

#for each zipcode I query the database for number of complaints for that zipcode in 2013 and make a dictionary of zipcodes as keys with counts as values
zip_count2013 = {}
#this list is for any zipcodes that do not appear in my database
fail_zip =[]

for zipcode in ziplist:
    try:
    	#query database
        data2013 = pd.read_sql('SELECT * FROM noisecomplaintsnewcoordtable2 WHERE incident_zip = "%s"  AND created_date <= "2013-12-31" AND created_date >= "2013-01-01"' %(zipcode), con)
        #number of complaints is the length of the returned query as each line is one complaint
        zip_count2013[zipcode] = len(data2013)
    except:
        fail_zip.append(zipcode)
#read in population data and only keep columns with zipcode and population
peoplezip = pd.read_csv('populationperzipcode.csv') 
peoplezip = peoplezip[['zipcode', 'population2013']]   
#convert the dataframe to a dictionary
zipandpeople= dict([(zipcode,population ) for zipcode, population , in zip(peoplezip.zipcode, peoplezip.population2013)])

#for each zipcode, I  divide the total counts by the total population and multiply by 1000 to get counts per 1000 people.
#Generate a dictionary with the zipcodes as the keys and counts per 1000 residents as the values.
zipandcountper1000 = {}
failziperpeeps = []
ziplist = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 11005, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697]
for zipcode in ziplist:
    try:
        zipandcountper1000[zipcode] = int(round(1000*(float(zip_count2013[zipcode])/float(zipandpeople[zipcode]))))
    except:
        failziperpeeps.append(zipcode)

#Pickle the dictionary to call in the main code.
pickle.dump( zipandcountper1000, open("zipandcountper1000.p", "wb" ) )
#list of just the values of counts per 1000 residents
count1000list = list(zipandcountper1000.values())

#In the main code I would, load the dictionary, determine the counts per 1000 residents for the queried zipcode,
countsper1000dict = pickle.load(open("app/static/zipandcountper1000.p", "rb"))
countsper1000 = countsper1000dict[int(zipcode)]
#look at the percentile of the countsper1000 for the queried zipcode relative to the counts for all zipcodes
count1000score = int(st.percentileofscore(count1000list, countsper1000))      
                         