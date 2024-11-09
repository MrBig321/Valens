import datetime
import chart
import texts


#Should have a ZodRelBase class and ZodRelL1 and ZodRelL3 derived from it...
class ZodRelL3:

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

	def __init__(self, y, m, d, h, mi, sign, opts):
		self.zrs = []

		self.y = y
		self.m = m
		self.d = d
		self.h = h
		self.mi = mi

		self.sign = sign
		self.opts = opts


	def calc(self):
		if (self.opts.zr27cap):
			ZodRelL3.planper[chart.Chart.CAPRICORNUS] = 27
		else:
			ZodRelL3.planper[chart.Chart.CAPRICORNUS] = 30

		#startdate
		startdate = datetime.datetime(self.y, self.m, self.d, self.h, self.mi, 0)
		sd = datetime.datetime(startdate.year, startdate.month, startdate.day, startdate.hour, startdate.minute, 0)

		daysperyear = 360.0
		if (not self.opts.zregyptian):
			daysperyear = 365.25

		diff = datetime.timedelta((daysperyear/12.0)*ZodRelL3.planper[self.sign])
		enddate = startdate+diff

		lb = False
		#There was already an LB?
		waslb = False
		signorig = self.sign
		go = True
		while(go):
			if (sd > enddate):
				go = False
				break

			if (sd != startdate and not waslb and self.sign == signorig):
				self.sign += int(chart.Chart.SIGN_NUM/2)
				if (self.sign >= chart.Chart.SIGN_NUM):
					self.sign -= chart.Chart.SIGN_NUM
				lb = True
				waslb = True
			else: lb = False

			self.zrs.append((self.sign, 3, sd.year, sd.month, sd.day, sd.hour, sd.minute, lb))

			#sub
			sdsub = datetime.datetime(sd.year, sd.month, sd.day, sd.hour, sd.minute, 0)
			signsub = self.sign
			lbsub = False
			waslbsub = False
			gosub = True
			diff = datetime.timedelta(ZodRelL3.planper[self.sign]*daysperyear/12.0/12.0)
			while(gosub):
				diffsub = datetime.timedelta(ZodRelL3.planper[signsub]*daysperyear/12.0/12.0/12.0)
				sdsub = sdsub+diffsub

				if (sdsub > sd+diff):
					gosub = False
					break

				signsubid = signsub+1
				if (signsubid > chart.Chart.PISCES):
					signsubid = chart.Chart.ARIES

				if (not waslbsub and self.sign == signsubid):
					signsub += int(chart.Chart.SIGN_NUM/2)
					if (signsub >= chart.Chart.SIGN_NUM):
						signsub -= chart.Chart.SIGN_NUM
					lbsub = True
					signsubid = signsub+1
					waslbsub = True
				else: lbsub = False

				self.zrs.append((signsubid, 4, sdsub.year, sdsub.month, sdsub.day, sdsub.hour, sdsub.minute, lbsub))

				signsub = signsub+1
				if (signsub > chart.Chart.PISCES):
					signsub = chart.Chart.ARIES

			sd = sd+diff

			self.sign = self.sign+1
			if (self.sign > chart.Chart.PISCES):
				self.sign = chart.Chart.ARIES

#		self.printZodRel()


	def printZodRel(self):
		num = len(self.zrs)
		for i in range(num):
			signtxt = texts.signs[self.zrs[i][ZodRelL3.SIGN]]
			leveltxt = 'L'+str(self.zrs[i][ZodRelL3.LEVEL])
			offstxt = ''
			if (self.zrs[i][ZodRelL3.LEVEL] == 3):
				leveltxt += '/L4'
			else:
				offstxt = '     '
			lbtxt = ''
			if (self.zrs[i][ZodRelL3.LB]):
				lbtxt = ' --- LB'

			datetxt = str(self.zrs[i][ZodRelL3.YEAR])+'/'+str(self.zrs[i][ZodRelL3.MONTH])+'/'+str(self.zrs[i][ZodRelL3.DAY])
			timetxt = str(self.zrs[i][ZodRelL3.HOUR]).zfill(2)+':'+str(self.zrs[i][ZodRelL3.MINUTE]).zfill(2)
			print(offstxt, signtxt, leveltxt, datetxt, timetxt, lbtxt)





