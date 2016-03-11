import pandas as pd
import numpy as np
import geocoder
import time

#downloaded a csv of all nyc firestations from nyc open data. I want to convert the addresses to latitude and longitude coordinates.
firestations = pd.read_csv("FDNY_Firehouse_Listing.csv")
#convert column with addresses to list
firestations2 = firestations.ix[1:]
addresses = firestations2['FacilityAddress'].values.tolist()

#a function that takes each address in the list, adds new york to it, because they are only give in number and street and retrieve lat and long
#using geocoder.
def addresstolatlon(address):
        g = geocoder.google(address + ', New York')
        lon=g.geojson['geometry']['coordinates'][0]
        lat=g.geojson['geometry']['coordinates'][1]
        return (lat, lon)

#make a list of the station coordinates, added in a pause in case geocoder api gets grumpy if you call it too frequently
stationcoords = []
for address in newaddresses:
    stationcoords.append(addresstolatlon(str(address)))
    time.sleep(2)
    print address

#convert station coordinates to dataframe, label the columns and then write out as a .csv format
stationcoords = pd.DataFrame(stationcoords)
stationcoords.columns=['latitude', 'longitude']
stationcoords.to_csv('finalallfirestationcoords.csv')