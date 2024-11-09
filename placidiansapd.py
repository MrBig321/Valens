import math
import astronomy
import planet
import planets
import houses
import chart
import primdirs
import secmotion
import placspec
import util


class PlacidianSAPD(primdirs.PrimDirs):
	'Implements Placidus(Semiarc) Primary Directions [i.e. Ptolemy]'

	def __init__(self, chrt, options, pdrange, direction, abort, queuepd):
		primdirs.PrimDirs.__init__(self, chrt, options, pdrange, direction, abort, queuepd)


	def calcPlanets2AspsPlanets(self):
		for p in range(planets.Planets.BODIES_NUM-1):
			if (not self.options.promplanets[p]):
				continue

			if (self.abort.isAborting()):
				return

			plprom = self.chart.planets.planets[p]
			raprom = plprom.speculum.data[placspec.PlacidianSpeculum.RA]
			adprom = plprom.speculum.data[placspec.PlacidianSpeculum.ADLAT]

			if (self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH):
				#recalc zodiacals
				raprom, declprom, dist = astronomy.swe_cotrans(plprom.data[planet.Planet.LON], 0.0, 1.0, -self.chart.obl[0])

				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
				if (math.fabs(val) > 1.0):
					continue
				adprom = math.degrees(math.asin(val))

			self.toPlanets(p, raprom, adprom)


	def calcUser2AspsPlanets(self):
		lonprom = self.userpromspec.data[placspec.PlacidianSpeculum.LON]
		raprom = self.userpromspec.data[placspec.PlacidianSpeculum.RA]
		adprom = self.userpromspec.data[placspec.PlacidianSpeculum.ADLAT]

		if (self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH):
			raprom, declprom, dist = astronomy.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
			if (math.fabs(val) > 1.0):
				return
			adprom = math.degrees(math.asin(val))

		self.toPlanets(primdirs.PrimDir.USER, raprom, adprom)


	def calcAspsPlanets2Planets(self):
		'''Calclucates zodiacal directions of the aspects of promissors to significators'''

		SINISTER = 0
		DEXTER = 1

		for p in range(planets.Planets.PLANETS_NUM):
			if (not self.options.promplanets[p]):
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculum.data[placspec.PlacidianSpeculum.LAT]

			for psidx in range(chart.Chart.CONIUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if (not self.options.pdaspects[psidx]):
					continue

				if (self.abort.isAborting()):
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[psidx]
					if (k == DEXTER):
						if (psidx == chart.Chart.OPPOSITIO):
							break

						aspect *= -1

					lon = plprom.data[planet.Planet.LON]+aspect
					lon = util.normalize(lon)
					raprom, adprom = 0.0, 0.0
					if (self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
						latprom = pllat
						if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH and self.options.bianchini):
							val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
							if (math.fabs(val) > 1.0):
								continue
							latprom = math.degrees(math.asin(val))

						#calc real(wahre)ra and adlat
#						raprom, declprom = util.getRaDecl(lon, latprom, self.chart.obl[0])
						raprom, declprom, dist = astronomy.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
						if (math.fabs(val) > 1.0):
							continue
						adprom = math.degrees(math.asin(val))
					else:
						raprom, declprom, dist = astronomy.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
						if (math.fabs(val) > 1.0):
							continue
						adprom = math.degrees(math.asin(val))

					for s in range(planets.Planets.BODIES_NUM-1):
						if (not self.options.sigplanets[s]):
							continue

						if (self.abort.isAborting()):
							return

						sigspec = self.chart.planets.planets[s].speculum
						self.toPlanet(p, primdirs.PrimDir.NONE, raprom, adprom, psidx, s, chart.Chart.CONIUNCTIO, sigspec, True, aspect)


	def calcAspsUser2Planets(self):
		SINISTER = 0
		DEXTER = 1

		pllon = self.userpromspec.data[placspec.PlacidianSpeculum.LON]
		pllat = self.userpromspec.data[placspec.PlacidianSpeculum.LAT]

		for psidx in range(chart.Chart.CONIUNCTIO+1, chart.Chart.OPPOSITIO+1):
			if (not self.options.pdaspects[psidx]):
				continue

			if (self.abort.isAborting()):
				return

			for k in range(DEXTER+1):
				aspect = chart.Chart.Aspects[psidx]
				if (k == DEXTER):
					if (psidx == chart.Chart.OPPOSITIO):
						break

					aspect *= -1

				lon = pllon+aspect
				lon = util.normalize(lon)
				raprom, adprom = 0.0, 0.0
				if (self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
					latprom = pllat
					if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH and self.options.bianchini):
						val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
						if (math.fabs(val) > 1.0):
							continue
						latprom = math.degrees(math.asin(val))

					#calc real(wahre)ra and adlat
#					raprom, declprom = util.getRaDecl(lon, latprom, self.chart.obl[0])
					raprom, declprom, dist = astronomy.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
					val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
					if (math.fabs(val) > 1.0):
						continue
					adprom = math.degrees(math.asin(val))
				else:
					raprom, declprom, dist = astronomy.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
					val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
					if (math.fabs(val) > 1.0):
						continue
					adprom = math.degrees(math.asin(val))

				for s in range(planets.Planets.BODIES_NUM-1):
					if (not self.options.sigplanets[s]):
						continue

					if (self.abort.isAborting()):
						return

					sigspec = self.chart.planets.planets[s].speculum
					self.toPlanet(primdirs.PrimDir.USER, primdirs.PrimDir.NONE, raprom, adprom, psidx, s, chart.Chart.CONIUNCTIO, sigspec, True, aspect)


	def calcBounds2Sigs(self):
		num = len(self.options.bounds[0])
		subnum = len(self.options.bounds[0][0])
		for i in range(num):
			summa = 0
			for j in range(subnum):
				lonprom = i*chart.Chart.SIGN_DEG+summa
				if (self.options.ayanamsa != 0):
					lonprom += self.chart.ayanamsa
					lonprom = util.normalize(lonprom)
				raprom, declprom, dist = astronomy.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
				if (math.fabs(val) > 1.0):
					continue
				adprom = math.degrees(math.asin(val))

				if (self.abort.isAborting()):
					return

				#Planets
				for s in range(planets.Planets.BODIES_NUM-1):
					if (self.options.sigplanets[s]):
						sigspec = self.chart.planets.planets[s].speculum
						self.toPlanet(primdirs.PrimDir.BOUND+i, self.options.bounds[self.options.selbounds][i][j][0], raprom, adprom, chart.Chart.CONIUNCTIO, s, chart.Chart.CONIUNCTIO, sigspec)

				#User2
				if (self.options.pduser2):
					self.toPlanet(primdirs.PrimDir.BOUND+i, self.options.bounds[self.options.selbounds][i][j][0], raprom, adprom, chart.Chart.CONIUNCTIO, primdirs.PrimDir.USER, chart.Chart.CONIUNCTIO, self.usersigspec)

				summa += self.options.bounds[self.options.selbounds][i][j][1]


	def calcAspsPlanets2User2(self):
		SINISTER = 0
		DEXTER = 1

		for p in range(planets.Planets.PLANETS_NUM):
			if (not self.options.promplanets[p]):
				continue

			plprom = self.chart.planets.planets[p]
			pllat = plprom.speculum.data[placspec.PlacidianSpeculum.LAT]

			for psidx in range(chart.Chart.CONIUNCTIO+1, chart.Chart.OPPOSITIO+1):
				if (not self.options.pdaspects[psidx]):
					continue

				if (self.abort.isAborting()):
					return

				for k in range(DEXTER+1):
					aspect = chart.Chart.Aspects[psidx]
					if (k == DEXTER):
						if (psidx == chart.Chart.OPPOSITIO):
							break

						aspect *= -1

					lon = plprom.data[planet.Planet.LON]+aspect
					lon = util.normalize(lon)
					raprom, adprom = 0.0, 0.0
					if (self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
						latprom = pllat
						if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH and self.options.bianchini):
							val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
							if (math.fabs(val) > 1.0):
								continue
							latprom = math.degrees(math.asin(val))

						#calc real(wahre)ra and adlat
#						raprom, declprom = util.getRaDecl(lon, latprom, self.chart.obl[0])
						raprom, declprom, dist = astronomy.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
						if (math.fabs(val) > 1.0):
							continue
						adprom = math.degrees(math.asin(val))
					else:
						raprom, declprom, dist = astronomy.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
						val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
						if (math.fabs(val) > 1.0):
							continue
						adprom = math.degrees(math.asin(val))

					self.toPlanet(p, primdirs.PrimDir.NONE, raprom, adprom, psidx, primdirs.PrimDir.USER, chart.Chart.CONIUNCTIO, self.usersigspec, True, aspect)


	def calcPlanets2AspsUser2(self):
		for p in range(planets.Planets.BODIES_NUM-1):
			if (not self.options.promplanets[p]):
				continue

			if (self.abort.isAborting()):
				return

			plprom = self.chart.planets.planets[p]
			raprom = plprom.speculum.data[placspec.PlacidianSpeculum.RA]
			adprom = plprom.speculum.data[placspec.PlacidianSpeculum.ADLAT]

			if (self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH):
				#recalc zodiacals
				raprom, declprom, dist = astronomy.swe_cotrans(plprom.data[planet.Planet.LON], 0.0, 1.0, -self.chart.obl[0])

				val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
				if (math.fabs(val) > 1.0):
					continue
				adprom = math.degrees(math.asin(val))

			self.toAspsUser2(p, raprom, adprom)


	def calcAsc2AspsPlanets(self):
		lonprom = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		raprom, declprom, dist = astronomy.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
		if (math.fabs(val) > 1.0):
			return
		adprom = math.degrees(math.asin(val))

		self.toPlanets(primdirs.PrimDir.ASC, raprom, adprom)


	def calcMC2AspsPlanets(self):
		lonprom = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		raprom, declprom, dist = astronomy.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
		if (math.fabs(val) > 1.0):
			return
		adprom = math.degrees(math.asin(val))

		self.toPlanets(primdirs.PrimDir.MC, raprom, adprom)


	def calcAsc2User2(self):
		lonprom = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		self.calcAscMC2User2(primdirs.PrimDir.ASC, lonprom)


	def calcMC2User2(self):
		lonprom = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		self.calcAscMC2User2(primdirs.PrimDir.MC, lonprom)


	def calcAscMC2User2(self, p, lonprom):
			raprom, declprom, dist = astronomy.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
			if (math.fabs(val) > 1.0):
				return
			adprom = math.degrees(math.asin(val))

			self.toAspsUser2(p, raprom, adprom)


	def toPlanets(self, p, raprom, adprom):
		'''Calculates the directions of the promissor to the planets and their aspects'''

		SINISTER = 0
		DEXTER = 1

		for s in range(planets.Planets.BODIES_NUM-1):
			if (not self.options.sigplanets[s]):
				continue

			if (self.abort.isAborting()):
				return

			sigspec = self.chart.planets.planets[s].speculum

			for asidx in range(chart.Chart.OPPOSITIO+1):
				if (not self.options.pdaspects[asidx] or (p == s and asidx == chart.Chart.CONIUNCTIO)):
					continue

				if (not self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS] and asidx > chart.Chart.CONIUNCTIO):
					continue

				if (self.abort.isAborting()):
					return

				#We don't need the aspects of the nodes
				if (s >= planets.Planets.PLANETS_NUM and asidx > chart.Chart.CONIUNCTIO):
					break

				self.toPlanet(p, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO, s, asidx, sigspec)


	def toPlanet(self, idprom, idprom2, raprom, adprom, promasp, sig, sigasp, sigspec, calcsecmotion=True, paspect=chart.Chart.NONE):
		aspect = chart.Chart.Aspects[sigasp]

		SINISTER = 0
		DEXTER = 1

		for k in range(DEXTER+1):
			if (k == DEXTER):
				if (sigasp == chart.Chart.CONIUNCTIO or sigasp == chart.Chart.OPPOSITIO):
					break

				aspect *= -1

			t, v, ra, mdpersasig = 0, 0, 0.0, 0.0
			if (self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
				if (sigasp == chart.Chart.CONIUNCTIO):
					t, v, ra = self.getvars(sigspec.abovehorizon, sigspec.eastern)

					mdsig = sigspec.data[placspec.PlacidianSpeculum.MD]
					if mdsig < 0.0:
						mdsig *= -1
					sasig = sigspec.data[placspec.PlacidianSpeculum.SA]
					if sasig < 0.0:
						sasig *= -1

					mdpersasig = mdsig/sasig
				else:
					lonsig = sigspec.data[placspec.PlacidianSpeculum.LON]+aspect
					lonsig = util.normalize(lonsig)
					latsig = sigspec.data[placspec.PlacidianSpeculum.LAT]

					if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH and self.options.bianchini):
						val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
						if (math.fabs(val) > 1.0):
							continue
						latsig = math.degrees(math.asin(val))

					ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig, latsig)
					if (not ok):
						continue
					t, v, ra = self.getvars(abovehorizon, eastern)
					mdpersasig = mdsig/sasig
			else:#zodiacal: calc aspectplace (conjunctio also)
				lonsig = sigspec.data[placspec.PlacidianSpeculum.LON]+aspect
				lonsig = util.normalize(lonsig)
				ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
				if (not ok):
					continue
				t, v, ra = self.getvars(abovehorizon, eastern)
				mdpersasig = mdsig/sasig

			arc = self.getDiff(raprom-ra)+t*(90+v*adprom)*mdpersasig
			ok = True
			if (idprom == planets.Planets.MOON and idprom2 == primdirs.PrimDir.NONE and self.options.pdsecmotion and calcsecmotion):
				if (paspect == chart.Chart.NONE):
					for itera in range(self.options.pdsecmotioniter+1):
						ok, arc = self.calcArcWithSM(idprom, sig, sigasp, aspect, arc, sigspec)
						if (not ok):
							break
				else:
					for itera in range(self.options.pdsecmotioniter+1):
						ok, arc = self.calcArcWithSM2(idprom, promasp, sig, paspect, arc, sigspec)
						if (not ok):
							break

			if (ok):
				self.create(idprom, idprom2, sig, promasp, sigasp, arc)


	def toAspsUser2(self, p, raprom, adprom):
		'''Calculates the directions of the promissor to User2 and their aspects'''

		SINISTER = 0
		DEXTER = 1

		for asidx in range(chart.Chart.OPPOSITIO+1):
			if (not self.options.pdaspects[asidx]):
				continue

			if (not self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS] and asidx > chart.Chart.CONIUNCTIO):
				continue

			if (self.abort.isAborting()):
				return

			self.toPlanet(p, primdirs.PrimDir.NONE, raprom, adprom, chart.Chart.CONIUNCTIO, primdirs.PrimDir.USER, asidx, self.usersigspec)


	def getZodMDSA(self, lon, lat=0.0):
		'''Calculates md, sa of the zodiacal point'''

		ra, decl, dist = astronomy.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])

		eastern = True
		if self.ramc > self.raic:
			if ra > self.raic and ra < self.ramc:
				eastern = False
		else:
			if (ra > self.raic and ra < 360.0) or (ra < self.ramc and ra > 0.0):
				eastern = False

		med = math.fabs(self.ramc-ra)

		if med > 180.0:
			med = 360.0-med
		icd = math.fabs(self.raic-ra)
		if icd > 180.0:
			icd = 360.0-icd

		md = med

		val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(decl))
		if math.fabs(val) > 1.0:
			return False, 0.0, 0.0, 0.0, 0.0

		adlat = math.degrees(math.asin(val))

		dsa = 90.0+adlat
		nsa = 90.0-adlat

		abovehorizon = True
		if med > dsa:
			abovehorizon = False

		sa = dsa
		if not abovehorizon:
			sa = nsa
			md = icd

		return True, md, sa, abovehorizon, eastern


	def getvars(self, abovehorizon, eastern):
		t = -1.0
		if (eastern and not abovehorizon) or (not eastern and abovehorizon):
			t = 1.0
	
		v = 1.0
		ra = self.ramc
		if (not abovehorizon):
			v = -1.0
			ra = self.raic

		return t, v, ra


