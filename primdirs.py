import math
import threading
import queue
import datetime
import astronomy
import houses
import chart
import chtime
import planet
import planets
import transits
import secmotion
import placspec
import util



class PrimDir:
	'''Represents a PD'''

	NONE = -1

	OFFSANGLES = planets.Planets.BODIES_NUM-1

	ASC = OFFSANGLES 
	DESC = ASC+1
	MC = DESC+1
	IC = MC+1
	BOUND = IC+1
	USER = BOUND+12+1


	def __init__(self):
		self.prom = PrimDir.NONE
		self.prom2 = PrimDir.NONE
		self.sig = PrimDir.NONE
		self.promasp = PrimDir.NONE
		self.sigasp = PrimDir.NONE
		self.arc = 0.0
		self.direct = True
		self.time = 0.0
		self.age = 0.0


class PrimDirs(threading.Thread):
	'''Implements the PDs that are common in all systems (directions to Asc-MC)'''

	#subzodiacals
	SZNEITHER = 0
	SZPROMISSOR = 1
	SZSIGNIFICATOR = 2
	SZBOTH = 3

	#zodical options
	ASPSPROMSTOSIGS = 0
	PROMSTOSIGASPS = 1

	#Dynamic Keys
	TRUESOLAREQUATORIALARC = 0
	BIRTHDAYSOLAREQUATORIALARC = 1
	TRUESOLARECLIPTICALARC = 2
	BIRTHDAYSOLARECLIPTICALARC = 3

	#Static Keys
	NAIBOD = 0
	CARDAN = 1
	PTOLEMY = 2
	USER = 3

	#Static data
	DEG = 0
	MIN = 1
	SEC = 2
	COEFF = 3
	staticData = ((0, 59, 8, 1.01456164), (0, 59, 12, 1.0135135), (1, 0, 0, 1.0))

	#Directions
	DIRECT = 0
	CONVERSE = 1
	BOTHDC = 2

	#Range
	RANGE25 = 0
	RANGE50 = 1
	RANGE75 = 2
	RANGE100 = 3
	RANGEALL = 4

	LIMIT = 100.0

	Ranges = ((0.0, 25.0), (25.0, 50.0), (50.0, 75.0), (75.0, LIMIT), (0.0, LIMIT))
	LOW = 0
	HIGH = 1


	def __init__(self, chrt, options, pdrange, direction, abort, queuepd):
		threading.Thread.__init__(self)

		self.chart = chrt
		self.options = options
		self.pdrange = pdrange
		self.direction = direction
		self.abort = abort
		self.queuepd = queuepd

		self.ramc = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.RA]
		self.raic = self.ramc+180.0
		if (self.raic >= 360.0):
			self.raic -= 360.0

		self.aoasc = self.ramc+90.0
		if (self.aoasc >= 360.0):
			self.aoasc -= 360.0

		self.dodesc = self.raic+90.0
		if (self.dodesc >= 360.0):
			self.dodesc -= 360.0

		#User
		d = self.options.pduserlon[0]
		m = self.options.pduserlon[1]
		s = self.options.pduserlon[2]
		d2 = self.options.pduserlat[0]
		m2 = self.options.pduserlat[1]
		s2 = self.options.pduserlat[2]
		lon = d+m/60.0+s/3600.0
		lat = d2+m2/60.0+s2/3600.0
		if (self.options.pdusersouthern):
			lat *= -1

		ra, decl, dist = astronomy.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])
		self.userpromspec = placspec.PlacidianSpeculum(self.chart.place.lat, self.ramc, lon, lat, ra, decl)

		d = self.options.pduser2lon[0]
		m = self.options.pduser2lon[1]
		s = self.options.pduser2lon[2]
		d2 = self.options.pduser2lat[0]
		m2 = self.options.pduser2lat[1]
		s2 = self.options.pduser2lat[2]
		lon = d+m/60.0+s/3600.0
		lat = d2+m2/60.0+s2/3600.0
		if (self.options.pduser2southern):
			lat *= -1

		ra, decl, dist = astronomy.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])
		self.usersigspec = placspec.PlacidianSpeculum(self.chart.place.lat, self.ramc, lon, lat, ra, decl)


	def run(self):
		self.calcPlanets2AscMC()
		if (self.abort.isAborting()):
			return
		if (self.options.pdbounds):
			self.calcBounds2AscMC()
			if (self.abort.isAborting()):
				return
		if (self.options.pduser):
			self.calcUser2AscMC()
			if (self.abort.isAborting()):
				return

		if (self.options.ascmchcsasproms):
			if (self.options.sigascmc[0]):
				self.calcAsc2AspsPlanets()
				if (self.abort.isAborting()):
					return
				if (self.options.pduser2):
					self.calcAsc2User2()
					if (self.abort.isAborting()):
						return
			if (self.options.sigascmc[1]):
				self.calcMC2AspsPlanets()
				if (self.abort.isAborting()):
					return
				if (self.options.pduser2):
					self.calcMC2User2()
					if (self.abort.isAborting()):
						return

		self.calcPlanets2AspsPlanets()
		if (self.abort.isAborting()):
			return
		self.calcAspsPlanets2Planets()
		if (self.abort.isAborting()):
			return
		if (self.options.pdbounds):
			self.calcBounds2Sigs()
			if (self.abort.isAborting()):
				return
		if (self.options.pduser):
			self.calcUser2AspsPlanets()
			if (self.abort.isAborting()):
				return
			self.calcAspsUser2Planets()
			if (self.abort.isAborting()):
				return
		if (self.options.pduser2):
			self.calcAspsPlanets2User2()
			if (self.abort.isAborting()):
				return
			self.calcPlanets2AspsUser2()

		self.abort.setReady()


	def calcPlanets2AscMC(self):
		if (self.options.sigascmc[0] or self.options.sigascmc[1]):
			for i in range(planets.Planets.BODIES_NUM-1):
				if (not self.options.promplanets[i]):
					continue

				pl = self.chart.planets.planets[i]
				self.toAscMC(pl.data[planet.Planet.LON], pl.data[planet.Planet.LAT], i, 0)


	def calcBounds2AscMC(self):
		if (self.options.sigascmc[0] or self.options.sigascmc[1]):
			num = len(self.options.bounds[0])
			subnum = len(self.options.bounds[0][0])
			for i in range(num):
				summa = 0
				for j in range(subnum):
					if (self.abort.isAborting()):
						return

					self.options.bounds[self.options.selbounds][i][j][0]
					lonbound = i*chart.Chart.SIGN_DEG+summa
					if (self.options.ayanamsa != 0):
						lonbound += self.chart.ayanamsa
						lonbound = util.normalize(lonbound)
					rabound, declbound, dist = astronomy.swe_cotrans(lonbound, 0.0, 1.0, -self.chart.obl[0])

					val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declbound))
					if (math.fabs(val) > 1.0):
						continue
					adlat = math.degrees(math.asin(val))
					#MC
					if (self.options.sigascmc[1]):
						self.create(PrimDir.BOUND+i, self.options.bounds[self.options.selbounds][i][j][0], PrimDir.MC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, rabound-self.ramc)

					#Asc
					if (self.options.sigascmc[0]):
						aobound = rabound-adlat
						self.create(PrimDir.BOUND+i, self.options.bounds[self.options.selbounds][i][j][0], PrimDir.ASC, chart.Chart.CONIUNCTIO, chart.Chart.CONIUNCTIO, aobound-self.aoasc)

					summa += self.options.bounds[self.options.selbounds][i][j][1]


	def calcUser2AscMC(self):
		if (self.options.sigascmc[0] or self.options.sigascmc[1]):
			lon = self.userpromspec.data[placspec.PlacidianSpeculum.LON]
			lat = self.userpromspec.data[placspec.PlacidianSpeculum.LAT]

			self.toAscMC(lon, lat, PrimDir.USER, False)


	def toAscMC(self, pllon, pllat, i, check=True):
		SINISTER = 0
		DEXTER = 1

		for j in range(chart.Chart.OPPOSITIO+1):
			if (not self.options.pdaspects[j]):
				continue

			if (not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS] and j > chart.Chart.CONIUNCTIO):
				break

			#We don't need the aspects of the nodes
			if (check and i >= planets.Planets.PLANETS_NUM and j > chart.Chart.CONIUNCTIO):
				break

			if (self.abort.isAborting()):
				return

			aspectus = chart.Chart.Aspects[j]
			for k in range(DEXTER+1):
				lon = 0.0
				if (k == SINISTER):
					lon = pllon+chart.Chart.Aspects[j]
					if (lon >= 360.0):
						lon -= 360.0

					aspectus = chart.Chart.Aspects[j]
				else:
					if (j == chart.Chart.CONIUNCTIO or j == chart.Chart.OPPOSITIO):
						continue

					lon = pllon-chart.Chart.Aspects[j]
					if (lon < 0.0):
						lon += 360.0

					aspectus = -chart.Chart.Aspects[j]

				rapl = 0.0
				adlat = 0.0
				latprom = 0.0
				if (self.options.subzodiacal == PrimDirs.SZBOTH):
					if (self.options.bianchini):
						val = self.getBianchini(pllat, chart.Chart.Aspects[j])
						if (math.fabs(val) > 1.0):
							continue
						latprom = math.degrees(math.asin(val))
					else:
						latprom = pllat
				elif (self.options.subzodiacal == PrimDirs.SZPROMISSOR):
					latprom = pllat

				rapl, declpl, dist = astronomy.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
				if (math.fabs(val) > 1.0):
					continue
				adlat = math.degrees(math.asin(val))

				#MC
				if (self.options.sigascmc[1]):
					ok = True
					if (i == planets.Planets.MOON and self.options.pdsecmotion):
						for itera in range(self.options.pdsecmotioniter+1):
							ok, rapl, adlat = self.calcZodSM(i, j, aspectus, rapl-self.ramc)
					
					if (ok):
						self.create(i, PrimDir.NONE, PrimDir.MC, j, chart.Chart.CONIUNCTIO, rapl-self.ramc)
					#IC
					if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and j == chart.Chart.CONIUNCTIO:
						ok = True
						if (i == planets.Planets.MOON and self.options.pdsecmotion):
							for itera in range(self.options.pdsecmotioniter+1):
								ok, rapl, adlat = self.calcZodSM(i, j, aspectus, rapl-self.raic)

						if (ok):
							self.create(i, PrimDir.NONE, PrimDir.IC, j, chart.Chart.CONIUNCTIO, rapl-self.raic)

				#Asc
				if (self.options.sigascmc[0]):
					aopl = rapl-adlat
					ok = True
					if (i == planets.Planets.MOON and self.options.pdsecmotion):
						for itera in range(self.options.pdsecmotioniter+1):
							ok, rapl, adlat = self.calcZodSM(i, j, aspectus, aopl-self.aoasc)
							aopl = rapl-adlat

					if (ok):
						self.create(i, PrimDir.NONE, PrimDir.ASC, j, chart.Chart.CONIUNCTIO, aopl-self.aoasc)

					#Desc
					if (not self.options.pdaspects[chart.Chart.OPPOSITIO] or not self.options.zodpromsigasps[PrimDirs.ASPSPROMSTOSIGS]) and j == chart.Chart.CONIUNCTIO:
						dopl = rapl+adlat
						ok = True
						if (i == planets.Planets.MOON and self.options.pdsecmotion):
							for itera in range(self.options.pdsecmotioniter+1):
								ok, rapl, adlat = self.calcZodSM(i, j, aspectus, dopl-self.dodesc)
								dopl = rapl+adlat

						if (ok):
							self.create(i, PrimDir.NONE, PrimDir.DESC, j, chart.Chart.CONIUNCTIO, dopl-self.dodesc)


	def calcZodSM(self, idp, j, aspect, arc):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place.lat, idp, arc, self.ramc, self.options.topocentric)
		pllon = sm.planet.speculum.data[placspec.PlacidianSpeculum.LON]
		pllat = sm.planet.speculum.data[placspec.PlacidianSpeculum.LAT]

		lon = pllon+aspect
		lon = util.normalize(lon)

		rapl = 0.0
		adlat = 0.0
		latprom = 0.0
		if (self.options.subzodiacal == PrimDirs.SZBOTH):
			if (self.options.bianchini):
				val = self.getBianchini(pllat, chart.Chart.Aspects[j])
				if (math.fabs(val) > 1.0):
					return False, 0.0, 0.0
				latprom = math.degrees(math.asin(val))
			else:
				latprom = pllat
		elif (self.options.subzodiacal == PrimDirs.SZPROMISSOR):
			latprom = pllat

		rapl, declpl, dist = astronomy.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declpl))
		if (math.fabs(val) > 1.0):
			return False, 0.0, 0.0
		adlat = math.degrees(math.asin(val))

		return True, rapl, adlat


	def getBianchini(self, lat, asp):
		return math.sin(math.radians(lat))*math.cos(math.radians(asp))


	def getDiff(self, diff):
		direct = True
		if diff < 0.0:
			diff *= -1
			direct = False
		if diff > 180.0:
			diff = 360.0-diff 
			direct = not direct

		if not direct:
			diff *= -1

		return diff


	def create(self, prom, prom2, sig, promasp, sigasp, arc):
		'''Creates a direction and pushes it into the list of directions'''

		#Just for safety
		if (arc <= -360.0):
			arc += 360.0
		if (arc >= 360.0):
			arc -= 360.0

		direct = True
		if (arc < 0.0):
			arc *= -1
			direct = False
		if (arc > 180.0):
			arc = 360.0-arc 
			direct = not direct

		if ((arc >= PrimDirs.LIMIT or arc <= -PrimDirs.LIMIT) or (self.direction == PrimDirs.DIRECT and not direct) or (self.direction == PrimDirs.CONVERSE and direct)):
			return

		time, age = self.calcTime(arc, direct)

		if (age < PrimDirs.Ranges[self.pdrange][PrimDirs.LOW] or age >= PrimDirs.Ranges[self.pdrange][PrimDirs.HIGH]):
			return

		pd = PrimDir()
		pd.prom = prom
		pd.prom2 = prom2
		pd.sig = sig
		pd.promasp = promasp
		pd.sigasp = sigasp
		pd.arc = arc
		pd.direct = direct
		pd.time = time
		pd.age = age

		try:
			self.queuepd.put_nowait(pd)
		except queue.Full:
			pass


	def calcTime(self, arc, direct):
		'''Calculates time from arc according to the selected key (dynamic or static)'''

		ti = 0.0

		if (self.options.pdkeydyn):
			if (self.options.pdkeyd == PrimDirs.TRUESOLAREQUATORIALARC or self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC):
				ti = self.calcTrueSolarArc(arc)
			else:
				ti = self.calcBirthSolarArc(arc)
		else:
			if (self.options.pdkeys == PrimDirs.USER):
				val = (self.options.pdkeydeg+self.options.pdkeymin/60.0+self.options.pdkeysec/3600.0) 
				if (val != 0.0):
					coeff = 1.0/val
					ti = arc*coeff
			else:
				ti = arc*PrimDirs.staticData[self.options.pdkeys][PrimDirs.COEFF]

		return self.chart.time.jd+ti*365.2421904, ti


	def calcTrueSolarArc(self, arc):
		LIM = 120.0 #arbitrary value
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		h, mi, s = util.decToDeg(self.chart.time.time)
		tt = 0.0

		#Add arc to Suns's pos (long or ra)
		prSunPos = self.chart.planets.planets[planets.Planets.SUN].dataEqu[planet.Planet.RAEQU]
		if (self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC):
			prSunPos = self.chart.planets.planets[planets.Planets.SUN].data[planet.Planet.LON]

		prSunPosEnd = prSunPos+arc
		transition = False #Pisces-Aries
		if (prSunPosEnd >= 360.0):
			transition = True

