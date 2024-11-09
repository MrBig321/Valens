import houses
import planets
import planet
#import placspec
import texts
import util


class Lots:
	''' The seven hellenistic lots '''

	FORTUNE = 0
	SPIRIT = 1
	EROS = 2
	VICTORY = 3
	NECESSITY = 4
	COURAGE = 5
	NEMESIS = 6
	LOTS_NUM = 7


	def __init__(self, ascmc, pls, abovehorizon, opts):
		self.data = []

		asclon = ascmc[houses.Houses.ASC][houses.Houses.LON]
		saturnlon = pls[planets.Planets.SATURN].data[planet.Planet.LON]
		jupiterlon = pls[planets.Planets.JUPITER].data[planet.Planet.LON]
		marslon = pls[planets.Planets.MARS].data[planet.Planet.LON]
		sunlon = pls[planets.Planets.SUN].data[planet.Planet.LON]
		venuslon = pls[planets.Planets.VENUS].data[planet.Planet.LON]
		mercurylon = pls[planets.Planets.MERCURY].data[planet.Planet.LON]
		moonlon = pls[planets.Planets.MOON].data[planet.Planet.LON]

		#Fortune
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = moonlon-sunlon
		else:
			diff = sunlon-moonlon

		fortunelon = util.normalize(asclon+diff)
		self.data.append(fortunelon)

		#Spirit
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = sunlon-moonlon
		else:
			diff = moonlon-sunlon

		spiritlon = util.normalize(asclon+diff)
		self.data.append(spiritlon)

		#Eros
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = venuslon-spiritlon
		else:
			diff = spiritlon-venuslon

		eroslon = util.normalize(asclon+diff)
		self.data.append(eroslon)

		#Victory
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = jupiterlon-spiritlon
		else:
			diff = spiritlon-jupiterlon

		jupiterlon = util.normalize(asclon+diff)
		self.data.append(jupiterlon)

		#Necessity
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = fortunelon-mercurylon
		else:
			diff = mercurylon-fortunelon

		necessitylon = util.normalize(asclon+diff)
		self.data.append(necessitylon)

		#Courage
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = fortunelon-marslon
		else:
			diff = marslon-fortunelon

		couragelon = util.normalize(asclon+diff)
		self.data.append(couragelon)

		#Nemesis
		diff = 0.0
		if (abovehorizon or opts.sectptolemy):
			diff = fortunelon-saturnlon
		else:
			diff = saturnlon-fortunelon

		nemesislon = util.normalize(asclon+diff)
		self.data.append(nemesislon)

#		self.printLots()

#		self.data = (31, 32, 33, 34, 35, 36, 37)


	def printLots(self):
		print ('')
		num = len(texts.lotsList)
		for i in range(num):
			print ('%s lon=%f' % (texts.lotsList[i], self.data[i]))





