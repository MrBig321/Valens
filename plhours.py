import astronomy
import chtime
import texts
import util


class PlanetaryHours:
	#From sunrise!! (till next sunrise)
	#Monday: Moon, Saturnus, Jupiter, Mars, Sun, Venus, Mercury, Moon...
	#Sunday: Sun, Venus, Mercury, Moon, Saturnus, Jupiter, Mars, Sun...
	PHs = ((6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1),
			(2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4),
			(5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0),
			(1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3),
			(4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6),
			(0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2),
			(3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5, 6, 0, 1, 2, 3, 4, 5))


	def __init__(self, lon, lat, altitude, weekday, jd):
		self.risetime = None
		self.settime = None
		self.hrlen = None
		self.daytime = None

		self.weekday = weekday

		#lon, lat, height, atmpress, celsius
		#in GMT, searches after jd!
		ret, risetime, serr = astronomy.swe_rise_trans(jd, astronomy.SE_SUN, '', astronomy.SEFLG_SWIEPH, astronomy.SE_CALC_RISE, lon, lat, float(altitude), 0.0, 10.0)
#		self.logCalc(risetime)#
		ret, settime, serr = astronomy.swe_rise_trans(jd, astronomy.SE_SUN, '', astronomy.SEFLG_SWIEPH, astronomy.SE_CALC_SET, lon, lat, float(altitude), 0.0, 10.0)
#		self.logCalc(settime)#

		#swe_rise_trans calculates only forward!!
		offs = lon*4.0/1440.0
		hr = 0
		HOURSPERHALFDAY = 12.0
		if (risetime > settime): # daytime
			self.daytime = True
#			print 'daytime'#
			ret, self.risetime, serr = astronomy.swe_rise_trans(jd-1.0, astronomy.SE_SUN, '', astronomy.SEFLG_SWIEPH, astronomy.SE_CALC_RISE, lon, lat, float(altitude), 0.0, 10.0)
#			self.logCalc(risetime)#
			ret, self.settime, serr = astronomy.swe_rise_trans(jd, astronomy.SE_SUN, '', astronomy.SEFLG_SWIEPH, astronomy.SE_CALC_SET, lon, lat, float(altitude), 0.0, 10.0)

			#From GMT to Local
			self.risetime += offs
			self.settime += offs

#			self.logCalc(settime)#
			self.hrlen = (self.settime-self.risetime)/HOURSPERHALFDAY #hrlen(hour-length) is in days
			for i in range(int(HOURSPERHALFDAY)):
				if (jd+offs < self.risetime+self.hrlen*(i+1)):
					hr = i
					break
		else:# nighttime
			self.daytime = False
#			print 'nightime'#
			ret, self.risetime, serr = astronomy.swe_rise_trans(jd, astronomy.SE_SUN, '', astronomy.SEFLG_SWIEPH, astronomy.SE_CALC_RISE, lon, lat, float(altitude), 0.0, 10.0)
#			self.logCalc(risetime)#
			ret, self.settime, serr = astronomy.swe_rise_trans(jd-1.0, astronomy.SE_SUN, '', astronomy.SEFLG_SWIEPH, astronomy.SE_CALC_SET, lon, lat, float(altitude), 0.0, 10.0)
#			self.logCalc(settime)#

			#From GMT to Local
			self.risetime += offs
			self.settime += offs

			#Is the local birthtime greater than midnight? If so => decrement day because a planetary day is from sunrise to sunrise
			if (jd+offs > int(jd+offs)+0.5):
				self.weekday = util.getPrevDay(self.weekday)

			self.hrlen = (self.risetime-self.settime)/HOURSPERHALFDAY
			for i in range(int(HOURSPERHALFDAY)):
				if (jd+offs < self.settime+self.hrlen*(i+1)):
					hr = i+int(HOURSPERHALFDAY)
					break

		self.planetaryhour = PlanetaryHours.PHs[self.weekday][hr]#planetary day begins from sunrise(not from 0 hour and Planetary hours are not equal!!)

#		self.printDayHour()


	def revTime(self, tjd, cal):
		calflag = astronomy.SE_GREG_CAL
		if (cal == chtime.Time.JULIAN):
			calflag = astronomy.SE_JUL_CAL
		jy, jm, jd, jh = astronomy.swe_revjul(tjd, calflag)
		d, m, s = util.decToDeg(jh)
		return (d, m, s)

		
	def logCalc(self, tjd):
		#in GMT!
		jy, jm, jd, jh = astronomy.swe_revjul(tjd, 1)
		d, m, s = util.decToDeg(jh)
		print('GMT: %d.%d.%d %d:%d:%d' % (jy,jm,jd, d, m, s))


	def printDayHour(self):
		print('')
		print('Planetary Day and Hour:')
		print('Day: %s Hour: %s' % (pls[PlanetaryHours.PHs[self.weekday][0]], texts.planets[self.planetaryhour]))