#		Find day in ephemeris
		while (prSunPos <= prSunPosEnd):
			y, m, d = util.incrDay(y, m, d)
			ti = chtime.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chtime.Time.GREENWICH, True, 0, 0, False, self.chart.place, False)
			sun = planet.Planet(ti.jd, planets.Planets.SUN, astronomy.SEFLG_SWIEPH)
			
			pos = sun.dataEqu[planet.Planet.RAEQU]
			if (self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC):
				pos = sun.data[planet.Planet.LON]

			if (transition and pos < LIM):
				pos += 360.0
			prSunPos = pos

			if (self.abort.isAborting()):
				return 0.0

		if (prSunPos != prSunPosEnd):
			y, m, d = util.decrDay(y, m, d)

			if (transition):
				prSunPosEnd -= 360.0

			trlon = 0.0
			if (self.options.pdkeyd == PrimDirs.TRUESOLARECLIPTICALARC):
				trlon = prSunPosEnd
			else:
				#to Longitude...
				trlon = util.ra2ecl(prSunPosEnd, self.chart.obl[0])

			trans = transits.Transits()
			trans.day(y, m, d, self.chart, planets.Planets.SUN, trlon)

			if (len(trans.transits) > 0):
				tt = trans.transits[0].time
		else:
			#the time is midnight
			tt = 0.0

		#difference
		d1 = datetime.datetime(self.chart.time.year, self.chart.time.month, self.chart.time.day, h, mi, s) #in GMT
		th, tm, ts = util.decToDeg(tt)
		d2 = datetime.datetime(y, m, d, th, tm, ts) #in GMT
		diff = d2-d1
		ddays = diff.days
		dtime = diff.seconds/3600.0
		#dtime to days
		dtimeindays = dtime/24.0

		tt = ddays+dtimeindays

		return tt


	def calcBirthSolarArc(self, arc):
		y = self.chart.time.year
		m = self.chart.time.month
		d = self.chart.time.day

		yn, mn, dn = util.incrDay(y, m, d)

		ti1 = chtime.Time(y, m, d, 0, 0, 0, False, self.chart.time.cal, chtime.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)
		ti2 = chtime.Time(yn, mn, dn, 0, 0, 0, False, self.chart.time.cal, chtime.Time.LOCALMEAN, True, 0, 0, False, self.chart.place, False)

		sun1 = planet.Planet(ti1.jd, planets.Planets.SUN, astronomy.SEFLG_SWIEPH)
		sun2 = planet.Planet(ti2.jd, planets.Planets.SUN, astronomy.SEFLG_SWIEPH)

		diff = 0.0
		if (self.options.pdkeyd == PrimDirs.BIRTHDAYSOLAREQUATORIALARC):
			diff = sun2.dataEqu[planet.Planet.RAEQU]-sun1.dataEqu[planet.Planet.RAEQU]
		elif (self.options.pdkeyd == PrimDirs.BIRTHDAYSOLARECLIPTICALARC):
			diff = sun2.data[planet.Planet.LON]-sun1.data[planet.Planet.LON]

		coeff = 0.0
		if (diff != 0.0):
			coeff = 1.0/diff

		return arc*coeff


