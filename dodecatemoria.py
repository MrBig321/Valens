import math
import planet
import planets
import houses
import lots
import syzygy
import util
import texts


class Dodecatemoria: #Csaba
	'''Computes dodecatemoria (twelfth parts) of the bodies(Asc, MC, planets, Lots and Syzygy)'''


	def __init__(self, pls, ascmc, lots7, syz, opts, ayan):
		self.ascmclons = []
		self.plslons = []
		self.lotslons = []
		self.syzlon = 0.0

		self.options = opts
		self.ayan = ayan

		lon = ascmc[houses.Houses.ASC][houses.Houses.LON]
		self.ascmclons.append(self.calc(lon))

		lon = ascmc[houses.Houses.MC][houses.Houses.LON]
		self.ascmclons.append(self.calc(lon))

		for i in range(planets.Planets.BODIES_NUM-1):
			lon = pls.planets[i].data[planet.Planet.LON]
			self.plslons.append(self.calc(lon))

		for i in range(lots.Lots.LOTS_NUM):
			self.lotslons.append(self.calc(lots7.data[i]))

		self.syzlon = self.calc(syz.lon)

#		self.printDodecatemoria()


	def calc(self, lon):
		if (self.options.ayanamsa != 0):
			lon -= self.ayan
			lon = util.normalize(lon)

		return self.KeepInZodiac(30*self.getSign(lon) + 12*self.getRelativeLon(lon))


	def KeepBetweenLimit(self, lon, lim):
		""" Keep the longitude between 0..lim """
		""" lon must be positive """
		return lon - math.floor(lon / lim) * lim

	
	def KeepInZodiac(self, lon):
		""" Keep the longitude between 0..360 """
		return self.KeepBetweenLimit(lon, 360)

	
	def getRelativeLon(self, lon):
		""" Returns the longitude relative to the zodiac """
		""" Ex. lon = 36 will return 6 (Taurus 6)"""
		return self.KeepBetweenLimit(lon, 30)


	def getSign(self, lon):
		""" Returns the sign: 0 - Aries, 1 - Taurus, 2 - Gemini..."""
		""" lon must be positive """
		return lon // 30


	def printDodecatemoria(self):
		print(texts.txtscommon['Dodecatemoria'])
		num = len(self.ascmclons)
		for i in range(num):
			txt = ''
			if (i == 0):
				txt = texts.txtscommon['Asc']
			else:
				txt = texts.txtscommon['MC']
			print('%s: %f' % (txt, self.ascmclons[i]))

		num = len(self.plslons)
		for i in range(num):
			txt = texts.planets[i]
			print('%s: %f' % (txt, self.plslons[i]))

		num = len(self.lotslons)
		for i in range(num):
			txt = texts.lotsList[i]
			print('%s: %f' % (txt, self.lotslons[i]))

		txt = texts.txtscommon['Syzygy']
		print('%s: %f' % (txt, self.syzlon))


