import math
import astronomy
import planet
import util


class Planets:
	"""Calculates the positions of the modern planets"""

#	HELIOCENTRIC = 
#	ECLIPTIC = 
#	EQUATORIAL =
#	XYZ = 
#	TOPOCENTRIC = 
#	SIDEREAL = 
	
	URANUS, NEPTUNE, PLUTO = range(7, 10)
	PLANETS_NUM = 3

	def __init__(self, tjd_ut, flag, placelat=None, ramc=None):

		self.planets = []

		self.create(self.planets, tjd_ut, flag, placelat, ramc)

#		self.printPlanets()
		

	def create(self, pls, tjd_ut, flag, placelat, ramc):

		ids = [Planets.URANUS, Planets.NEPTUNE, Planets.PLUTO]

		for i in ids:
			pls.append(planet.Planet(tjd_ut, i, flag, placelat, ramc))


	def printPlanets(self):
		print('')
		print('Modern Planets:')
		for i in range(Planets.PLANETS_NUM):
			print('%s: lon=%f lat=%f' % (self.planets[i].name, self.planets[i].data[planet.Planet.LON], self.planets[i].data[planet.Planet.LAT]))





