import astronomy
import chtime
import planets
import planet
import util


class EphemCalc:

	PLANET = 0
	DAY = 1
#	HOUR = 2

	def __init__(self, year, opts):
		self.year = year
		self.flags = astronomy.SEFLG_SPEED+astronomy.SEFLG_SWIEPH
		self.posArr = []

		self.calc(opts)


	def calc(self, opts):
		ayanamsa = 0.0
		if (opts.ayanamsa != 0):
			astronomy.swe_set_sid_mode(opts.ayanamsa-1, 0, 0)
			tim = chtime.Time(self.year, 1, 1, 0, 0, 0, False, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
			ayanamsa = astronomy.swe_get_ayanamsa_ut(tim.jd)


		#calculating one per day (per hour would be too slow)
		for i in range(planets.Planets.PLANETS_NUM-1): #moon excepted
			y = self.year; m = 1; d = 1
			ar = []
			for num in range(365):
				time = chtime.Time(y, m, d, 0, 0, 0, False, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, True, 0, 0, False, None, False)
				pl = planet.Planet(time.jd, i, self.flags)
				pos = pl.data[planet.Planet.LON]
				if (opts.ayanamsa != 0):
					pos = util.normalize(pos-ayanamsa)

				ar.append(pos)

				y, m, d = util.incrDay(y, m, d)

			self.posArr.append(ar)



