import chart
import houses
import planets
import planet
import texts
import util


class Lots2:
	''' The lots from the editor '''

	##### Copied from lotsoptdlg ###### Should be moved from both to Options!?
	#Component of a Lot
	ASC, IC, DSC, MC, HC1, HC2, HC3, HC4, HC5, HC6, HC7, HC8, HC9, HC10, HC11, HC12 = range(16)
	SAT, JUP, MAR, SUN, VEN, MER, MOO = range(16, 23)
	PLS = SAT
	ASCLORD, ICLORD, DSCLORD, MCLORD, HC1LORD, HC2LORD, HC3LORD, HC4LORD, HC5LORD, HC6LORD, HC7LORD, HC8LORD, HC9LORD, HC10LORD, HC11LORD, HC12LORD = range(23, 39)
	HCLORD = ASCLORD
	SATLORD, JUPLORD, MARLORD, SUNLORD, VENLORD, MERLORD, MOOLORD = range(39, 46)
	PLSLORD = SATLORD
	SYZ = MOOLORD+1
	SYZLORD = SYZ+1
	LT = SYZLORD+1
	LTLORD = LT+1
	LD = LTLORD+1
	LDLORD = LD+1
	LH = LDLORD+1
	LHLORD = LH+1
	DE = LHLORD+1
	RE = DE+1
	RELORD = RE+1

	LORDTXT = '!'

	NAME = 0
	FORMULA = 1
	LONG = 2
	
	NAMEOPT = 0
	FORMULAOPT = 1
	REFORDEGSOPT = 2
	DIURNALOPT = 3

	domslords = (2, 4, 5, 6, 3, 5, 4, 2, 1, 0, 0, 1)	# rulers of the 12 signs acc. to chaldean order (saturn is 0, jupiter is 1, etc ...)
	daylords = (6, 2, 5, 1, 4, 0, 3)	

	def __init__(self, chrt):
		self.data = []

		opts = chrt.options

		asclon = chrt.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		iclon = util.normalize(chrt.houses.ascmc[houses.Houses.MC][houses.Houses.LON]+180.0)
		mclon = chrt.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		desclon = util.normalize(chrt.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]+180.0)
		angles = (asclon, iclon, desclon, mclon)

		hcs = list(chrt.houses.cusps[1:])
		if (opts.hcmeanssigncusp):
			del hcs[:]
			offs = 0
			if (opts.ascissigncusp):
				offs = asclon%chart.Chart.SIGN_DEG
			sign = int(asclon/chart.Chart.SIGN_DEG)
			for i in range(chart.Chart.SIGN_NUM):
				sign += i
				if (sign >= chart.Chart.SIGN_NUM):
					sign = 0
				hcs.append(sign*chart.Chart.SIGN_DEG+offs)

		pls = (chrt.planets.planets[planets.Planets.SATURN].data[planet.Planet.LON], chrt.planets.planets[planets.Planets.JUPITER].data[planet.Planet.LON], chrt.planets.planets[planets.Planets.MARS].data[planet.Planet.LON], chrt.planets.planets[planets.Planets.SUN].data[planet.Planet.LON], chrt.planets.planets[planets.Planets.VENUS].data[planet.Planet.LON], chrt.planets.planets[planets.Planets.MERCURY].data[planet.Planet.LON], chrt.planets.planets[planets.Planets.MOON].data[planet.Planet.LON])

		syzlon = chrt.syzygy.lon
		ltlon = pls[planets.Planets.MOON]
		abovehor = chrt.isAboveHorizon()
		if (abovehor):
			ltlon = pls[planets.Planets.SUN]

		ldlon = pls[Lots2.daylords[chrt.time.ph.weekday]]
		lhlon = pls[chrt.time.ph.planetaryhour]

		ar = (syzlon, pls[self.getLord(syzlon)], ltlon, pls[self.getLord(ltlon)], ldlon, pls[self.getLord(ldlon)], lhlon, pls[self.getLord(lhlon)])

		num = len(opts.lotsopts)
		for i in range(num):
			nametxt = opts.lotsopts[i][Lots2.NAMEOPT]
			lon1 = lon2 = lon3 = 0.0
			f1txt = f2txt = f3txt = ''
			if (opts.lotsopts[i][Lots2.FORMULAOPT][0] == Lots2.DE):
				sign = int(opts.lotsopts[i][Lots2.REFORDEGSOPT][0]/chart.Chart.SIGN_DEG)
				deg = int(opts.lotsopts[i][Lots2.REFORDEGSOPT][0]%chart.Chart.SIGN_DEG)
				f1txt = str(deg)+texts.signs2[sign]
				lon1 = opts.lotsopts[i][Lots2.REFORDEGSOPT][0]
			elif (opts.lotsopts[i][Lots2.FORMULAOPT][0] == Lots2.RE or opts.lotsopts[i][Lots2.FORMULAOPT][0] == Lots2.RELORD):
				f1txt = texts.txtslotsdlg['R']+str(opts.lotsopts[i][Lots2.REFORDEGSOPT][0])
				lon1 = self.data[opts.lotsopts[i][Lots2.REFORDEGSOPT][0]-1][Lots2.LONG]
				if (opts.lotsopts[i][Lots2.FORMULAOPT][0] == Lots2.RELORD):
					f1txt += Lots2.LORDTXT
					lon1 = pls[self.getLord(self.data[opts.lotsopts[i][Lots2.REFORDEGSOPT][0]-1][Lots2.LONG])]
			else:
				f1txt = texts.lotComponentList[opts.lotsopts[i][Lots2.FORMULAOPT][0]]
				if (opts.lotsopts[i][Lots2.FORMULAOPT][0] < Lots2.HC1):
					lon1 = angles[opts.lotsopts[i][Lots2.FORMULAOPT][0]]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][0] < Lots2.PLS):
					lon1 = hcs[opts.lotsopts[i][Lots2.FORMULAOPT][0]-Lots2.HC1]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][0] < Lots2.ASCLORD):
					lon1 = pls[opts.lotsopts[i][Lots2.FORMULAOPT][0]-Lots2.PLS]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][0] < Lots2.HC1LORD):
					lon1 = pls[self.getLord(angles[opts.lotsopts[i][Lots2.FORMULAOPT][0]-Lots.ASCLORD])]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][0] < Lots2.PLSLORD):
					lon1 = pls[self.getLord(hcs[opts.lotsopts[i][Lots2.FORMULAOPT][0]-Lots2.HC1LORD])]
				else:
					lon1 = ar[opts.lotsopts[i][Lots2.FORMULAOPT][0]-Lots2.SYZ]

			if (opts.lotsopts[i][Lots2.FORMULAOPT][1] == Lots2.DE):
				sign = int(opts.lotsopts[i][Lots2.REFORDEGSOPT][1]/chart.Chart.SIGN_DEG)
				deg = int(opts.lotsopts[i][Lots2.REFORDEGSOPT][1]%chart.Chart.SIGN_DEG)
				f2txt = str(deg)+texts.signs2[sign]
				lon2 = opts.lotsopts[i][Lots2.REFORDEGSOPT][1]
			elif (opts.lotsopts[i][Lots2.FORMULAOPT][1] == Lots2.RE or opts.lotsopts[i][Lots2.FORMULAOPT][1] == Lots2.RELORD):
				f2txt = texts.txtslotsdlg['R']+str(opts.lotsopts[i][Lots2.REFORDEGSOPT][1])
				lon2 = self.data[opts.lotsopts[i][Lots2.REFORDEGSOPT][1]-1][Lots2.LONG]
				if (opts.lotsopts[i][Lots2.FORMULAOPT][1] == Lots2.RELORD):
					f2txt += Lots2.LORDTXT
					lon2 = pls[self.getLord(self.data[opts.lotsopts[i][Lots2.REFORDEGSOPT][1]-1][Lots2.LONG])]
			else:
				f2txt = texts.lotComponentList[opts.lotsopts[i][Lots2.FORMULAOPT][1]]
				if (opts.lotsopts[i][Lots2.FORMULAOPT][1] < Lots2.HC1):
					lon2 = angles[opts.lotsopts[i][Lots2.FORMULAOPT][1]]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][1] < Lots2.PLS):
					lon2 = hcs[opts.lotsopts[i][Lots2.FORMULAOPT][1]-Lots2.HC1]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][1] < Lots2.ASCLORD):
					lon2 = pls[opts.lotsopts[i][Lots2.FORMULAOPT][1]-Lots2.PLS]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][1] < Lots2.HC1LORD):
					lon2 = pls[self.getLord(angles[opts.lotsopts[i][Lots2.FORMULAOPT][1]-Lots.ASCLORD])]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][1] < Lots2.PLSLORD):
					lon2 = pls[self.getLord(hcs[opts.lotsopts[i][Lots2.FORMULAOPT][1]-Lots2.HC1LORD])]
				else:
					lon2 = ar[opts.lotsopts[i][Lots2.FORMULAOPT][1]-Lots2.SYZ]

			if (opts.lotsopts[i][Lots2.FORMULAOPT][2] == Lots2.DE):
				sign = int(opts.lotsopts[i][Lots2.REFORDEGSOPT][2]/chart.Chart.SIGN_DEG)
				deg = int(opts.lotsopts[i][Lots2.REFORDEGSOPT][2]%chart.Chart.SIGN_DEG)
				f3txt = str(deg)+texts.signs2[sign]
				lon3 = opts.lotsopts[i][Lots2.REFORDEGSOPT][2]
			elif (opts.lotsopts[i][Lots2.FORMULAOPT][2] == Lots2.RE or opts.lotsopts[i][Lots2.FORMULAOPT][2] == Lots2.RELORD):
				f3txt = texts.txtslotsdlg['R']+str(opts.lotsopts[i][Lots2.REFORDEGSOPT][2])
				lon3 = self.data[opts.lotsopts[i][Lots2.REFORDEGSOPT][2]-1][Lots2.LONG]
				if (opts.lotsopts[i][Lots2.FORMULAOPT][2] == Lots2.RELORD):
					f3txt += Lots2.LORDTXT
					lon3 = pls[self.getLord(self.data[opts.lotsopts[i][Lots2.REFORDEGSOPT][2]-1][Lots2.LONG])]
			else:
				f3txt = texts.lotComponentList[opts.lotsopts[i][Lots2.FORMULAOPT][2]]
				if (opts.lotsopts[i][Lots2.FORMULAOPT][2] < Lots2.HC1):
					lon3 = angles[opts.lotsopts[i][Lots2.FORMULAOPT][2]]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][2] < Lots2.PLS):
					lon3 = hcs[opts.lotsopts[i][Lots2.FORMULAOPT][2]-Lots2.HC1]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][2] < Lots2.ASCLORD):
					lon3 = pls[opts.lotsopts[i][Lots2.FORMULAOPT][2]-Lots2.PLS]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][2] < Lots2.HC1LORD):
					lon3 = pls[self.getLord(angles[opts.lotsopts[i][Lots2.FORMULAOPT][2]-Lots.ASCLORD])]
				elif (opts.lotsopts[i][Lots2.FORMULAOPT][2] < Lots2.PLSLORD):
					lon3 = pls[self.getLord(hcs[opts.lotsopts[i][Lots2.FORMULAOPT][2]-Lots2.HC1LORD])]
				else:
					lon3 = ar[opts.lotsopts[i][Lots2.FORMULAOPT][2]-Lots2.SYZ]

			formulatxt = f1txt+'+'+f2txt+'-'+f3txt
			lon = util.normalize(lon1+util.normalize(lon2-lon3))
			if (opts.lotsopts[i][Lots2.DIURNALOPT] and not abovehor):  # switch in case of nocturnal
				formulatxt = f1txt+'+'+f3txt+'-'+f2txt
				lon = util.normalize(lon1+util.normalize(lon3-lon2))

			self.data.append((nametxt, formulatxt, lon))

#		self.printLots()


	def getLord(self, lon):
		sign = int(lon/chart.Chart.SIGN_DEG)
		return Lots2.domslords[sign]


	def printLots(self):
		print ('')
		num = len(self.data)
		for i in range(num):
			print ('%s %s lon=%f' % (self.data[i][Lots2.NAME], self.data[i][Lots2.FORMULA], self.data[i][Lots2.LONG]))





