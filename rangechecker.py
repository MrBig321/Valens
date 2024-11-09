import os

class RangeChecker:
	def __init__(self):
		self.epherange = 3000
		self.extended = False

		if (os.path.isfile('SWEP/Ephem/seplm54.se1') and os.path.isfile('SWEP/Ephem/seplm48.se1') and os.path.isfile('SWEP/Ephem/seplm42.se1') and os.path.isfile('SWEP/Ephem/seplm36.se1') and os.path.isfile('SWEP/Ephem/semom54.se1') and os.path.isfile('SWEP/Ephem/semom48.se1') and os.path.isfile('SWEP/Ephem/semom42.se1') and os.path.isfile('SWEP/Ephem/semom36.se1') and os.path.isfile('SWEP/Ephem/sepl_30.se1') and os.path.isfile('SWEP/Ephem/sepl_36.se1') and os.path.isfile('SWEP/Ephem/sepl_42.se1') and os.path.isfile('SWEP/Ephem/sepl_48.se1') and os.path.isfile('SWEP/Ephem/semo_30.se1') and os.path.isfile('SWEP/Ephem/semo_36.se1') and os.path.isfile('SWEP/Ephem/semo_42.se1') and os.path.isfile('SWEP/Ephem/semo_48.se1')): 
			self.epherange = 5000
			self.extended = True


	def getRange(self):
		return self.epherange

	def isExtended(self):
		return self.extended


