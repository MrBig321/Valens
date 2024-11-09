import astronomy
import chart
import util


class FixedStars:
	"""Calculates the positions of the fixedstars"""

	NAME = 0
	NOMNAME = 1
	LON = 2
	LAT = 3
	RA = 4
	DECL = 5

	nomnames = ('etTau', 'alTau', 'bePer', 'ga-1And', 'alSco', 'alBoo', 'deCnc', 'gaCnc', 'etUMa', 'alOri', 'alCen', 'alCar', 'alGem', 'beLeo', 'alPsA', 'alCrB', 'alPeg', 'beAnd', 'alUMi', 'beGem', 'M44', 'alCMi', 'alLeo', 'beOri', 'alCMa', 'alVir', 'alSer', 'alLyr', 'al-2Lib', 'beLib')

	def __init__(self, tjd_ut, flag, obl):
		
		self.data = []

		num = len(FixedStars.nomnames)
		for i in range(num):
			self.data.append(['', '', 0.0, 0.0, 0.0, 0.0])
			ret, name, dat, serr = astronomy.swe_fixstar_ut(','+FixedStars.nomnames[i], tjd_ut, flag)

			nam = name[0].strip()
			nomnam = ''
			DELIMITER = ','
			if (nam.find(DELIMITER) != -1):
				snam = nam.split(DELIMITER)
				nam = snam[0].strip()
				nomnam = snam[1].strip()

			self.data[i][FixedStars.NAME] = nam
			self.data[i][FixedStars.NOMNAME] = nomnam
			self.data[i][FixedStars.LON] = dat[0]
			self.data[i][FixedStars.LAT] = dat[1]
			ra, decl, dist = astronomy.swe_cotrans(dat[0], dat[1], 1.0, -obl)
			self.data[i][FixedStars.RA] = ra
			self.data[i][FixedStars.DECL] = decl

		self.sort()

#		self.printFixedStars()


	def sort(self):
		num = len(self.data)
		self.mixed = []
			
		for i in range(num):
			self.mixed.append(i)

		for i in range(num):
			for j in range(num-1):
				if (self.data[j][FixedStars.LON] > self.data[j+1][FixedStars.LON]):
					tmp = self.data[j][:]
					self.data[j] = self.data[j+1][:]
					self.data[j+1] = tmp[:]
					tmp = self.mixed[j]
					self.mixed[j] = self.mixed[j+1]
					self.mixed[j+1] = tmp


	def printFixedStars(self):
		signs = ('Ari', 'Tau', 'Gem', 'Can', 'Leo', 'Vir', 'Lib', 'Sco', 'Sag', 'Cap', 'Aqu', 'Pis')

		print ('')
		print ('FixedStars')
		num = len(self.data)
		for i in range(num):
			si = int(self.data[i][FixedStars.LON]/chart.Chart.SIGN_DEG)
			d1, m1, s1 = util.decToDeg(self.data[i][FixedStars.LON])
			d2, m2, s2 = util.decToDeg(self.data[i][FixedStars.LAT])
			print ('%s %s %02d%s %02dm %02ds  %02ddeg %02dm %02ds' % (self.data[i][FixedStars.NAME], self.data[i][FixedStars.NOMNAME], d1, signs[si], m1, s1, d2, m2, s2))






