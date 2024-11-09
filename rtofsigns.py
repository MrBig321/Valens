import math
import util


class RiseTimeOfSigns:
	'''Calculates rising times of signs'''


	def __init__(self, placelat, obl):
		aos = []
		self.riseofsigns = []

		lon = 0.0
		for i in range(7):
			ra, decl = util.transform(lon, 0.0, obl)

			adlat = 0.0
			val = math.tan(math.radians(placelat))*math.tan(math.radians(decl))
			if (math.fabs(val) <= 1.0): # what if not valid? (i.e. else)
				adlat = math.degrees(math.asin(val))

			aos.append(ra-adlat)
			lon += 30.0


		for i in range(6):
			self.riseofsigns.append(aos[i+1]-aos[i])

#		self.printrts()


	def printrts(self):
		for i in range(6):
			print(self.riseofsigns[i])



