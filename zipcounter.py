import geocoder
import pandas as pd
import pymysql as mdb
import numpy as np
from sklearn import datasets, linear_model
from sklearn.neighbors import KernelDensity
import scipy.stats as st
import pickle
#this code is the main functions that are called by views.py

#converts the queried address to latitude, longitude and makes a small rectangle around the query. The limits of this rectangle are used
#for the zoom boundaries of the street map shown in output.html
def zipcount(address):
    g = geocoder.google(address)
    lon=g.geojson['geometry']['coordinates'][0]
    lat=g.geojson['geometry']['coordinates'][1]
    lathigh = float(lat + 0.005)
    latlow = float(lat - 0.005)
    lonhigh = float(lon + 0.005)
    lonlow = float(lon - 0.005)
    return lon, lat, lathigh, latlow, lonhigh, lonlow

#converts the user entered address to a zipcode, and returns counts of complaints for this zipcode, the slope across complaints for this zipcode and complaints per 1000 residents
#separate files for the calculations of complaints and linear regression coefficients for each zipcode are included in the project folder
def zipcodefromaddress(address):
    #reads address
    g =geocoder.google(address)
    #converts address to zipcode
    zipcode = g.address.split('NY ')[1].split(',')[0]
    #dictionary of keys as zipcodes and values as counts of complaints per zipcode
    zipcountdict = pickle.load(open("app/static/zipcountdict.p", "rb"))
    countsofzip = zipcountdict[zipcode]
    #dictionary of keys as zipcodes and values as slopes across time for each zipcode
    slopedict = pickle.load(open("app/static/slopedict.p", "rb"))
    zipslope = slopedict[int(zipcode)]
    #dictionary of keys as zipcodes and values as complaints per 1000 residents
    countsper1000dict = pickle.load(open("app/static/zipandcountper1000.p", "rb"))
    countsper1000 = countsper1000dict[int(zipcode)]
    return zipcode, countsofzip, zipslope, countsper1000

#performs kernel density estimation and makes a meshgrid of longitude and latitudes
def kerneldensity(address):
    #extract latitude and longitude of address
    g = geocoder.google(address)
    lon=g.geojson['geometry']['coordinates'][0]
    lat=g.geojson['geometry']['coordinates'][1]
    #makes a small rectangle around address
    lathigh = float(lat + 0.0025)
    latlow = float(lat - 0.0025)
    lonhigh = float(lon + 0.0025)
    lonlow = float(lon - 0.0025)
    #converts coordinates to strings
    latlonhigh = str(lathigh), str(lonhigh)
    latlonlow = str(latlow), str(lonlow)
    lathighlonlow = str(lathigh), str(lonlow)
    latlowlonhigh = str(latlow), str(lonhigh)
    #determines the zipcodes of each corner of the rectangle. this is important for cases where the queried address is on the edge of a zipcode and I want to return
    #data for neighboring zipcodes.
    g =geocoder.google(latlonhigh, method='reverse')
    zipcodea = g.address.split('NY ')[1].split(',')[0]
    g =geocoder.google(latlonlow, method='reverse')
    zipcodeb = g.address.split('NY ')[1].split(',')[0]
    g =geocoder.google(lathighlonlow, method='reverse')
    zipcodec = g.address.split('NY ')[1].split(',')[0]
    g =geocoder.google(latlowlonhigh, method='reverse')
    zipcoded = g.address.split('NY ')[1].split(',')[0]
    #query the database for complaints for each zipcode
    con = mdb.connect('localhost', 'root', '', 'noisecomplaintsnewcoord2')
    data = pd.read_sql('SELECT longitude, latitude FROM noisecomplaintsnewcoordtable2 WHERE incident_zip IN ("%s", "%s", "%s", "%s") AND created_date <= "2015-10-31" AND created_date >= "2015-01-01"' %(zipcodea, zipcodeb, zipcodec, zipcoded), con)
    #determine the minimum longitude and latitude
    minimum = data[['longitude', 'latitude']].min()
    #determine the maximum longitude and latitude
    maximum = data[['longitude', 'latitude']].max()
    #convert latitude and logitude coordinates for each complaint to numpy array
    lonlat = data[['longitude', 'latitude']].values
    resolution = 300j
    #make a gride of 300 by 300 of latitude and longitudes going from the mininum to maximum values
    xx, yy = np.mgrid[minimum[0]:maximum[0]:resolution, minimum[1]:maximum[1]:resolution]
    #unravel this grid to vertical stacks
    positions = np.vstack([xx.ravel(), yy.ravel()])
    #unravel that latitude and longitude complaint coordinates to vertical stacks
    values = np.vstack([lonlat[:,0], lonlat[:,1]])
    #the sklearn kernel density also was used. both this and the scipy version gave good estimates I chose the
    #scipy because while is semi overfit the data, because the leaflet heatmap was not very sensitve it helped 
    #visualise low and highly dense regions better.
    #sklearn bandwidth was calucated using gridsearch crossvalidation
    #kde = KernelDensity(kernel='exponential', bandwidth=0.0004).fit(values.T)
    #log_dens = kde.score_samples(positions.T)
    #f = np.reshape(log_dens, xx.shape)
    #get the kernel density estimate for the coordinates given
    kernel = st.gaussian_kde(values) 
    f = np.reshape(kernel(positions).T, xx.shape)

    return f, xx, yy

