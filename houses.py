import astronomy
import texts
import util


class Houses:
	"""Calculates the cusps of the Houses"""

	HOUSE_NUM = 12 #number of housecusps
#	hsystems = ('P', 'K', 'R', 'C', 'E', 'W', 'X', 'M', 'H', 'T', 'B', 'O') #available Housesystems in the SwissEphemeris
	hsystems = ('W', 'O', 'B', 'R', 'P')

	WHOLESIGN, PORPHYRY, ALCABITUS, REGIOMONTANUS, PLACIDUS = range(5)

	ASC = 0
	MC = 1

	LON, LAT, RA, DECL = range(0, 4)

	def __init__(self, tjd_ut, flag, placelat, placelon, hsys, obl): #, ayanopt, ayan): #ayanopt is the ID
		if (hsys >= 0 and hsys < len(Houses.hsystems)):
			self.hsys = hsys
		else:
			self.hsys = 0

		res, self.cusps, sweascmc = astronomy.swe_houses_ex(tjd_ut, flag, placelat, placelon, ord(Houses.hsystems[self.hsys]))

		##################
#		if (ayanopt != 0 and self.hsys == 0):
#			del self.cusps
#			cusps = [0.0]
#			sign = int(util.normalize(sweascmc[Houses.ASC]-ayan))/30
#			cusps.append(sign*30.0)
#			for i in range(2, Houses.HOUSE_NUM+1):
#				hc = util.normalize(cusps[i-1]+30.0)
#				cusps.append(hc)
#
#			#to tuple (which is a read-only list)
#			self.cusps = tuple(cusps)
		##################

		ascra, ascdecl, dist = astronomy.swe_cotrans(sweascmc[Houses.ASC], 0.0, 1.0, -obl)				
		mcra, mcdecl, dist = astronomy.swe_cotrans(sweascmc[Houses.MC], 0.0, 1.0, -obl)
		self.ascmc = ((sweascmc[Houses.ASC], 0.0, ascra, ascdecl), (sweascmc[Houses.MC], 0.0, mcra, mcdecl))

#		self.printAscMC()
#		self.printHouses()


	def printAscMC(self):
		print('')
		print('Asc: lon=%f' % self.ascmc[Houses.ASC][Houses.LON])
		print('MC: lon=%f' % self.ascmc[Houses.MC][Houses.LON])


	def printHouses(self):
		print('')
		print('Selected housesystem: %s' % texts.hsystemList[self.hsys])
		for i in range(1, Houses.HOUSE_NUM+1):
			print('%d. %f' % (i, self.cusps[i]))



