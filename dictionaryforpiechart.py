import pandas as pd
import pymysql as mdb
import pickle
#this code generates a pickled dictionary which serves as an input for D3 piecharts
#the chart is of counts of different kinds of noise complaints for each zipcode. Because there are so many descriptors I kept the top six for each zipcode
#and grouped the rest in other. I also shortened the names of many of the common descriptors that are long and cumbersome.

#list of all zipcodes in NYC
ziplist = [10001, 10002, 10003, 10004, 10005, 10006, 10007, 10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10018, 10019, 10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028, 10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037, 10038, 10039, 10040, 10044, 10065, 10069, 10075, 10103, 10110, 10111, 10112, 10115, 10119, 10128, 10152, 10153, 10154, 10162, 10165, 10167, 10168, 10169, 10170, 10171, 10172, 10173, 10174, 10177, 10199, 10271, 10278, 10279, 10280, 10282, 10301, 10302, 10303, 10304, 10305, 10306, 10307, 10308, 10309, 10310, 10311, 10312, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457, 10458, 10459, 10460, 10461, 10462, 10463, 10464, 10465, 10466, 10467, 10468, 10469, 10470, 10471, 10472, 10473, 10474, 10475, 11004, 11005, 11101, 11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204, 11205, 11206, 11207, 11208, 11209, 11210, 11211, 11212, 11213, 11214, 11215, 11216, 11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225, 11226, 11228, 11229, 11230, 11231, 11232, 11233, 11234, 11235, 11236, 11237, 11238, 11239, 11351, 11354, 11355, 11356, 11357, 11358, 11359, 11360, 11361, 11362, 11363, 11364, 11365, 11366, 11367, 11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377, 11378, 11379, 11385, 11411, 11412, 11413, 11414, 11415, 11416, 11417, 11418, 11419, 11420, 11421, 11422, 11423, 11424, 11425, 11426, 11427, 11428, 11429, 11430, 11432, 11433, 11434, 11435, 11436, 11451, 11691, 11692, 11693, 11694, 11697]

pielist=[]
finaldict={}
#for each zipcode query the database and pull out all noise complaints
for zipcode in ziplist:
    con = mdb.connect('localhost', 'root', '', 'noisecomplaintsnewcoord2')
    #query database of all instances of descriptors in the zipcode
    alldata = pd.read_sql('SELECT descriptor FROM noisecomplaintsnewcoordtable2 WHERE incident_zip = "%s"' %(zipcode), con)
    dflist = alldata['descriptor'].values.tolist()
    #a dictionary with each descriptor as the keys and the number of times it exists as values for the zipcode
    descounts = {}
    #shorten long descriptor names
    for i in dflist:
        if i=='Noise: Construction Before/After Hours (NM1)':
            i ='Construction'
        if i=='Noise: Construction Equipment (NC1)':
            i='Construction Equipment'
        if i == 'Noise: Jack Hammering (NC2)':
            i = 'Jack Hammering'
        if i == 'Banging/Pounding':
            i = 'Banging'
        if i == 'Loud Music/Party':
            i = 'Music/Party'
        if i == 'Noise: air condition/ventilation equipment (NV1)':
            i = 'Air condition/ventilation'
        if i == 'Noise: Air Condition/Ventilation Equip, Commercial (NJ2)':
            i = 'Air condition/ventilation'
        if i == 'Noise: Air Condition/Ventilation Equip, Residential (NJ1)':
            i = 'Air condition/ventilation'
        if i == 'Noise, Barking Dog (NR5)':
            i = 'Barking Dog'
        if descounts.has_key(i):
            descounts[i] = descounts[i] + 1
        else:
            descounts[i] = 1
    #create a flipped version of the above dictionary with descriptor counts as values so it can be sorted
    res = dict((v,k) for k,v in descounts.iteritems())
    #convert to a soted list of tuples of count and descriptor
    ressorted = sorted(res.iteritems(), reverse = True)
    resortedf = pd.DataFrame(ressorted, columns=['count', 'descriptor'])
    #take the top 6 types of complaints
    resortedhigh = resortedf[:6]
    #combine the rest of complaints into an other category
    resortedrest = resortedf[6:]
    #keep only counts
    resortedrestdf= resortedrest['count']
    #add up all counts and combine as 'other' and add on after the top six descriptors
    resortedhigh.loc[len(resortedhigh)]=[df.sum(axis=0), 'other']
    resortedordered=resortedhigh[['descriptor', 'count']]
    #convert to list
    orderedlist = resortedordered.values.tolist()
    #generate a dictionary with keys as zipcodes and values in a list form that D3 accepts which is a list of dictionaries 
    #with keys as 'label' which holds the value of descriptor and a second key as 'value' whose value is counts
    pielist=[]
    for i in range(len(orderedlist)):
        dictionary= {'label':orderedlist[i][0], 'value': orderedlist[i][1]}
        pielist.append(dictionary)
    finaldict[zipcode]=pielist

#pickle dictionary to call for specific zipcodes in my views file
pickle.dump( finaldict, open( "zipandpie.p", "wb" ) )