#####################################Moon's SecMotion
	def calcArcWithSM(self, idprom, sig, sigasp, aspect, arc, sigspec):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place.lat, idprom, arc, self.ramc, self.options.topocentric)
		lonprom = sm.planet.speculum.data[placspec.PlacidianSpeculum.LON]
		raprom = sm.planet.speculum.data[placspec.PlacidianSpeculum.RA]
		adprom = sm.planet.speculum.data[placspec.PlacidianSpeculum.ADLAT]

		if (self.options.subzodiacal != primdirs.PrimDirs.SZPROMISSOR and self.options.subzodiacal != primdirs.PrimDirs.SZBOTH):
			#recalc zodiacals
			raprom, declprom, dist = astronomy.swe_cotrans(lonprom, 0.0, 1.0, -self.chart.obl[0])

			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
			if (math.fabs(val) > 1.0):
				return False, 0.0
			adprom = math.degrees(math.asin(val))

		t, v, ra, mdpersasig = 0, 0, 0.0, 0.0
		if (self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
			if (sigasp == chart.Chart.CONIUNCTIO):
				t, v, ra = self.getvars(sigspec.abovehorizon, sigspec.eastern)

				mdsig = sigspec.data[placspec.PlacidianSpeculum.MD]
				if mdsig < 0.0:
					mdsig *= -1
				sasig = sigspec.data[placspec.PlacidianSpeculum.SA]
				if sasig < 0.0:
					sasig *= -1

				mdpersasig = mdsig/sasig
			else:
				lonsig = sigspec.data[placspec.PlacidianSpeculum.LON]+aspect
				lonsig = util.normalize(lonsig)
				latsig = sigspec.data[placspec.PlacidianSpeculum.LAT]

				if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH and self.options.bianchini):
					val = self.getBianchini(latsig, chart.Chart.Aspects[sigasp])
					if math.fabs(val) > 1.0:
						return False, 0.0
					latsig = math.degrees(math.asin(val))

				ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig, latsig)
				if (not ok):
					return False, 0.0
				t, v, ra = self.getvars(abovehorizon, eastern)
				mdpersasig = mdsig/sasig
		else:#zodiacal: calc aspectplace (conjunctio also)
			lonsig = sigspec.data[placspec.PlacidianSpeculum.LON]+aspect
			lonsig = util.normalize(lonsig)
			ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
			if (not ok):
				return False, 0.0
			t, v, ra = self.getvars(abovehorizon, eastern)
			mdpersasig = mdsig/sasig

		arc = self.getDiff(raprom-ra)+t*(90+v*adprom)*mdpersasig

		return True, arc


	def calcArcWithSM2(self, idprom, psidx, sig, paspect, arc, sigspec):
		sm = secmotion.SecMotion(self.chart.time, self.chart.place.lat, idprom, arc, self.ramc, self.options.topocentric)
		lonprom = sm.planet.speculum.data[placspec.PlacidianSpeculum.LON]
		pllat = sm.planet.speculum.data[placspec.PlacidianSpeculum.LAT]

		lon = lonprom+paspect
		lon = util.normalize(lon)

		raprom, adprom = 0.0, 0.0
		if (self.options.subzodiacal == primdirs.PrimDirs.SZPROMISSOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
			latprom = pllat
			if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH and self.options.bianchini):
				val = self.getBianchini(pllat, chart.Chart.Aspects[psidx])
				if (math.fabs(val) > 1.0):
					return False, 0.0
				latprom = math.degrees(math.asin(val))

			raprom, declprom, dist = astronomy.swe_cotrans(lon, latprom, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
			if (math.fabs(val) > 1.0):
				return False, 0.0
			adprom = math.degrees(math.asin(val))
		else:
			raprom, declprom, dist = astronomy.swe_cotrans(lon, 0.0, 1.0, -self.chart.obl[0])
			val = math.tan(math.radians(self.chart.place.lat))*math.tan(math.radians(declprom))
			if (math.fabs(val) > 1.0):
				return False, 0.0
			adprom = math.degrees(math.asin(val))

		t, v, ra, mdpersasig = 0, 0, 0.0, 0.0
		if (self.options.subzodiacal == primdirs.PrimDirs.SZSIGNIFICATOR or self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
			t, v, ra = self.getvars(sigspec.abovehorizon, sigspec.eastern)

			mdsig = sigspec.data[placspec.PlacidianSpeculum.MD]
			if (mdsig < 0.0):
				mdsig *= -1
			sasig = sigspec.data[placspec.PlacidianSpeculum.SA]
			if (sasig < 0.0):
				sasig *= -1

			mdpersasig = mdsig/sasig
		else:#zodiacal: calc aspectplace (conjunctio also)
			lonsig = sigspec.data[placspec.PlacidianSpeculum.LON]
			ok, mdsig, sasig, abovehorizon, eastern = self.getZodMDSA(lonsig)
			if (not ok):
				return False, 0.0
			t, v, ra = self.getvars(abovehorizon, eastern)
			mdpersasig = mdsig/sasig

		arc = self.getDiff(raprom-ra)+t*(90+v*adprom)*mdpersasig

		return True, arc





