import planets
import transits
import util


class Revolutions:

	def __init__(self):
		self.t = [0, 0, 0, 0, 0, 0]


	def compute(self, typ, by, bm, bd, chrt):
		if (typ == planets.Planets.SUN):
			year = by
			if (bm > chrt.time.month or (bm == chrt.time.month and bd > chrt.time.day)):
				year+= 1

			month = chrt.time.month
			day = chrt.time.day

			trans = transits.Transits()
			trans.month(year, month, chrt, planets.Planets.SUN)

#			if not found => checking previous or next month
			if (len(trans.transits) == 0):
				if (day < 4):
					year, month = util.decrMonth(year, month)
				else:
					year, month = util.incrMonth(year, month)

				trans = transits.Transits()
				trans.month(year, month, chrt, planets.Planets.SUN)

			if (len(trans.transits) > 0):
				self.createRevolution(year, month, trans)
				return True

			return False
		elif (typ == planets.Planets.MOON):
			trans = transits.Transits()
			trans.month(by, bm, chrt, planets.Planets.MOON)

			if (len(trans.transits) > 0):
				second = False

				if (bd > trans.transits[0].day):
					# There can be more than one lunar in a month!!
					if (len(trans.transits) > 1):
						if bd > trans.transits[1].day:
							by, bm = util.incrMonth(by, bm)

							trans = transits.Transits()
							trans.month(by, bm, chrt, planets.Planets.MOON)
						else:
							second = True
					else:
						by, bm = util.incrMonth(by, bm)

						trans = transits.Transits()
						trans.month(by, bm, chrt, planets.Planets.MOON)

				if (len(trans.transits) > 0):
					if (second):
						self.createRevolution(by, bm, trans, 1)
					else:
						self.createRevolution(by, bm, trans)
					return True

			return False
		elif (typ == planets.Planets.MERCURY):
			for i in range(14):
				trans = transits.Transits()
				trans.month(by, bm, chrt, planets.Planets.MERCURY)

				if (len(trans.transits) > 0):
					if (not (i == 0 and bd > trans.transits[0].day)):
						self.createRevolution(by, bm, trans)
						return True

				by, bm = util.incrMonth(by, bm)

			return False
		elif (typ == planets.Planets.VENUS):
			for i in range(16):
				trans = transits.Transits()
				trans.month(by, bm, chrt, planets.Planets.VENUS)

				if (len(trans.transits) > 0):
					if (not (i == 0 and bd > trans.transits[0].day)):
						self.createRevolution(by, bm, trans)
						return True

				by, bm = util.incrMonth(by, bm)

			return False
		elif (typ == planets.Planets.MARS):
			for i in range(26):
				trans = transits.Transits()
				trans.month(by, bm, chrt, planets.Planets.MARS)

				if (len(trans.transits) > 0):
					if (not (i == 0 and bd > trans.transits[0].day)):
						self.createRevolution(by, bm, trans)
						return True

				by, bm = util.incrMonth(by, bm)

			return False
		elif (typ == planets.Planets.JUPITER):
			for i in range(12*12):
				trans = transits.Transits()
				trans.month(by, bm, chrt, planets.Planets.JUPITER)

				if (len(trans.transits) > 0):
					if (not (i == 0 and bd > trans.transits[0].day)):
						self.createRevolution(by, bm, trans)
						return True

				by, bm = util.incrMonth(by, bm)

			return False
		elif (typ == planets.Planets.SATURN):
			for i in range(30*12):
				trans = transits.Transits()
				trans.month(by, bm, chrt, planets.Planets.SATURN)

				if (len(trans.transits) > 0):
					if (not (i == 0 and bd > trans.transits[0].day)):
						self.createRevolution(by, bm, trans)
						return True

				by, bm = util.incrMonth(by, bm)

			return False

		return False


	def createRevolution(self, year, month, trans, num = 0):
		self.t[0] = year
		self.t[1] = month
		self.t[2] = trans.transits[num].day
		h, m, s = util.decToDeg(trans.transits[num].time)
		self.t[3] = h
		self.t[4] = m
		self.t[5] = s



