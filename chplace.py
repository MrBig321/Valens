


class Place:
	"""Place of Birth"""

	def __init__(self, placename, deglon, minlon, seclon, east, deglat, minlat, seclat, north, altitude):
		self.placename = placename	

		self.deglon = deglon
		self.minlon = minlon
		self.seclon = seclon
		self.east = east	

		self.deglat = deglat
		self.minlat = minlat
		self.seclat = seclat
		self.north = north

		self.altitude = altitude

		self.lon = deglon+minlon/60.0+seclon/3600.0
		self.lat = deglat+minlat/60.0+seclat/3600.0

		if (not self.north):
			self.lat *= -1.0

		if (not self.east):
			self.lon *= -1.0




