import astronomy
import chtime
import chart
import planet
import planets
import util


class Syzygy:

	def __init__(self, chrt):
		self.time = chrt.time
		self.lon = chrt.planets.planets[planets.Planets.MOON].data[planet.Planet.LON]

		self.flags = astronomy.SEFLG_SPEED+astronomy.SEFLG_SWIEPH

		if (not chrt.time.bc):
			lonsun = chrt.planets.planets[planets.Planets.SUN].data[planet.Planet.LON]
			lonmoon = chrt.planets.planets[planets.Planets.MOON].data[planet.Planet.LON]

			d, m, s = util.decToDeg(lonsun)
			lonsun = d+m/60.0+s/3600.0
			d, m, s = util.decToDeg(lonmoon)
			lonmoon = d+m/60.0+s/3600.0

			diff = lonmoon-lonsun
			self.newmoon, self.ready = self.isNewMoon(diff)

			if (not self.ready):
				ok, self.time, self.ready = self.getDateHour(self.time, chrt.place, self.newmoon)
				if (not self.ready):
					ok, self.time, self.ready = self.getDateMinute(self.time, chrt.place, self.newmoon)
					if (not self.ready):
						ok, self.time, self.ready = self.getDateSecond(self.time, chrt.place, self.newmoon)

			self.time.calcPHs(chrt.place)

			moon = planet.Planet(self.time.jd, planets.Planets.MOON, self.flags)
			self.lon = moon.data[planet.Planet.LON]

#		self.printSyzygy()


	def isNewMoon(self, diff):
		newmoon = True
		ready = False

		if (diff == 0.0):
			newmoon = True
			ready = True
		elif (diff == 180.0 or diff == -180.0):
			newmoon = False
			ready = True
		elif (diff < 0.0):
			if (diff < -180.0):
				newmoon = True
			else:
				newmoon = False
		elif (diff > 0.0):
			if (diff > 180.0):
				newmoon = False
			else:
				newmoon = True

		return newmoon, ready


	def getDateHour(self, tim, place, newmoonorig):
		while (True):
			h, m, s = util.decToDeg(tim.time) 
			y, mo, d = tim.year, tim.month, tim.day
			h -= 1
			if (h < 0):
				h = 23	
				y, mo, d = util.decrDay(y, mo, d)
				if (y == 0):
					y = 1
					tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)
					return True, tim, True

			tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)

			sun = planet.Planet(tim.jd, planets.Planets.SUN, self.flags)
			moon = planet.Planet(tim.jd, planets.Planets.MOON, self.flags)
			lonsun = sun.data[planet.Planet.LON]
			lonmoon = moon.data[planet.Planet.LON]

			d, m, s = util.decToDeg(lonsun)
			lonsun = d+m/60.0+s/3600.0
			d, m, s = util.decToDeg(lonmoon)
			lonmoon = d+m/60.0+s/3600.0

			diff = lonmoon-lonsun
			newmoon, ready = self.isNewMoon(diff)
			if (newmoon != newmoonorig or ready):
				return True, tim, ready

		return False, tim


	def getDateMinute(self, tim, place, newmoonorig):
		h, m, s = util.decToDeg(tim.time) 
		y, mo, d = tim.year, tim.month, tim.day
		h += 1
		if (h > 23):
			h = 0	
			y, mo, d = util.incrDay(y, mo, d)

		tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)

		while (True):
			h, m, s = util.decToDeg(tim.time) 
			y, mo, d = tim.year, tim.month, tim.day
			y, mo, d, h, m = util.subtractMins(y, mo, d, h, m, 1)
			if (y == 0):
				y = 1
				tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)
				return True, tim, True

			tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)

			sun = planet.Planet(tim.jd, planets.Planets.SUN, self.flags)
			moon = planet.Planet(tim.jd, planets.Planets.MOON, self.flags)
			lonsun = sun.data[planet.Planet.LON]
			lonmoon = moon.data[planet.Planet.LON]

			d, m, s = util.decToDeg(lonsun)
			lonsun = d+m/60.0+s/3600.0
			d, m, s = util.decToDeg(lonmoon)
			lonmoon = d+m/60.0+s/3600.0

			diff = lonmoon-lonsun
			newmoon, ready = self.isNewMoon(diff)
			if (newmoon != newmoonorig or ready):
				return True, tim, ready

		return False, tim


	def getDateSecond(self, tim, place, newmoonorig):
		h, m, s = util.decToDeg(tim.time) 
		y, mo, d = tim.year, tim.month, tim.day
		y, mo, d, h, m = util.addMins(y, mo, d, h, m, 1)

		tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)

		while (True):
			h, m, s = util.decToDeg(tim.time) 
			y, mo, d = tim.year, tim.month, tim.day
			y, mo, d, h, m, s = util.subtractSecs(y, mo, d, h, m, s, 1)
			if (y == 0):
				y = 1
				tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)
				return True, tim, True

			tim = chtime.Time(y, mo, d, h, m, s, False, tim.cal, chtime.Time.GREENWICH, True, 0, 0, False, place, False)

			sun = planet.Planet(tim.jd, planets.Planets.SUN, self.flags)
			moon = planet.Planet(tim.jd, planets.Planets.MOON, self.flags)
			lonsun = sun.data[planet.Planet.LON]
			lonmoon = moon.data[planet.Planet.LON]

			d, m, s = util.decToDeg(lonsun)
			lonsun = d+m/60.0+s/3600.0
			d, m, s = util.decToDeg(lonmoon)
			lonmoon = d+m/60.0+s/3600.0

			diff = lonmoon-lonsun
			newmoon, ready = self.isNewMoon(diff)
			if (newmoon != newmoonorig or ready):
				return True, tim, ready

		return False, tim


	def printSyzygy(self):
		signs = ('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis')

		print ('')
		print ('Syzygy:')
		txt = ('Full Moon')
		if (self.newmoon):
			txt = ('New Moon')
		ye, mo, da = self.time.year, self.time.month, self.time.day
		h, m, s = util.decToDeg(self.time.time)
		si = int(self.lon/chart.Chart.SIGN_DEG)
		dd = int(self.lon%chart.Chart.SIGN_DEG)
		d, mi, se = util.decToDeg(self.lon)
		print ('%s %d.%02d.%02d %02d:%02d:%02d lon=%02d%s %02dm %02ds' % (txt, ye, mo, da, h, m, s, dd, signs[si], mi, se))




