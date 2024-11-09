import planet
import planets
import houses
import lots
import texts
import util


class Antiscia:
	'''Computes antiscia of the bodies(Asc, MC, planets, Lots and Syzygy)'''

	CANCER0 = 90.0
	CAPRICORN0 = 270.0

	def __init__(self, pls, ascmc, lots7, syz):
		self.ascmclons = []
		self.plslons = []
		self.lotslons = []
		self.syzlon = 0.0

		ant = self.calc(ascmc[houses.Houses.ASC][houses.Houses.LON])
		self.ascmclons.append(ant)
		ant = self.calc(ascmc[houses.Houses.MC][houses.Houses.LON])
		self.ascmclons.append(ant)

		for i in range(planets.Planets.BODIES_NUM-1):
			ant = self.calc(pls.planets[i].data[planet.Planet.LON])
			self.plslons.append(ant)

		for i in range(lots.Lots.LOTS_NUM):
			ant = self.calc(lots7.data[i])
			self.lotslons.append(ant)

		self.syzlon = self.calc(syz.lon)

#		self.printAnts()


	def calc(self, lon):
		ant = 0.0

		if (lon == Antiscia.CANCER0 or lon == Antiscia.CAPRICORN0):
			ant = lon
		elif (lon > Antiscia.CANCER0 and lon < Antiscia.CAPRICORN0):
			ant = util.normalize(Antiscia.CAPRICORN0+(Antiscia.CAPRICORN0-lon))
		elif (lon < Antiscia.CANCER0):
			ant = util.normalize(Antiscia.CANCER0+(Antiscia.CANCER0-lon))
		elif (lon > Antiscia.CAPRICORN0):
			ant = util.normalize(Antiscia.CAPRICORN0-(lon-Antiscia.CAPRICORN0))

		return ant


	def printAnts(self):
		print(texts.txtscommon['Antiscia'])
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




