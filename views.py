
from app import app
from flask import render_template, request, send_file
import pandas as pd
import numpy as np
import zipcounter
import scipy.stats as st
import pdb
import pickle

#see zipcounter.py for specifics on all functions called from zipcounter
#this is the main code that renders to the output template and collects variables from the input template
#this ultimately generates the annoisyscore which is how relatively loud a zipcode is, the growthscore, how relatively
#quickly a zipcode is getting noisier, a piechart of local types of noises and a streetmap overlaid with a heatmap of 
#kernel density estimates showing relative lows and highs of noise.


#this simple function renders the homepage for the user
@app.route('/')
def annoisy():
    return render_template("input.html", title = 'Home')

@app.route('/about')
def about():
	return render_template("about.html")


#this renders the output page returning the user information about the entered address
@app.route('/output')
def output():
	try: 
		#this fetches the entered address and returns itas a variable address 
		address = request.args.get('ID')
		#this converts the address to latitude, longitude and makes a small rectangle with coordinates
		#around it
		lon, lat, lathigh, latlow, lonhigh, lonlow = zipcounter.zipcount(address)
	except:
		#if the entered address is not valid an error is returned
		return render_template("output_error.html")
		#if the entered address is not within the boundaries of NYC an error is returned
	if lon < -74.257061 or lon > -73.699273 or lat > 40.915087 or lat < 40.498294:
		return render_template("output_error.html")
	try:
		#returns zipcode, complaints for zipcode, slope of complaints over time and counts per 1000 residents
		#otherwise returns error page
		zipcode, countsofzip, zipslope, countsper1000 = zipcounter.zipcodefromaddress(address)
	except:
		return render_template("output_error.html")
	#this the counts of complaints are lower than 500 return the user to a page saying this spot is super quiet
	if countsofzip < 500:
		return render_template("output_error2.html")	
	#this is a list of all the counts of complaints for each zipcode
	complaintsperzip = [16180,13907,13062,12757,12499,11906,11778,11645,11100,11001,10933,10777,10684,9654,9426,9333,9278,8995,8854,8787,8647,8417,8398,8281,8030,7614,7595,7256,7141,6964,6807,6782,6655,6518,6188,5757,5703,5629,5529,5465,5227,5222,5197,5123,4974,4914,4866,4858,4793,4777,4774,4724,4715,4641,4626,4530,4482,4433,4138,4076,4013,4006,3998,3944,3910,3896,3833,3701,3690,3676,3666,3526,3524,3516,3508,3352,3202,3141,3013,3007,2972,2898,2822,2774,2688,2683,2601,2590,2485,2440,2435,2345,2322,2298,2290,2221,2218,2149,2124,2103,2075,2065,2007,1972,1961,1960,1955,1942,1933,1927,1913,1913,1893,1796,1795,1777,1746,1745,1735,1714,1636,1540,1514,1500,1498,1477,1406,1378,1352,1297,1295,1272,1261,1261,1243,1169,1154,1142,1137,1131,1110,1101,1055,1024,1008,986,949,926,912,883,877,874,840,817,748,741,666,663,637,587,528]
	#to determine relative levels of noise the counts for the queried zipcode are compared to those for all zipcodes
	annoisyscore = int(st.percentileofscore(complaintsperzip, countsofzip))

	#list of slopes for each zipcode
	slopelist = [1.664578777,2.018161141,1.395975855,0.3435394979,0.4061062024,0.2213279678,0.4198757764,1.562645438,0.7171726008,1.539725308,1.198145394,1.299536349,1.073921792,1.66414137,1.025684542,0.4936575978,2.308476949,0.3347738606,0.7169276529,1.05548071,0.8112151168,1.519132184,2.372320882,2.341352463,0.9094042516,2.550835447,0.9262881638,2.708966845,3.223392529,1.966652086,3.643163328,1.005826262,2.014049514,0.3571691016,0.7959758551,0.3868078033,4.36150818,1.054308459,0.06149943137,0.3706062462,1.234817601,0.1323418774,0.2298661534,0.169853906,0.01894847345,0.4970518765,0.1668795381,0.09054325956,0.2172163415,0.3395853381,0.1123786195,0.05978479573,-0.005511328843,0.2104102878,0.8474674132,1.496177062,0.747826087,0.2534861342,0.5567141982,1.24489546,1.782661185,0.8957396553,0.3362960371,0.6581576415,0.3964132622,0.4239524101,0.7971656023,0.1934039017,0.1261132009,0.1523401277,0.9685591812,1.19637827,0.3305397603,0.15087044,0.1284577027,1.362225527,0.2850669233,0.07266205931,0.00951797743,0.2025719535,1.100901059,0.589764675,1.144606771,0.6867290701,0.4430058613,0.7717784971,0.09710436532,1.675706412,0.3073746829,0.1388854868,1.436357274,2.518082407,1.067780597,0.7880325431,0.4820050739,0.1022657685,3.036339778,0.1686816551,1.180824075,0.2377569766,1.30160091,2.880902808,1.574122999,0.8317032631,0.3697489284,1.199317645,2.228256495,1.09007086,0.3745254134,0.1945586563,1.949173301,2.283894672,0.1801592162,-0.1393053976,0.6342752165,0.4497419298,0.5541072522,0.7473011985,0.5817688741,0.4472749541,0.2244772986,1.786247922,2.897314321,0.2870789957,0.2384393316,0.2187035255,0.04197358061,0.2189309772,0.04776484997,0.1292100429,0.04090630741,0.06190184586,0.1996325781,1.374805354,0.3726008223,0.7872976992,0.05939987753,0.08609920392,0.9959408626,0.2806753565,0.3723733707,0.4475898871,0.1160878313,0.09259032456,0.03210567754,1.21849357,0.1076546234,0.09031580789,0.06421135509,0.3273904295,0.162592949,0.1292625317,0.2214854343,0.2054063512,0.2659609833,0.2427084245,0.2962645438,0.1364884962,0.4309859155,0.03240311434,0.04972443356,0.08844370571,0.3584463302,0.2104102878,0.2391916718,0.3023007611,0.05889248535,0.2973143207,0.05486834048,0.4845770274]
	#returns rank of slope for queried zipcode relative to other zipcodes
	growthscore = int(st.percentileofscore(slopelist, zipslope))
	#list of complaints per 1000 people
	count1000list = pickle.load(open("app/static/count1000list.p", "rb"))
	#relative rank of counts per 1000 people for queried zipcode relative to other zipcodes
	count1000score = int(st.percentileofscore(count1000list, countsper1000))
	#see zipcounter for details, but this returns a grid of latitude and longitudes from low to high along with the
	#kernel density estimates for each pair of coordinates.
	f,  xx, yy = zipcounter.kerneldensity(address)
	#normalize kernel density estimates by dividing by maximum value
	fmax = np.amax(f)
	fnorm = f/fmax
	#unravel all the coordinates and density estimates and send as a list to a variable heatmaplist which will be read in by leaflet in mapbox
	heatmap_out1 = np.vstack([yy.ravel(),xx.ravel(),fnorm.ravel()])
	df = pd.DataFrame(data=heatmap_out1).T
	df.columns= [['lat', 'lng', 'count']]
	heatmaplist= df.values.tolist()
	#see dictionaryforpiechart.py for details
	zipandpie = pickle.load(open("app/static/zipandpie.p", "rb"))
	piechart = zipandpie[int(zipcode)]



	return render_template("output.html",  count1000score = count1000score, countsper1000=countsper1000, piechart=piechart, address = address, annoisyscore = annoisyscore, growthscore=growthscore, heatmaplist=heatmaplist, lon=lon, lat=lat, latlow=latlow, lathigh=lathigh, lonlow=lonlow, lonhigh=lonhigh, zipcode=zipcode)




