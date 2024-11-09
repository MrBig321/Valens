import os

class Common:
	def __init__(self):

		self.ephepath = os.path.join('SWEP', 'Ephem')

		self.asc = '0'
		self.mc = '1'
		self.ascmc = ('0', '1')
		self.signs = ('a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l')
		self.planets = ('A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I')
		self.aspects = ('L', 'M', 'N', 'O', 'P', 'R', 'S')
		self.parallels = ('R', 'S')
		self.housenames = ('I', '2', '3', 'IV', '5', '6', 'VII', '8', '9', 'X', '11', '12')
		self.housenames2 = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')

		self.lots = ('t', 'u', 'v', 'w', 'x', 'y', 'z')

		self.syzygy = 's'

		self.retr = 'T'





