import util
import placspec
import astronomy


class Planet:
	"""Data of a Planet"""

	#data[x]
	LON, LAT, DIST, SPLON, SPLAT, SPDIST = range(0, 6)

	#dataEqu
	RAEQU, DECLEQU, DISTEQU, SPRAEQU, SPDECLEQU, SPDISTEQU = range(0, 6)


	def __init__(self, tjd_ut, pId, flag, placelat=None, ramc=None, dnodeecl=None, dnodeequ=None):
		if (pId < 7):
			pId = util.mapChaldeanToModern(pId)

		self.pId = pId

		if (dnodeecl == None):
			rflag, self.data, serr = astronomy.swe_calc_ut(tjd_ut, pId, flag)
#			rflag, self.dataEqu, serr = astronomy.swe_calc_ut(tjd_ut, pId, flag+astronomy.SEFLG_EQUATORIAL)
			rflag, self.dataEqu, serr = astronomy.swe_calc_ut(tjd_ut, pId, flag+(2*1024))

			# data[0] : longitude
			# data[1] : latitude
			# data[2] : distance
			# data[3] : speed in long
			# data[4] : speed in lat
			# data[5] : speed in dist

			# if (rflag < 0):
			#	print 'Error: %s' % serr

			self.name = astronomy.swe_get_planet_name(pId)
		else: #To build the DescNode from the AscNode
			self.data = tuple(dnodeecl)
			self.dataEqu = tuple(dnodeequ)
			self.name = 'DescNode'

		if (placelat != None and ramc != None):
			self.speculum = placspec.PlacidianSpeculum(placelat, ramc, self.data[Planet.LON], self.data[Planet.LAT], self.dataEqu[Planet.RAEQU], self.dataEqu[Planet.DECLEQU])
		else:
			self.speculum = None











