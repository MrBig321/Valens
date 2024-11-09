import math
import planet
import planets
import util


class Mid:
	def __init__(self, p1, p2, m):
		self.p1 = p1
		self.p2 = p2
		self.m = m


class MidPoints:
	"""Computes Midpoints"""

	def __init__(self, pls):
		self.mids = []

		self.calcMidPoints(pls)
	
#		self.printMidPoints(self.mids, pls)


	def calcMidPoints(self, pls):	
		for i in range(planets.Planets.PLANETS_NUM):#Nodes are excluded
			for j in range(i+1, planets.Planets.PLANETS_NUM):
				p1 = pls.planets[i].data[planet.Planet.LON]
				p2 = pls.planets[j].data[planet.Planet.LON]
				d = math.fabs(p1-p2)
				m = 0.0
				if (d <= 180.0):
					if (p1 < p2):
						m = p1+d/2.0
					else:
						m = p2+d/2.0
				else:
					d = 360.0-d
					if (p1 < p2):
						m = p2+d/2.0
					else:
						m = p1+d/2.0
					if (m >= 360.0):
						m -= 360.0

				m = util.normalize(m)

				self.mids.append(Mid(i, j, m))


	def printMidPoints(self, mids, pls):
		print('')
		print('Midpoints:')
		for x in mids:
			d,m,s = util.decToDeg(x.m)
			print("%s-%s: %d %d'%d\"" % (pls.planets[x.p1].name, pls.planets[x.p2].name, d, m, s))



