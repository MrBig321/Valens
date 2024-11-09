# -*- coding: utf-8 -*-

import math
import astronomy
import planets
import modernplanets
import houses
import riseset
import rtofsigns
import placspec
import antiscia
import dodecatemoria
import midpoints
import fixedstars
import lots
import lots2
import syzygy
import util


		
class Chart:
	"""Represents a horoscope"""

	#types
	RADIX, DIRECTION, REVOLUTION, TRANSIT = range(0, 4)

	SIGN_NUM = 12
	SIGN_DEG = 30

	ARIES, TAURUS, GEMINI, CANCER, LEO, VIRGO, LIBRA, SCORPIO, SAGITTARIUS, CAPRICORNUS, AQUARIUS, PISCES = range(0, 12)
	Signs = [0.0, 30.0, 60.0, 90.0, 120.0, 150.0, 180.0, 210.0, 240.0, 270.0, 300.0, 330.0]

	CONIUNCTIO, SEXTIL, QUADRAT, TRIGON, OPPOSITIO, ASPECT_NUM = range(6)
	Aspects = [0.0, 60.0, 90.0, 120.0, 180.0]

	Signboundaries = ((0.0, 30.0), (30.0, 60.0), (60.0, 90.0), (90.0, 120.0), (120.0, 150.0), (150.0, 180.0), (180.0, 210.0), (210.0, 240.0), (240.0, 270.0), (270.0, 300.0), (300.0, 330.0), (330.0, 360.0))

	NONE = -1

	def __init__(self, name, male, htype, time, place, notes, opts, full=True): #full means to calculate everything(e.g. Fixedstars, Antiscia ...)
		self.name = name
		self.male = male
		self.htype = htype
		self.time = time
		self.place = place
		self.options = opts
		self.notes = notes
		self.full = full

		d = astronomy.swe_deltat(time.jd)
		rflag, self.obl, serr = astronomy.swe_calc(time.jd+d, astronomy.SE_ECL_NUT, 0)
		#true obliquity of the ecliptic
		#mean
		#nutation in long
		#nutation in obl

		astronomy.swe_set_topo(place.lon, place.lat, place.altitude)

		self.create()


	def create(self):
		pflag = astronomy.SEFLG_SWIEPH+astronomy.SEFLG_SPEED
		self.ayanamsa = 0.0
		if (self.options.ayanamsa != 0):
			astronomy.swe_set_sid_mode(self.options.ayanamsa-1, 0, 0)
			self.ayanamsa = astronomy.swe_get_ayanamsa_ut(self.time.jd)

		if (self.options.topocentric):
			pflag += astronomy.SEFLG_TOPOCTR

		self.houses = houses.Houses(self.time.jd, 0, self.place.lat, self.place.lon, self.options.hsys, self.obl[0]) #, self.options.ayanamsa, self.ayanamsa)
		self.planets = planets.Planets(self.time.jd, self.options.meannode, pflag, self.place.lat, self.houses.ascmc[houses.Houses.MC][houses.Houses.RA])
		abovehor = self.isAboveHorizon()

		self.modernplanets = modernplanets.Planets(self.time.jd, pflag, self.place.lat, self.houses.ascmc[houses.Houses.MC][houses.Houses.RA])

		self.lots = lots.Lots(self.houses.ascmc, self.planets.planets, abovehor, self.options) #, self.ayanamsa)

		self.syzygy = syzygy.Syzygy(self)

		self.lots2 = lots2.Lots2(self)

		self.dodec = None
		self.riseset = None
		self.risetimeofsigns = None
		self.midpoints = None
		self.fixedstars = None
		if (self.full):
			self.dodec = dodecatemoria.Dodecatemoria(self.planets, self.houses.ascmc, self.lots, self.syzygy, self.options, self.ayanamsa)
			self.antis = antiscia.Antiscia(self.planets, self.houses.ascmc, self.lots, self.syzygy)
			self.riseset = riseset.RiseSet(self.time.jd, self.time.cal, self.place.lon, self.place.lat, self.place.altitude, self.planets)
			self.risetimeofsigns = rtofsigns.RiseTimeOfSigns(self.place.lat, self.obl[0])
			self.midpoints = midpoints.MidPoints(self.planets)
			self.fixedstars = fixedstars.FixedStars(self.time.jd, 0, self.obl[0])

		astronomy.swe_close()

#		self.printData()


	def setHouses(self):
		del self.houses
		self.houses = houses.Houses(self.time.jd, 0, self.place.lat, self.place.lon, self.options.hsys, self.obl[0]) #, self.options.ayanamsa, self.ayanamsa)


	def setNodes(self):
		del self.planets
		pflag = astronomy.SEFLG_SWIEPH+astronomy.SEFLG_SPEED
		self.planets = planets.Planets(self.time.jd, self.options.meannode, pflag, self.place.lat, self.houses.ascmc[houses.Houses.MC][houses.Houses.RA])


	def recalc(self):
#		print ('*** recalc ***')
		del self.houses
		del self.planets
		del self.riseset
		del self.risetimeofsigns
		del self.midpoints
		del self.modernplanets
		del self.lots
		del self.lots2
		del self.syzygy
		del self.antis
		del self.dodec
		del self.fixedstars

		self.create()


	def isAboveHorizon(self):
		abovehorizon = False
		if (not self.options.sectecl):
			mdsun = self.planets.planets[planets.Planets.SUN].speculum.data[placspec.PlacidianSpeculum.MD]
			sasun = self.planets.planets[planets.Planets.SUN].speculum.data[placspec.PlacidianSpeculum.SA]
			abovehorizon = self.planets.planets[planets.Planets.SUN].speculum.abovehorizon

			if (not abovehorizon):
				if (mdsun < 0.0):
					mdsun += 180.0
				if (sasun < 0.0):
					sasun += 180.0

				if (self.options.sectuseorb):
					if (mdsun-self.options.sectorb < sasun):
						abovehorizon = True

		else:
			asclon = self.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
			desclon = util.normalize(self.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]+180.0)
			sunlon = self.planets.planets[planets.Planets.SUN].speculum.data[placspec.PlacidianSpeculum.LON]

			orb = 0.0
			if (self.options.sectuseorb):
				orb = float(self.options.sectorb)
			asclonwithorb = util.normalize(asclon+orb)
			desclonwithorb = util.normalize(desclon-orb)
			dist = asclonwithorb-desclonwithorb
			if (dist < 0.0):	#Pisces-Aries transition above horizon
				if (sunlon > desclonwithorb or sunlon < asclonwithorb):
					abovehorizon = True
			else:
				if (sunlon > desclonwithorb and sunlon < asclonwithorb):
					abovehorizon = True

		return abovehorizon


	def printData(self):
		print('ayanamsa=%f' % self.ayanamsa)



def getBound(lon, opts):
	pos = lon % Chart.SIGN_DEG
	sign = int(lon/Chart.SIGN_DEG)

	subnum = len(opts.bounds[0][0])
	summa = 0.0
	for t in range(subnum):
		summa += opts.bounds[opts.selbounds][sign][t][1]#degs
		if (summa > pos):
			break

	bound = opts.bounds[opts.selbounds][sign][t][0]#planet
	return bound



