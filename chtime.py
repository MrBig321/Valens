import datetime
import astronomy
import plhours
import util


# if long is 'E' or/and lat is 'S' -> negate value

class Time:
	"""Time of Birth"""

	#calendars
	GREGORIAN = 0
	JULIAN = 1

	#times
	ZONE, GREENWICH, LOCALMEAN, LOCALAPPARENT = range(0, 4)
	
	HOURSPERDAY = 24.0

	def __init__(self, year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, dst, place, full = True): #zt is zonetime, zh is zonehour, zm is zoneminute
		self.year = year
		self.month = month
		self.day = day
		self.origyear = year
		self.origmonth = month
		self.origday = day
		self.hour = hour
		self.minute = minute
		self.second = second
		self.bc = bc
		self.cal = cal
		self.zt = zt
		self.plus = plus
		self.zh = zh
		self.zm = zm
		self.dst = dst

		self.time = hour+minute/60.0+second/3600.0

		self.oyear, self.omonth, self.oday, self.ohour, self.omin, self.osec = year, month, day, hour, minute, second #orig
		self.dyear, self.dmonth, self.dday, self.dhour, self.dmin, self.dsec = year, month, day, hour, minute, second
		if (self.dst):
			self.time -= 1.0
			self.dhour -= 1
		#check dst underflow
		if (self.time < 0.0):
			self.time += Time.HOURSPERDAY
			self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)
			self.dhour += int(Time.HOURSPERDAY)
			self.dyear, self.dmonth, self.dday = self.year, self.month, self.day
			
		if (zt == Time.ZONE):#ZONE
			ztime = zh+zm/60.0
			if (self.plus):
				self.time-=ztime
			else:
				self.time+=ztime
		elif (zt == Time.LOCALMEAN):#LMT
			t = (place.deglon+place.minlon/60.0)*4.0 #long * 4min
			if (place.east):
				self.time-=t/60.0
			else:
				self.time+=t/60.0	

		if (bc):
			self.year = 1-self.year

		#check over/underflow
		if (self.time >= Time.HOURSPERDAY):
			self.time -= Time.HOURSPERDAY
			self.year, self.month, self.day = util.incrDay(self.year, self.month, self.day)
		elif (self.time < 0.0):
			self.time += Time.HOURSPERDAY
			self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)

		calflag = astronomy.SE_GREG_CAL
		if (self.cal == Time.JULIAN):
			calflag = astronomy.SE_JUL_CAL
		self.jd = astronomy.swe_julday(self.year, self.month, self.day, self.time, calflag)
		if (zt == Time.LOCALAPPARENT):#LAT
			ret, te, serr = astronomy.swe_time_equ(self.jd)
			self.jd += te #LMT
			#Back to h,m,s(self.time) from julianday fromat
			self.year, self.month, self.day, self.time = astronomy.swe_revjul(self.jd, calflag)
			#To GMT
			t = (place.deglon+place.minlon/60.0)*4.0 #long * 4min
			if (place.east):
				self.time-=t/60.0
			else:
				self.time+=t/60.0	

			#check over/underflow
			if (self.time >= Time.HOURSPERDAY):
				self.time -= Time.HOURSPERDAY
				self.year, self.month, self.day = util.incrDay(self.year, self.month, self.day)
			elif (self.time < 0.0):
				self.time += Time.HOURSPERDAY
				self.year, self.month, self.day = util.decrDay(self.year, self.month, self.day)

			#GMT in JD (julianday)
			self.jd = astronomy.swe_julday(self.year, self.month, self.day, self.time, calflag)
		
		self.sidTime = astronomy.swe_sidtime(self.jd) #GMT

		self.ph = None
		if (full):
			self.calcPHs(place)


	def calcPHs(self, place):
		#Planetary day/hour calculation
		weekday = datetime.datetime(self.dyear, self.dmonth, self.dday, self.dhour, self.dmin, self.dsec).weekday()#only dst was subtracted
		lon = place.deglon+place.minlon/60.0
		if (not place.east):
			lon *= -1
		lat = place.deglat+place.minlat/60.0
		if (not place.north):
			lat *= -1
			
		self.ph = plhours.PlanetaryHours(lon, lat, place.altitude, weekday, self.jd)

		




