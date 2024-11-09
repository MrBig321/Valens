import math
import threading
import queue
import astronomy
import chtime
import planet
import planets
import rangechecker
import util


class FindTime(threading.Thread):
	NONE = -1

	HOUR = 0
	MINUTE = 1
	SECOND = 2
	OVER = 3

	CIRCLE = 360.0
	OFFSET = 20.0 # arbitrary (just to check if a planet is close to 0 Aries in case the other end of the region is close to the 359 Pisces (on the other side))

	YEAR, MONTH, DAY, TIME, JD = range(5)

	#From FindTimeDlg
	LON = 0
	RETR = 1

	MIN = 0
	SEC = 1
	RET = 2

	USEAPPROX = 0
	APPROXDEG = 1
	APPROXMIN = 2
	APPROXSEC = 3

	YEARS = 50


	def __init__(self, bc, ftdata, ftdatause, ftdataapprox, abort, queueft, queueyear):
		threading.Thread.__init__(self)
		self.bc = bc
		self.ftdata = ftdata
		self.ftdatause = ftdatause
		self.ftdataapprox = ftdataapprox
		self.abort = abort
		self.queueft = queueft
		self.queueyear = queueyear

		self.flags = astronomy.SEFLG_SPEED+astronomy.SEFLG_SWIEPH


	def run(self):
		checker = rangechecker.RangeChecker()
		rnge = checker.getRange()

		y = 1973 #year doesn't matter
		m = 3
		d = 21
		for i in range(int(self.ftdata[planets.Planets.SUN][FindTime.LON])):
			y, m ,d = util.incrDay(y, m ,d)

		#Because the Sun's velocity is not exactly one degree per day. It is variable. The targetdate (from Sun's long) won't exactly be in the middle of the range
		tim = chtime.Time(y, m, d, 0, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
		tmpSun = planet.Planet(tim.jd, planets.Planets.SUN, self.flags)
		lonSun = tmpSun.data[planet.Planet.LON]
		lontofind = self.ftdata[planets.Planets.SUN][FindTime.LON]

		if (lonSun > FindTime.CIRCLE-FindTime.OFFSET and lontofind < FindTime.OFFSET):
			lontofind += FindTime.CIRCLE
		if (lontofind > FindTime.CIRCLE-FindTime.OFFSET and lonSun < FindTime.OFFSET):
			lonSun += FindTime.CIRCLE

		diff = int(math.fabs(int(lonSun)-int(lontofind)))
		if (int(self.ftdata[planets.Planets.SUN][FindTime.LON]) < int(lonSun)):
			for i in range(diff):
				y, m, d = util.decrDay(y, m, d)
		else:
			for i in range(diff):
				y, m, d = util.incrDay(y, m, d)

		ybeg, mbeg, dbeg = y, m, d
		yend, mend, dend = y, m, d
		DATEOFFS = 7
		#adjust range
		for i in range(DATEOFFS):
			ybeg, mbeg, dbeg = util.decrDay(ybeg, mbeg ,dbeg)
			yend, mend, dend = util.incrDay(yend, mend ,dend)
			
		tfnd = (1, 1, 1, 1.0, 1.0)
		y = 1; m = mbeg; d = dbeg
		while (y < rnge):
			if (self.abort.isAborting()):
				return

			fnd = self.day(y, m, d, planets.Planets.SUN, self.ftdata[planets.Planets.SUN][FindTime.LON])
			if (fnd != None):
				found = True
				for i in range(planets.Planets.PLANETS_NUM):
					if (i != planets.Planets.SUN):
						tfnd = self.day(y, m, d, i, self.ftdata[i][FindTime.LON])
						if (tfnd == None):
							found = False
							break

				if (found):
					try:
						self.queueft.put_nowait(tfnd)
					except queue.Full:
						pass

			yt = y
			if (m == mend and d == dend):
				y += 1
				m = mbeg
				d = dbeg
			else:
				y, m, d = util.incrDay(y, m, d)

			if (yt != y and yt%FindTime.YEARS == 0):
				try:
					self.queueyear.put_nowait(yt)
				except queue.Full:
					pass

		self.abort.aborting()


	def day(self, year, month, day, pl, pos):
		y, m, d = util.incrDay(year, month, day)
		time1 = chtime.Time(year, month, day, 0, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
		time2 = chtime.Time(y, m, d, 0, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
				
		return self.cycleplanet(time1, time2, pl, pos)


	def cycleplanet(self, time1, time2, pl, pos):
		planet1 = planet.Planet(time1.jd, pl, self.flags)
		planet2 = planet.Planet(time2.jd, pl, self.flags)

		if (self.check(planet1, planet2, pos)):
			return self.get(planet1, planet2, time1, pos, pl, FindTime.HOUR)

		return None


	def get(self, planet1, planet2, time1, lon, pl, unit):
		if (self.check(planet1, planet2, lon)):
			fr = 0
			to = 60
			if (unit == FindTime.HOUR):
				fr = 0
				to = 24

			for val in range(fr, to):
				time = None
				if (unit == FindTime.HOUR):
					time1 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, val, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
					time2 = None
					if (val+1 < to):
						time2 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, val+1, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
					else:
						y, m, d = util.incrDay(int(math.fabs(time1.year)), time1.month, time1.day)
						time2 = chtime.Time(y, m, d, 0, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
				elif (unit == FindTime.MINUTE):
					time1 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, val, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
					time2 = None
					if (val+1 < to):
						time2 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, val+1, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
					else:
						if (time1.hour+1 < 24):
							time2 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour+1, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
						else:
							y, m, d = util.incrDay(int(math.fabs(time1.year)), time1.month, time1.day)
							time2 = chtime.Time(y, m, d, 0, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
				elif (unit == FindTime.SECOND):
					time1 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, time1.minute, val, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
					time2 = None
					if (val+1 < to):
						time2 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, time1.minute, val+1, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
					else:
						if (time1.minute+1 < 60):
							time2 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour, time1.minute+1, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
						else:
							if (time1.hour+1 < 24):
								time2 = chtime.Time(int(math.fabs(time1.year)), time1.month, time1.day, time1.hour+1, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
							else:
								y, m, d = util.incrDay(int(math.fabs(time1.year)), time1.month, time1.day)
								time2 = chtime.Time(y, m, d, 0, 0, 0, self.bc, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
				else:
#					print 'unit > SECOND'
					return None	

				planet1 = planet.Planet(time1.jd, pl, self.flags)
				planet2 = planet.Planet(time2.jd, pl, self.flags)
	
				if (self.check(planet1, planet2, lon)):
					un = FindTime.OVER
					if (unit == FindTime.HOUR):
						un = FindTime.MINUTE
					if (unit == FindTime.MINUTE):
						un = FindTime.SECOND
				
					if (un != FindTime.OVER):
						return self.get(planet1, planet2, time1, lon, pl, un)
					else:
						if (self.ftdatause[FindTime.RET]):
							#check retrograde
							if ((planet1.data[planet.Planet.SPLON] <= 0.0 and self.ftdata[pl][FindTime.RETR]) or (planet1.data[planet.Planet.SPLON] > 0.0 and not self.ftdata[pl][FindTime.RETR])):
								return (int(math.fabs(time1.year)), time1.month, time1.day, time1.time, time1.jd)

							return None

						return (int(math.fabs(time1.year)), time1.month, time1.day, time1.time, time1.jd)
				
		return None


	def check(self, planet1, planet2, lon):
		#Handle 360-0 transitions(Pisces-Aries) and normal case

		y1, m1, s1 = util.decToDeg(planet1.data[planet.Planet.LON])
		y2, m2, s2 = util.decToDeg(planet2.data[planet.Planet.LON])

		if (self.ftdataapprox[FindTime.USEAPPROX] and (self.ftdataapprox[FindTime.APPROXDEG] != 0 or self.ftdataapprox[FindTime.APPROXMIN] != 0 or self.ftdataapprox[FindTime.APPROXSEC] != 0)):
			lon1 = float(y1)+float(m1)/60.0+float(s1)/3600.0
			lon2 = float(y2)+float(m2)/60.0+float(s2)/3600.0

			if (lon2 < lon1):
				tlon = lon1
				lon1 = lon2
				lon2 = tlon

			approxval = self.ftdataapprox[FindTime.APPROXDEG]+self.ftdataapprox[FindTime.APPROXMIN]/60.0+self.ftdataapprox[FindTime.APPROXSEC]/3600.0
			lona = util.normalize(lon-approxval)
			lonb = util.normalize(lon+approxval)

			if (lonb < lona):
				tlon = lona
				lona = lonb
				lonb = tlon

			if ((lon2 > FindTime.CIRCLE-FindTime.OFFSET and lon1 < FindTime.OFFSET) and (lonb > FindTime.CIRCLE-FindTime.OFFSET and lona < FindTime.OFFSET)):
				return True

			if ((lon2 > FindTime.CIRCLE-FindTime.OFFSET and lon1 < FindTime.OFFSET) and (lonb > FindTime.CIRCLE-FindTime.OFFSET and lona > FindTime.CIRCLE-FindTime.OFFSET)):
				if (lon2 <= lona):
					return True

				return False

			if ((lonb > FindTime.CIRCLE-FindTime.OFFSET and lona < FindTime.OFFSET) and (lon2 > FindTime.CIRCLE-FindTime.OFFSET and lon1 > FindTime.CIRCLE-FindTime.OFFSET)):
				if (lonb <= lon1):
					return True

				return False

			if ((lonb < FindTime.OFFSET and lona < FindTime.OFFSET) and (lon2 > FindTime.CIRCLE-FindTime.OFFSET and lon1 < FindTime.OFFSET)):
				if (lonb <= lon1):
					return True

				return False

			if ((lonb > FindTime.CIRCLE-FindTime.OFFSET and lona < FindTime.OFFSET) and (lon2 < FindTime.OFFSET and lon1 < FindTime.OFFSET)):
				if (lon2 <= lona):
					return True

				return False

			if ((lonb > FindTime.CIRCLE-FindTime.OFFSET and lona < FindTime.OFFSET) and (lon2 > FindTime.OFFSET and lon2 < FindTime.CIRCLE-FindTime.OFFSET and lon1 > FindTime.OFFSET and lon1 < FindTime.CIRCLE-FindTime.OFFSET) or (lon2 > FindTime.CIRCLE-FindTime.OFFSET and lon1 < FindTime.OFFSET) and (lonb > FindTime.OFFSET and lonb < FindTime.CIRCLE-FindTime.OFFSET and lona > FindTime.OFFSET and lona < FindTime.CIRCLE-FindTime.OFFSET)):
				return False

			#Handle normal case
			if ((lon1 <= lona and lon2 >= lona) or (lona <= lon1 and lonb >= lon1)):
				return True

		else:
			lon1 = lon2 = 0.0
			if (self.ftdatause[FindTime.MIN] and self.ftdatause[FindTime.SEC]):
				lon1 = float(y1)+float(m1)/60.0+float(s1)/3600.0
				lon2 = float(y2)+float(m2)/60.0+float(s2)/3600.0
			else:
				if (not self.ftdatause[FindTime.SEC]):
					lon1 = float(y1)+float(m1)/60.0
					lon2 = float(y2)+float(m2)/60.0
				if (not self.ftdatause[FindTime.MIN]):
					lon1 = float(y1)
					lon2 = float(y2)

			if (lon2 < lon1):
				tlon = lon1
				lon1 = lon2
				lon2 = tlon

			if (lon2 > FindTime.CIRCLE-FindTime.OFFSET and lon1 < FindTime.OFFSET):
				if (lon2 <= lon or lon1 > lon):
					return True
				return False

			#Handle normal case
			if (lon1 <= lon and lon2 >= lon):
				return True

		return False



