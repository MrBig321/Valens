import astronomy
import chart
import chtime
import planet
import planets
import houses
import lots
import util


class Transit:
	NONE = -1
	RETR = 0
	STAT = 1

	ASCMC = 0
	PLANET = 1
	SIGN = 2
	ANTISCION = 3
	LOT = 4
	SYZYGY = 5


	def __init__(self):
		self.plt = chart.Chart.NONE #PlanetTransiting
		self.pltretr = Transit.NONE
		self.obj = chart.Chart.NONE #Radix object (Planet, Asc, MC), sign change, antiscion or Lots
		self.objretr = Transit.NONE
		self.objtype = chart.Chart.NONE
		self.aspect = chart.Chart.NONE
		self.house = chart.Chart.NONE
		self.day = chart.Chart.NONE
		self.time = 0.0


class Transits:
	NONE = -1

	HOUR = 0
	MINUTE = 1
	SECOND = 2
	OVER = 3

	CIRCLE = 360.0
	OFFSET = 20.0 # arbitrary, greater then the Moon's speed

	def __init__(self):
		self.transits = []
		self.flags = Transits.NONE


	def month(self, year, month, chrt, pl = -1, pos = None):
		self.flags = astronomy.SEFLG_SPEED+astronomy.SEFLG_SWIEPH
		if (chrt.options.topocentric):
			self.flags += astronomy.SEFLG_TOPOCTR

		lastday = 1
		for day in range(1, 31):
			valid = util.checkDate(year, month, day)
			if (valid):
				lastday = day

				valid = util.checkDate(year, month, day+1)
				if (valid):
					lastday = day+1
					self.day(year, month, day, chrt, pl, pos)
				else:
					break
			else:
				break

		#lastday in month-first day in next month
		time1 = chtime.Time(year, month, lastday, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
		
		year, month = util.incrMonth(year, month)
		time2 = chtime.Time(year, month, 1, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)

		cnt = len(self.transits)

		if (pl == Transits.NONE):
			self.cycle(time1, chrt, time2)
		else:
			self.cycleplanet(time1, chrt, time2, pl, pos)

		self.order(cnt)

#		self.printTransits(self.transits)


	def day(self, year, month, day, chrt, pl = -1, pos = None):
		if (self.flags == Transits.NONE):
			self.flags = astronomy.SEFLG_SPEED+astronomy.SEFLG_SWIEPH
			if (chrt.options.topocentric):
				self.flags += astronomy.SEFLG_TOPOCTR

		time1 = chtime.Time(year, month, day, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
		time2 = chtime.Time(year, month, day+1, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
				
		cnt = len(self.transits)
		if (pl == Transits.NONE):
			self.cycle(time1, chrt, time2)
		else:
			self.cycleplanet(time1, chrt, time2, pl, pos)

		self.order(cnt)


	def order(self, cnt):
		if (len(self.transits) > cnt+1):
			beg = cnt
			for cyc in range(len(self.transits)-beg+1):
				for i in range(beg, len(self.transits)-1):
					if (self.transits[i].time > self.transits[i+1].time):
						tr = self.transits[i]
						self.transits[i] = self.transits[i+1]
						self.transits[i+1] = tr		


	def cycle(self, time1, chrt, time2):
		for j in range (planets.Planets.PLANETS_NUM-1): #Skip Moon
			planet1 = planet.Planet(time1.jd, j, self.flags)
			planet2 = planet.Planet(time2.jd, j, self.flags)

			for a in range(len(chart.Chart.Aspects)):
				for l in range(2):
					if (l == 1 and (a == chart.Chart.CONIUNCTIO or a == chart.Chart.OPPOSITIO)):
						continue
					for k in range (planets.Planets.PLANETS_NUM):
						lon = chrt.planets.planets[k].data[planet.Planet.LON]
						if (l == 0):
							lon += chart.Chart.Aspects[a]
							if (lon > 360.0):
								lon -= 360.0
						else:
							lon -= chart.Chart.Aspects[a]
							if (lon < 0.0):
								lon += 360.0
					
						tr = self.get(planet1, planet2, time1, chrt, lon, j, k, a, Transits.HOUR, Transit.PLANET)
						if (tr != None):
							self.transits.append(tr)

					#ascmc
					for h in range(2):
						lon = chrt.houses.ascmc[h][houses.Houses.LON]
						if (l == 0):
							lon += chart.Chart.Aspects[a]
							if (lon > 360.0):
								lon -= 360.0
						else:
							lon -= chart.Chart.Aspects[a]
							if (lon < 0.0):
								lon += 360.0

						tr = self.get(planet1, planet2, time1, chrt, lon, j, h, a, Transits.HOUR, Transit.ASCMC)
						if (tr != None):
							self.transits.append(tr)						

			#signs
			for s in range(len(chart.Chart.Signs)):
				lona = chart.Chart.Signs[s]
				if (chrt.options.ayanamsa != 0):
					lona += chrt.ayanamsa
					lona = util.normalize(lona)

				tr = self.get(planet1, planet2, time1, chrt, lona, j, 0, 0, Transits.HOUR, Transit.SIGN)
				if (tr != None):
					self.transits.append(tr)													

			#Antiscia
			for p in range (planets.Planets.PLANETS_NUM):
				lona = chrt.antis.plslons[p]

				tr = self.get(planet1, planet2, time1, chrt, lona, j, p, chart.Chart.CONIUNCTIO, Transits.HOUR, Transit.ANTISCION)
				if (tr != None):
					self.transits.append(tr)													

			#Lots
			for l in range(lots.Lots.LOTS_NUM):
				if (chrt.options.lots[l]):
					for a in range(len(chart.Chart.Aspects)):
						for d in range(2):		#direction of aspect
							if (d == 1 and (a == chart.Chart.CONIUNCTIO or a == chart.Chart.OPPOSITIO)):
								continue

							lonlot = chrt.lots.data[l]
							if (d == 0):
								lonlot += chart.Chart.Aspects[a]
								if (lonlot > 360.0):
									lonlot -= 360.0
							else:
								lonlot -= chart.Chart.Aspects[a]
								if (lonlot < 0.0):
									lonlot += 360.0
							tr = self.get(planet1, planet2, time1, chrt, lonlot, j, l, a, Transits.HOUR, Transit.LOT)
							if (tr != None):
								self.transits.append(tr)

			#Syzygy
			if (chrt.options.syzygy):
				for a in range(len(chart.Chart.Aspects)):
					for d in range(2):		#direction of aspect
						if (d == 1 and (a == chart.Chart.CONIUNCTIO or a == chart.Chart.OPPOSITIO)):
							continue

						lonsyz = chrt.syzygy.lon
						if (d == 0):
							lonsyz += chart.Chart.Aspects[a]
							if (lonsyz > 360.0):
								lonsyz -= 360.0
						else:
							lonsyz -= chart.Chart.Aspects[a]
							if (lonsyz < 0.0):
								lonsyz += 360.0
						tr = self.get(planet1, planet2, time1, chrt, lonsyz, j, 0, a, Transits.HOUR, Transit.SYZYGY)
						if (tr != None):
							self.transits.append(tr)


	def cycleplanet(self, time1, chrt, time2, pl, pos):
		planet1 = planet.Planet(time1.jd, pl, self.flags)
		planet2 = planet.Planet(time2.jd, pl, self.flags)

		lon = chrt.planets.planets[pl].data[planet.Planet.LON] #####

		if (pl != Transits.NONE and pos != None):
			lon = pos
		tr = self.get(planet1, planet2, time1, chrt, lon, pl, pl, chart.Chart.CONIUNCTIO, Transits.HOUR, Transit.PLANET)
		if (tr != None):
			self.transits.append(tr)


	def get(self, planet1, planet2, time1, chrt, lon, j, k, a, unit, typ):
		if (self.check(planet1, planet2, lon)):
			fr = 0
			to = 60
			if (unit == Transits.HOUR):
				fr = 0
				to = 24

			for val in range(fr, to):
				time = None
				if (unit == Transits.HOUR):
					time1 = chtime.Time(time1.year, time1.month, time1.day, val, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
					time2 = None
					if (val+1 < to):
						time2 = chtime.Time(time1.year, time1.month, time1.day, val+1, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
					else:
						y, m, d = util.incrDay(time1.year, time1.month, time1.day)
						time2 = chtime.Time(y, m, d, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
				elif (unit == Transits.MINUTE):
					time1 = chtime.Time(time1.year, time1.month, time1.day, time1.hour, val, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
					time2 = None
					if (val+1 < to):
						time2 = chtime.Time(time1.year, time1.month, time1.day, time1.hour, val+1, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
					else:
						if (time1.hour+1 < 24):
							time2 = chtime.Time(time1.year, time1.month, time1.day, time1.hour+1, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
						else:
							y, m, d = util.incrDay(time1.year, time1.month, time1.day)
							time2 = chtime.Time(y, m, d, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
				elif (unit == Transits.SECOND):
					time1 = chtime.Time(time1.year, time1.month, time1.day, time1.hour, time1.minute, val, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
					time2 = None
					if (val+1 < to):
						time2 = chtime.Time(time1.year, time1.month, time1.day, time1.hour, time1.minute, val+1, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
					else:
						if (time1.minute+1 < 60):
							time2 = chtime.Time(time1.year, time1.month, time1.day, time1.hour, time1.minute+1, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
						else:
							if (time1.hour+1 < 24):
								time2 = chtime.Time(time1.year, time1.month, time1.day, time1.hour+1, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
							else:
								y, m, d = util.incrDay(time1.year, time1.month, time1.day)
								time2 = chtime.Time(y, m, d, 0, 0, 0, False, chrt.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, chrt.place, False)
				else:
#					print 'unit > SECOND'
					return None	

				planet1 = planet.Planet(time1.jd, j, self.flags)
				planet2 = planet.Planet(time2.jd, j, self.flags)
	
				if (self.check(planet1, planet2, lon)):
					un = Transits.OVER
					if (unit == Transits.HOUR):
						un = Transits.MINUTE
					if (unit == Transits.MINUTE):
						un = Transits.SECOND
				
					if (un != Transits.OVER):
						return self.get(planet1, planet2, time1, chrt, lon, j, k, a, un, typ)
					else:
						tr = Transit()
						tr.plt = j
						tr.objtype = typ
						if (typ == Transit.SIGN):
							tr.obj = int(lon/chart.Chart.SIGN_DEG)
						else:
							tr.obj = k

						if (planet1.data[planet.Planet.DIST] < 0.0):
							tr.pltretr = Transit.RETR
						elif (planet1.data[planet.Planet.DIST] == 0.0):
							tr.pltretr = Transit.STAT
						if (typ == Transit.PLANET):
							if (chrt.planets.planets[k].data[planet.Planet.SPLON] < 0.0):
								tr.objretr = Transit.RETR
							elif (chrt.planets.planets[k].data[planet.Planet.SPLON] == 0.0):
								tr.objretr = Transit.STAT

						if typ != Transit.SIGN:
							tr.aspect = a
						tr.house = 0 #chrt.houses.getHousePos(planet1.data[planet.Planet.LON], chrt.options)
						tr.day = time1.day
						tr.time = time1.time

						return tr
				
		return None


	def check(self, planet1, planet2, lon):
		#Handle 360-0 transitions(Pisces-Aries)
		if ((planet1.data[planet.Planet.LON] > Transits.CIRCLE-Transits.OFFSET and planet2.data[planet.Planet.LON] < Transits.OFFSET) or (planet2.data[planet.Planet.LON] > Transits.CIRCLE-Transits.OFFSET and planet1.data[planet.Planet.LON] < Transits.OFFSET)):
			if (planet1.data[planet.Planet.LON] > Transits.CIRCLE-Transits.OFFSET and planet2.data[planet.Planet.LON] < Transits.OFFSET):
				if (planet1.data[planet.Planet.LON] <= lon or planet2.data[planet.Planet.LON] > lon):
					return True
			if (planet2.data[planet.Planet.LON] > Transits.CIRCLE-Transits.OFFSET and planet1.data[planet.Planet.LON] < Transits.OFFSET):
				if (planet2.data[planet.Planet.LON] <= lon or planet1.data[planet.Planet.LON] > lon):
					return True
			return False

		#Handle normal case
		if ((planet1.data[planet.Planet.LON] <= lon and planet2.data[planet.Planet.LON] > lon) or (planet2.data[planet.Planet.LON] <= lon and planet1.data[planet.Planet.LON] > lon)):
			return True

		return False


	def printTransits(self, ls):
		for tr in ls:
			d, m, s = util.decToDeg(tr.time)
			if (tr.objtype == Transit.PLANET):
				print ('day %d: %s %s %s house:%d %d:%02d:%02d' % (tr.day, texts.planets[tr.plt], texts.aspects[tr.aspect], texts.planets[tr.obj], tr.house+1, d, m, s))
			elif (tr.objtype == Transit.ASCMC):
				print ('day %d: %s %s %s house:%d %d:%02d:%02d' % (tr.day, texts.planets[tr.plt], texts.aspects[tr.aspect], texts.ascmc[tr.obj], tr.house+1, d, m, s))
			else:
				print ('day %d: %s %s house:%d %d:%02d:%02d' % (tr.day, texts.planets[tr.plt], txts.signs[tr.obj], tr.house+1, d, m, s))






