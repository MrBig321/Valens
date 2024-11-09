import datetime
import chart
import texts


class ZodRelL1:

	SIGN = 0
	LEVEL = 1
	YEAR = 2
	MONTH = 3
	DAY = 4
	HOUR = 5
	MINUTE = 6
	LB = 7

	#Planetary periods of planets assigned to signs (e.g. Mars is 15 and aries is the first sign, Venus is 8 years and Taurus is the second sign)
	planper = [15, 8, 20, 25, 19, 20, 8, 15, 12, 30, 30, 12]

	def __init__(self, time, sign, period, opts):
		self.zrs = []

		self.y = time.oyear
		self.m = time.omonth
		self.d = time.oday
		self.h = time.ohour
		self.mi = time.omin

		self.sign = sign
		self.period = period
		self.opts = opts


	def calc(self):
		#startdate
		startdate = datetime.datetime(self.y, self.m, self.d, self.h, self.mi, 0)
		sd = datetime.datetime(startdate.year, startdate.month, startdate.day, startdate.hour, startdate.minute, 0)

		daysperyear = 360.0
		if (not self.opts.zregyptian):
			daysperyear = 365.25

		if (self.opts.zr27cap):
			ZodRelL1.planper[chart.Chart.CAPRICORNUS] = 27
		else:
			ZodRelL1.planper[chart.Chart.CAPRICORNUS] = 30

		period2 = 0
		go = True
		while(go):
			if (self.period == period2):
				go = False
				break

			self.zrs.append((self.sign, 1, sd.year, sd.month, sd.day, sd.hour, sd.minute, False))
			#sub
			sdsub = datetime.datetime(sd.year, sd.month, sd.day, sd.hour, sd.minute, 0)
			signsub = self.sign
			gosub = True
			lb = False
			#There was already an LB?
			waslb = False
			months = 0
			while(gosub):
				diff = datetime.timedelta((daysperyear/12.0)*ZodRelL1.planper[signsub])
				sdsub = sdsub+diff

				months += ZodRelL1.planper[signsub]
				if (months/12.0 > ZodRelL1.planper[self.sign]):
					gosub = False
					break

				signsubid = signsub+1
				if (signsubid > chart.Chart.PISCES):
					signsubid = chart.Chart.ARIES

				if (not waslb and self.sign == signsubid):
					signsub += int(chart.Chart.SIGN_NUM/2)
					if (signsub >= chart.Chart.SIGN_NUM):
						signsub -= chart.Chart.SIGN_NUM
					lb = True
					signsubid = signsub+1
					waslb = True
				else: lb = False

				self.zrs.append((signsubid, 2, sdsub.year, sdsub.month, sdsub.day, sdsub.hour, sdsub.minute, lb))

				signsub = signsub+1
				if (signsub > chart.Chart.PISCES):
					signsub = chart.Chart.ARIES

			period2 += 1

			diff = datetime.timedelta(daysperyear*ZodRelL1.planper[self.sign])
			sd = sd+diff

			if (sd.year-startdate.year > 10000):	#safety, not to have an infinite loop
				go = False

			waslb = False

			self.sign = self.sign+1
			if (self.sign > chart.Chart.PISCES):
				self.sign = chart.Chart.ARIES

#		self.printZodRel()


	def printZodRel(self):
		num = len(self.zrs)
		for i in range(num):
			signtxt = texts.signs[self.zrs[i][ZodRelL1.SIGN]]
			leveltxt = 'L'+str(self.zrs[i][ZodRelL1.LEVEL])
			offstxt = ''
			if (self.zrs[i][ZodRelL1.LEVEL] == 1):
				leveltxt += '/L2'
			else:
				offstxt = '     '
			lbtxt = ''
			if (self.zrs[i][ZodRelL1.LB]):
				lbtxt = ' --- LB'

			datetxt = str(self.zrs[i][ZodRelL1.YEAR])+'/'+str(self.zrs[i][ZodRelL1.MONTH])+'/'+str(self.zrs[i][ZodRelL1.DAY])
			print(offstxt, signtxt, leveltxt, datetxt, lbtxt)





