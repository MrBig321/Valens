import math
import astronomy
import chtime
import chart
import planets
import texts
import util


class RiseSet:
	"""Computes Rise/Set times (for the birthday)"""

	RISE, MC, SET, IC = range(0, 4)

	Angles = [astronomy.SE_CALC_RISE, astronomy.SE_CALC_MTRANSIT , astronomy.SE_CALC_SET,  astronomy.SE_CALC_ITRANSIT]

	def __init__(self, jd, cal, lon, lat, alt, pls):
		self.jd = jd
		self.cal = cal
		self.lon = lon
		self.lat = lat
		self.alt = alt

		self.calflag = astronomy.SE_GREG_CAL
		if (self.cal == chtime.Time.JULIAN):
			self.calflag = astronomy.SE_JUL_CAL

#		self.offs = lon*4.0/1440.0 #lon*4 will be in minutes. after /60*24, it will be in days, suitable for addition to julian-day

		self.times = []

		self.calcTimes()
	
#		self.printRiseSet(pls)


	def calcTimes(self):
		#the date we get from julianday is the same as year, month day in Time-class but we didn't pass it to the init function.
		oyear, omonth, oday, otim = astronomy.swe_revjul(self.jd, self.calflag)

		for i in range(planets.Planets.PLANETS_NUM):#Nodes are excluded
			ar = []

			#Rise
			ret, JDRise, serr = astronomy.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.RISE], self.lon, self.lat, self.alt, 0.0, 10.0)
			tyear, tmonth, tday, ttim = astronomy.swe_revjul(JDRise, self.calflag)
			if (oyear != tyear or omonth != tmonth or oday != tday):
				ret, JDRise, serr = astronomy.swe_rise_trans(self.jd-1.0, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.RISE], self.lon, self.lat, self.alt, 0.0, 10.0)

			#MC
			ret, JDMC, serr = astronomy.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.MC], self.lon, self.lat, self.alt, 0.0, 10.0)
			tyear, tmonth, tday, ttim = astronomy.swe_revjul(JDMC, self.calflag)
			if (oyear != tyear or omonth != tmonth or oday != tday):
				ret, JDMC, serr = astronomy.swe_rise_trans(self.jd-1.0, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.MC], self.lon, self.lat, self.alt, 0.0, 10.0)

			#Set
			ret, JDSet, serr = astronomy.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.SET], self.lon, self.lat, self.alt, 0.0, 10.0)
			tyear, tmonth, tday, ttim = astronomy.swe_revjul(JDSet, self.calflag)
			if (oyear != tyear or omonth != tmonth or oday != tday):
				ret, JDSet, serr = astronomy.swe_rise_trans(self.jd-1.0, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.SET], self.lon, self.lat, self.alt, 0.0, 10.0)

			#IC
			ret, JDIC, serr = astronomy.swe_rise_trans(self.jd, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.IC], self.lon, self.lat, self.alt, 0.0, 10.0)
			tyear, tmonth, tday, ttim = astronomy.swe_revjul(JDIC, self.calflag)
			if (oyear != tyear or omonth != tmonth or oday != tday):
				ret, JDIC, serr = astronomy.swe_rise_trans(self.jd-1.0, util.mapChaldeanToModern(i), "", astronomy.SEFLG_SWIEPH, RiseSet.Angles[RiseSet.IC], self.lon, self.lat, self.alt, 0.0, 10.0)

			#From GMT to Local
#			JDRise += self.offs
			year, month, day, hr = astronomy.swe_revjul(JDRise, self.calflag)
			ar.append(hr)

#			JDMC += self.offs
			year, month, day, hr = astronomy.swe_revjul(JDMC, self.calflag)
			ar.append(hr)

#			JDSet += self.offs
			year, month, day, hr = astronomy.swe_revjul(JDSet, self.calflag)
			ar.append(hr)

#			JDIC += self.offs
			year, month, day, hr = astronomy.swe_revjul(JDIC, self.calflag)
			ar.append(hr)

			self.times.append(ar)


	def printRiseSet(self, pls):
		numangles = len(RiseSet.Angles)
		txt = [texts.txtsriseset['Rise'], texts.txtsriseset['MC'], texts.txtsriseset['Set'], texts.txtsriseset['IC']]
		print('')
		print('Rise/Set times:')
		for i in range(planets.Planets.PLANETS_NUM):#Nodes are excluded
			for angle in range(numangles):
				h,m,s = util.decToDeg(self.times[i][angle])
				print("%s: %s: %02d:%02d:%02d" % (pls.planets[i].name, txt[angle], h, m, s))



