import math
import astronomy
import planet
import util


class Planets:
	"""Calculates the positions of the planets"""

#	HELIOCENTRIC = 
#	ECLIPTIC = 
#	EQUATORIAL =
#	XYZ = 
#	TOPOCENTRIC = 
#	SIDEREAL = 
	
	SATURN, JUPITER, MARS, SUN, VENUS, MERCURY, MOON, ANODE, DNODE = range(0, 9)
	PLANETS_NUM = MOON+1
	BODIES_NUM = DNODE+1

	def __init__(self, tjd_ut, meannode, flag, placelat=None, ramc=None):

		self.planets = []

		self.create(self.planets, tjd_ut, meannode, flag, placelat, ramc)

#		self.printPlanets()
		

	def create(self, pls, tjd_ut, meannode, flag, placelat, ramc):
		node = astronomy.SE_TRUE_NODE
		if (meannode):
			node = astronomy.SE_MEAN_NODE

		ids = [Planets.SATURN, Planets.JUPITER, Planets.MARS, Planets.SUN, Planets.VENUS, Planets.MERCURY, Planets.MOON, node]

		for i in ids:
			pls.append(planet.Planet(tjd_ut, i, flag, placelat, ramc))

		data = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		#Node+180.0 in planets
		data[planet.Planet.LON] = util.normalize(pls[-1].data[planet.Planet.LON]+180.0)
		data[planet.Planet.LAT] = pls[-1].data[planet.Planet.LAT]
		data[planet.Planet.DIST] = pls[-1].data[planet.Planet.DIST]
		data[planet.Planet.SPLON] = pls[-1].data[planet.Planet.SPLON]
		data[planet.Planet.SPLAT] = pls[-1].data[planet.Planet.SPLAT]
		data[planet.Planet.SPDIST] = pls[-1].data[planet.Planet.SPDIST]

		dataEqu = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
		#Equatorial: Node+180.0 in planets
		dataEqu[planet.Planet.RAEQU] = util.normalize(pls[-1].dataEqu[planet.Planet.RAEQU]+180.0)
		dataEqu[planet.Planet.DECLEQU] = -1*(pls[-1].dataEqu[planet.Planet.DECLEQU])
		dataEqu[planet.Planet.DISTEQU] = pls[-1].dataEqu[planet.Planet.DISTEQU]
		dataEqu[planet.Planet.SPRAEQU] = pls[-1].dataEqu[planet.Planet.SPRAEQU]
		dataEqu[planet.Planet.SPDECLEQU] = pls[-1].dataEqu[planet.Planet.SPDECLEQU]
		dataEqu[planet.Planet.SPDISTEQU] = pls[-1].dataEqu[planet.Planet.SPDISTEQU]

		pls.append(planet.Planet(tjd_ut, node, flag, placelat, ramc, data, dataEqu))


	def printPlanets(self):
		print('')
		print('Planets:')
		for i in range(Planets.BODIES_NUM):
			print('%s: lon=%f lat=%f' % (self.planets[i].name, self.planets[i].data[planet.Planet.LON], self.planets[i].data[planet.Planet.LAT]))





