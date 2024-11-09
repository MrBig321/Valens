import json
#from urllib.parse import urlencode
#from urllib.request import urlopen
import urllib.request
import urllib.parse


#Csaba's code

class Geonames:
	NAME, LON, LAT, COUNTRYCODE, COUNTRYNAME, ALTITUDE, GMTOFFS = range(0, 7)
	lang = "en"
	USERNAME = 'morinastro'

	def __init__(self, city, maxnum):
		self.city = city
		self.maxnum = maxnum
		self.li = None


	def fetch_values_from_page(self, url, params, key):
		url = url % urllib.parse.urlencode(params)

		try:
			page = urllib.request.urlopen(url) 
			doc = json.loads(page.read().decode("utf-8"))
			values = doc.get(key, None)
		except Exception as e:
			#print(e)
			values = None

		return values


	def get_basic_info(self, city):
		url = "http://api.geonames.org/searchJSON?%s"

		params = {
			"username" : Geonames.USERNAME,
			"lang" : Geonames.lang,
			"q" : city,
			"featureClass" : "P",
			"maxRows" : self.maxnum,
			}

		return self.fetch_values_from_page(url, params, "geonames")


	def get_gmt_offset(self, longitude, latitude):
		url = "http://api.geonames.org/timezoneJSON?%s"
		params = {
			"username" : Geonames.USERNAME,
			"lng" : longitude,
			"lat" : latitude,
			}
		return self.fetch_values_from_page(url, params, "rawOffset")


	def get_elevation(self, longitude, latitude):
		url = "http://api.geonames.org/astergdemJSON?%s"
		params = {
			"username" : Geonames.USERNAME,
			"lng" : longitude,
			"lat" : latitude,
			}
		return self.fetch_values_from_page(url, params, "astergdem")


	def get_location_info(self):
		info = self.get_basic_info(self.city)

		if (info == None):
			return False

		self.li = []
		for it in info:
			longitude = it.get("lng", 0)
			latitude = it.get("lat", 0)
			placename = it.get("name", "")
			country_code = it.get("countryCode", "")
			country_name = it.get("countryName", "")

			gmt_offset = self.get_gmt_offset(longitude, latitude)
			elevation = self.get_elevation(longitude, latitude)

			self.li.append((placename, float(longitude), float(latitude), 
				country_code, country_name, elevation, gmt_offset))

		return True



