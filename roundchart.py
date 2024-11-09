import math
from tkinter import *
from tkinter import font
import houses
import planet
import planets
import chtime
import chart
import options
import lots
import common
import texts
import util


class RoundChart:
	DEG1 = math.pi/180
	DEG5 = math.pi/36
	DEG10 = math.pi/18
	DEG30 = math.pi/6

	SMALL_SIZE = 400
	MEDIUM_SIZE = 600

	SATURN = 0
	JUPITER = 1
	MARS = 2
	SUN = 3
	VENUS = 4
	MERCURY = 5
	MOON = 6
	ANODE = 7
	LOTS = 8
	FORTUNE = 8
	SPIRIT= 9
	EROS = 10
	VICTORY = 11
	NECESSITY = 12
	COURAGE = 13
	NEMESIS = 14
	SYZYGY = 15


	def __init__(self, parent, chrt, opts, wndsize, chrt2=None):
		self.parent = parent
#		self.chart = chrt
#		self.options = opts
#		self.w, self.h = wndsize

		self.bw = False
		bkg_rgb = util.getRGBTxt(opts.clrbackground) 
		self.can = Canvas(self.parent, bd=0, highlightthickness=0, bg=bkg_rgb)
		self.drawCanvas(chrt, opts, wndsize, chrt2)


	def drawCanvas(self, chrt, opts, wndsize, chrt2=None):
		self.chart = chrt
		self.options = opts
		self.chart2 = chrt2
		self.can.delete("all")
		self.w, self.h = wndsize
		self.chartsize = min(self.w, self.h)
		self.maxradius = self.chartsize/2
		self.center = (self.w/2, self.h/2)

		self.arrowlen = 0.04
		self.retrdiff = 0.01
		self.deg01510len = 0.01

		if ((chrt.full and opts.outer != options.Options.NONE) or chrt2 != None):
			self.symbolSize = self.maxradius/18
			self.signSize = self.maxradius/20
			self.outerplanetsectorlen = 0.12
			self.planetsectorlen = 0.15
			self.signsectorlen = self.planetsectorlen
			self.signoffs = (self.signsectorlen/2.0)*self.maxradius
			self.planetoffs = (self.planetsectorlen/2.0)*self.maxradius
			self.planetlinelen = 0.03
			self.rHousesectorlen = 0.06
			self.rOuterMax = self.maxradius*0.97
			if (self.options.hsys != 0):
				self.rOuterHouseName = self.rOuterMax-(self.rHousesectorlen*self.maxradius)/2.0
				self.rOuterHouse = self.rOuterMax-self.rHousesectorlen*self.maxradius
				self.r30 = self.rOuterHouse-self.outerplanetsectorlen*self.maxradius
			else:
				self.r30 = self.rOuterMax-self.outerplanetsectorlen*self.maxradius
				self.rOuterASCMC = self.maxradius*0.92

			self.rOuterPlanet = self.r30+self.planetoffs
			self.rOuterASCMC = self.maxradius*0.92
			self.rOuterArrow = self.rOuterASCMC+self.arrowlen*self.maxradius
			self.rOuterLine = self.r30+self.planetlinelen*self.maxradius
			self.rOuterRetr = self.rOuterLine+self.maxradius*self.retrdiff
			self.rOuter0 = self.r30
			self.rOuter1 = self.rOuter0-self.deg01510len*self.maxradius
			self.rOuter5 = self.rOuter1-self.deg01510len*self.maxradius
			self.rOuter10 = self.rOuter5-self.deg01510len*self.maxradius
			self.rOuterMin = self.maxradius*0.78
			self.rSign = self.r30-self.signoffs
			self.r0 = self.r30-self.signsectorlen*self.maxradius
			self.r1 = self.r0+self.deg01510len*self.maxradius
			self.r5 = self.r1+self.deg01510len*self.maxradius
			self.r10 = self.r5+self.deg01510len*self.maxradius
			self.rASCMC = self.rSign
			self.rArrow = self.rASCMC+self.arrowlen*self.maxradius

			self.rBounds = self.r0
			self.boundssectorlen = 0.0
			if (self.options.showboundsround):
				self.boundssectorlen = 0.08
			self.boundsoffs = (self.boundssectorlen/2.0)*self.maxradius
			self.rBoundsPlanet = self.r0-self.boundsoffs#
			self.rInner = self.rBounds-self.boundssectorlen*self.maxradius

			self.rLLine = self.rInner-self.planetlinelen*self.maxradius #line between zodiacpos & planet
			self.rPlanet = self.rInner-self.planetoffs
			self.rPosDeg = self.rInner-self.planetsectorlen*self.maxradius
			self.rPosMin = self.rPosDeg-0.05*self.maxradius
			self.rRetr = self.rPosMin-0.05*self.maxradius

			poscusps = 0.36
			if (self.options.showboundsround):
				poscusps = 0.28

			self.rPosCusps = self.maxradius*poscusps
			self.rPosCuspsMin = self.rPosCusps-self.maxradius*0.05

			baseoffset = 0.0
			if (self.options.showboundsround):
				baseoffset = self.maxradius*0.08

			self.rBase = self.maxradius*0.30-baseoffset
			self.rHouse = self.rBase+self.rHousesectorlen*self.maxradius
			self.rHouseName = self.rBase+(self.rHousesectorlen*self.maxradius)/2.0
		else:
			self.symbolSize = self.maxradius/14
			self.signSize = self.maxradius/12
			self.signsectorlen = 0.16
			self.planetsectorlen = 0.18
			self.planetoffs = (self.planetsectorlen/2.0)*self.maxradius
			self.planetlinelen = 0.03
			self.rHousesectorlen = 0.08
			self.r30 = self.maxradius*0.96
			self.signoffs = (self.signsectorlen/2.0-0.02)*self.maxradius
			self.rSign = self.r30-self.signoffs
			self.rASCMC = self.maxradius*0.88
			self.rArrow = self.rASCMC+self.arrowlen*self.maxradius
			self.r0 = self.r30-self.signsectorlen*self.maxradius
			self.r1 = self.r0+self.deg01510len*self.maxradius
			self.r5 = self.r1+self.deg01510len*self.maxradius
			self.r10 = self.r5+self.deg01510len*self.maxradius

			self.rBounds = self.r0
			self.boundssectorlen = 0.0
			if (self.options.showboundsround):
				self.boundssectorlen = 0.08
			self.boundsoffs = (self.boundssectorlen/2.0)*self.maxradius
			self.rBoundsPlanet = self.r0-self.boundsoffs#
			self.rInner = self.rBounds-self.boundssectorlen*self.maxradius

			self.rLLine = self.rInner-self.planetlinelen*self.maxradius #line between zodiacpos & planet
			self.rPlanet = self.rInner-self.planetoffs
			self.rPosDeg = self.rInner-self.planetsectorlen*self.maxradius
			self.rPosMin = self.rPosDeg-0.06*self.maxradius
			self.rRetr = self.rPosMin-0.06*self.maxradius

			poscusps = 0.42	
			if (self.options.showboundsround):
				poscusps = 0.35

			self.rPosCusps = self.maxradius*poscusps
			self.rPosCuspsMin = self.rPosCusps-self.maxradius*0.05

			baseoffset = 0.0
			if (self.options.showboundsround):
				baseoffset = self.maxradius*0.08

			self.rBase = self.maxradius*0.30-baseoffset
			self.rHouse = self.rBase+self.rHousesectorlen*self.maxradius
			self.rHouseName = self.rBase+(self.rHousesectorlen*self.maxradius)/2.0

		self.smallsymbolSize = 2*self.symbolSize/3

		self.dataTxtSize = self.maxradius/26
		self.dataTxtSize2 = self.maxradius/34

		self.fntSymbol = font.Font(family='Valens', size=int(self.symbolSize))
		self.fntSmallSymbol = font.Font(family='Valens', size=int(self.smallsymbolSize))
		self.fntSymbolSigns = font.Font(family='Valens', size=int(self.signSize))
		self.fntText = font.Font(family='Helvetica', size=int(self.symbolSize/2))
		self.fntAntisText = font.Font(family='Helvetica', size=int(self.symbolSize))
		self.fntDodecText = font.Font(family='Helvetica', size=int(self.symbolSize))
		self.fntRetr = font.Font(family='Valens', size=int(self.symbolSize/2))
		self.fntRetrOuter = font.Font(family='Valens', size=int(self.symbolSize/4))
		self.fntSmallTextOuter = font.Font(family='Helvetica', size=int(self.symbolSize/4))
		self.fntSmallText2 = font.Font(family='Helvetica', size=int(self.symbolSize/3))
		self.fntSymbolData = font.Font(family='Valens', size=int(5*self.dataTxtSize/4))
		self.fntSymbolData2 = font.Font(family='Valens', size=int(self.dataTxtSize2))
		self.fntDataText = font.Font(family='Helvetica', size=int(self.dataTxtSize))
		self.fntDataText2 = font.Font(family='Helvetica', size=int(self.dataTxtSize2))
		self.deg_symbol = '\u00b0'

		self.black_rgb = util.getRGBTxt((0, 0, 0))
		self.white_rgb = util.getRGBTxt((255, 255, 255))
		bkg_rgb = self.white_rgb
		if (not self.bw):
			bkg_rgb = util.getRGBTxt(opts.clrbackground)
		self.can.configure(bg=bkg_rgb)

		bkg_rgb = self.white_rgb
		if (not self.bw):
			bkg_rgb = util.getRGBTxt(opts.clrbackground)
		self.can.configure(bg=bkg_rgb)

		self.drawCircles()
		self.drawSigns()

		if (self.options.showboundsround):
			self.drawBoundsLines()
			self.drawBounds()

		if (self.options.hsys != 0):
			self.drawHouses(self.chart.houses, self.rBase, self.rInner)
			self.drawHouseNames(self.chart, self.rHouseName)
			if (self.chart2 != None):
				self.drawHouses(self.chart2.houses, self.r30, self.rOuterMax)
				self.drawHouseNames(self.chart2, self.rOuterHouseName)

		self.drawAscMC(self.chart.houses.ascmc, self.rBase, self.rASCMC, self.rArrow)
		if (self.chart2 != None):
			self.drawAscMC(self.chart2.houses.ascmc, self.rOuterMin, self.rOuterASCMC, self.rOuterArrow)

		if (self.options.showdata):
			self.drawData(self.chart)

		if (self.options.hsys != 0 and self.options.showcuspspos):
			self.drawCuspsPos(self.chart.houses.cusps)

		lotclrs = (self.options.clrplanets[planets.Planets.MOON], self.options.clrplanets[planets.Planets.SUN], self.options.clrplanets[planets.Planets.VENUS], self.options.clrplanets[planets.Planets.JUPITER], self.options.clrplanets[planets.Planets.MERCURY], self.options.clrplanets[planets.Planets.MARS], self.options.clrplanets[planets.Planets.SATURN])

		#draw planets, lots and syzygy
		#calc shift of planets (in order to avoid overlapping)
		lons = []
		objs = []
		rets = []
		fnts = []
		clrs = []
		for i in range(planets.Planets.BODIES_NUM-1):
			lons.append(self.chart.planets.planets[i].data[planet.Planet.LON])	
			objs.append(common.common.planets[i])
			rets.append(self.chart.planets.planets[i].data[planet.Planet.SPLON] < 0.0)
			fnts.append(self.fntSymbol)
			clrs.append(self.options.clrplanets[i])

		num = len(self.options.lots)
		for i in range(num):
			if (self.options.lots[i]):
				lon = self.chart.lots.data[i]
				lons.append(lon)
				objs.append(common.common.lots[i])
				rets.append(False)
				fnts.append(self.fntSymbol)
				clrs.append(lotclrs[i])

		if (self.options.syzygy):
			lon = self.chart.syzygy.lon
			lons.append(lon)
			objs.append(common.common.syzygy)
			rets.append(False)
			fnts.append(self.fntSymbol)
			clrs.append(self.options.clrsigns)

#		inorder = self.qsort(lons)
		idorder = self.getIdOrder(lons)
		shift = self.arrangeObjs(objs, lons, fnts, idorder, self.rPlanet)
		self.drawObjLines(shift, lons, self.rInner, self.rLLine)
		self.drawSymbols(shift, lons, objs, rets, fnts, clrs, self.rPlanet, self.rRetr)

		#outer
		lons2 = []
		objs2 = []
		rets2 = []
		fnts2 = []
		clrs2 = []
		if (self.chart2 != None):
			for i in range(planets.Planets.BODIES_NUM-1):
				lons2.append(self.chart2.planets.planets[i].data[planet.Planet.LON])	
				objs2.append(common.common.planets[i])
				rets2.append(self.chart2.planets.planets[i].data[planet.Planet.SPLON] < 0.0)
				fnts2.append(self.fntSymbol)
				clrs2.append(self.options.clrplanets[i])

			num = len(self.options.lots)
			for i in range(num):
				if (self.options.lots[i]):
					lon = self.chart2.lots.data[i]
					lons2.append(lon)
					objs2.append(common.common.lots[i])
					rets2.append(False)
					fnts2.append(self.fntSymbol)
					clrs2.append(lotclrs[i])

			if (self.options.syzygy):
				lon = self.chart2.syzygy.lon
				lons2.append(lon)
				objs2.append(common.common.syzygy)
				rets2.append(False)
				fnts2.append(self.fntSymbol)
				clrs2.append(self.options.clrsigns)

			idorder2 = self.getIdOrder(lons2)
			shift2 = self.arrangeObjs(objs2, lons2, fnts2, idorder2, self.rOuterPlanet)
		else:
			if (self.chart.full and self.options.outer != options.Options.NONE):
				if (self.options.outer == options.Options.ANTIS):
					artxt = (texts.txtscommon['AntAsc'], texts.txtscommon['AntMC'])
					for i in range(2):
						lons2.append(self.chart.antis.ascmclons[i])
						objs2.append(artxt[i])
						rets2.append(False)
						fnts2.append(self.fntAntisText)
						clrs2.append(self.options.clrtexts)

					for i in range(planets.Planets.BODIES_NUM-1):
						lons2.append(self.chart.antis.plslons[i])
						objs2.append(common.common.planets[i])
						rets2.append(self.chart.planets.planets[i].data[planet.Planet.SPLON] < 0.0)
						fnts2.append(self.fntSymbol)
						clrs2.append(self.options.clrplanets[i])

					num = len(self.options.lots)
					for i in range(num):
						if (self.options.lots[i]):
							lons2.append(self.chart.antis.lotslons[i])
							objs2.append(common.common.lots[i])
							rets2.append(False)
							fnts2.append(self.fntSymbol)
							clrs2.append(lotclrs[i])

					if (self.options.syzygy):
						lon = self.chart.antis.syzlon
						lons2.append(lon)
						objs2.append(common.common.syzygy)
						rets2.append(False)
						fnts2.append(self.fntSymbol)
						clrs2.append(self.options.clrsigns)

					idorder2 = self.getIdOrder(lons2)
					shift2 = self.arrangeObjs(objs2, lons2, fnts2, idorder2, self.rOuterPlanet)

				elif (self.options.outer == options.Options.DODEC):
					artxt = (texts.txtscommon['AntAsc'], texts.txtscommon['AntMC'])
					for i in range(2):
						lon = self.chart.dodec.ascmclons[i]
						if (self.options.ayanamsa != 0):
							lon += self.chart.ayanamsa
							lon = util.normalize(lon)					
						lons2.append(lon)
						objs2.append(artxt[i])
						rets2.append(False)
						fnts2.append(self.fntDodecText)
						clrs2.append(self.options.clrtexts)

					for i in range(planets.Planets.BODIES_NUM-1):
						lon = self.chart.dodec.plslons[i]
						if (self.options.ayanamsa != 0):
							lon += self.chart.ayanamsa
							lon = util.normalize(lon)					

						lons2.append(lon)
						objs2.append(common.common.planets[i])
						rets2.append(self.chart.planets.planets[i].data[planet.Planet.SPLON] < 0.0)
						fnts2.append(self.fntSymbol)
						clrs2.append(self.options.clrplanets[i])

					num = len(self.options.lots)
					for i in range(num):
						if (self.options.lots[i]):
							lon = self.chart.dodec.lotslons[i]
							if (self.options.ayanamsa != 0):
								lon += self.chart.ayanamsa
								lon = util.normalize(lon)					
							lons2.append(lon)
							objs2.append(common.common.lots[i])
							rets2.append(False)
							fnts2.append(self.fntSymbol)
							clrs2.append(lotclrs[i])

					if (self.options.syzygy):
						lon = self.chart.dodec.syzlon
						if (self.options.ayanamsa != 0):
							lon += self.chart.ayanamsa
							lon = util.normalize(lon)					
						lons2.append(lon)
						objs2.append(common.common.syzygy)
						rets2.append(False)
						fnts2.append(self.fntSymbol)
						clrs2.append(self.options.clrsigns)

					idorder2 = self.getIdOrder(lons2)
					shift2 = self.arrangeObjs(objs2, lons2, fnts2, idorder2, self.rOuterPlanet)

		if (self.chart2 != None or (self.chart.full and self.options.outer != options.Options.NONE)):
			self.drawObjLines(shift2, lons2, self.r30, self.rOuterLine)
			self.drawSymbols(shift2, lons2, objs2, rets2, fnts2, clrs2, self.rOuterPlanet, self.rOuterRetr, True)


	def drawCircles(self):
		frameclr = util.getRGBTxt(self.options.clrframe)
		if (self.bw):
			frameclr = self.black_rgb

		w = 3
		if (self.chartsize <= RoundChart.SMALL_SIZE):
			w = 1
		elif (self.chartsize <= RoundChart.MEDIUM_SIZE):
			w = 2

		#rOuterMax and rOuterHouse (for outer housenames)
		if (self.chart2 != None and self.options.hsys != 0):
			r = self.rOuterMax
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)
			r = self.rOuterHouse
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)

		#r30 circle
		if (self.chart2 != None or (self.chart.full and self.options.outer != options.Options.NONE)):
			r = self.r30
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=w)

			#Outer 10, 5, 1-circle
			r = self.rOuter10
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)
		else:
			r = self.r30
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)

		#r10 Circle
		r = self.r10
		self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)

		#r0 Circle
		if (self.options.showboundsround):
			r = self.r0
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)

		r = self.rInner
		self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=w)

		#rHouse Circle
		if (self.options.hsys != 0):
			r = self.rHouse
			self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=frameclr, width=1)

		#Base Circle
		ascmcclr = util.getRGBTxt(self.options.clrAscMC)
		if (self.bw):
			ascmcclr = self.black_rgb
		wi = w
		if (w == 1):
			wi = 2

		r = self.rBase
		self.can.create_oval(self.center[0]-r, self.center[1]-r, self.center[0]+r+1, self.center[1]+r+1, outline=ascmcclr, width=wi)

		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			asclon -= self.chart.ayanamsa
			asclon = util.normalize(asclon)

		#30-degs
		self.drawLines(RoundChart.DEG30, asclon, self.rInner, self.r30, w, frameclr)

		#10-degs
		w = 2
		if (self.chartsize <= RoundChart.MEDIUM_SIZE):
			w = 1
		self.drawLines(RoundChart.DEG10, asclon, self.r0, self.r10, w, frameclr)

		#5-degs
		self.drawLines(RoundChart.DEG5, asclon, self.r0, self.r5, w, frameclr)

		#1-degs
		self.drawLines(RoundChart.DEG1, asclon, self.r0, self.r1, 1, frameclr)

		#Outer 10, 5, 1 -degs
		if (self.chart2 != None or (self.chart.full and self.options.outer != options.Options.NONE)):
			#10-degs
			self.drawLines(RoundChart.DEG10, asclon, self.rOuter0, self.rOuter10, w, frameclr)

			#5-degs
			self.drawLines(RoundChart.DEG5, asclon, self.rOuter0, self.rOuter5, w, frameclr)

			#1-degs
			self.drawLines(RoundChart.DEG1, asclon, self.rOuter0, self.rOuter1, 1, frameclr)


	def drawLines(self, deg, shift, r1, r2, w, clr):
		cx = self.center[0]+1
		cy = self.center[1]+1
		i = math.pi+math.radians(shift)
		while (i>-math.pi+math.radians(shift)):
			x1 = cx+math.cos(i)*r1
			y1 = cy+math.sin(i)*r1
			x2 = cx+math.cos(i)*r2
			y2 = cy+math.sin(i)*r2

			line = self.can.create_line(x1, y1, x2, y2, fill=clr, width=w)
			i -= deg


	def drawBoundsLines(self):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrframe)
		if (self.bw):
			clr = self.black_rgb
		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			asclon -= self.chart.ayanamsa
			asclon = util.normalize(asclon)

		shift = math.radians(asclon)
		signdeg = float(chart.Chart.SIGN_DEG)
		num = len(self.options.bounds[self.options.selbounds])
		subnum = len(self.options.bounds[self.options.selbounds][0])
		sign = 0.0
		for i in range(num):
			deg = sign
			for j in range(subnum):
				deg += float(self.options.bounds[self.options.selbounds][i][j][1])

				x1 = cx+math.cos(math.pi+shift-math.radians(deg))*self.rBounds
				y1 = cy+math.sin(math.pi+shift-math.radians(deg))*self.rBounds
				x2 = cx+math.cos(math.pi+shift-math.radians(deg))*self.rInner
				y2 = cy+math.sin(math.pi+shift-math.radians(deg))*self.rInner

				line = self.can.create_line(x1, y1, x2, y2, fill=clr, width=1)

			sign += signdeg


	def drawBounds(self):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrsigns)
		if (self.bw):
			clr = self.black_rgb

		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			asclon -= self.chart.ayanamsa
			asclon = util.normalize(asclon)

		shift = math.radians(asclon)
		signdeg = float(chart.Chart.SIGN_DEG)
		num = len(self.options.bounds[self.options.selbounds])
		subnum = len(self.options.bounds[self.options.selbounds][0])
		sign = 0.0
		for i in range(num):
			deg = sign
			for j in range(subnum):
				pldeg = deg+float(self.options.bounds[self.options.selbounds][i][j][1])/2.0
				deg += float(self.options.bounds[self.options.selbounds][i][j][1])

				x = cx+math.cos(math.pi+shift-math.radians(pldeg))*self.rBoundsPlanet
				y = cy+math.sin(math.pi+shift-math.radians(pldeg))*self.rBoundsPlanet

				txtId = self.can.create_text(x, y, font=self.fntSmallSymbol, text=common.common.planets[self.options.bounds[self.options.selbounds][i][j][0]], fill=clr)

			sign += signdeg


	def drawSigns(self):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrsigns) 
		if (self.bw):
			clr = self.black_rgb
		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			asclon -= self.chart.ayanamsa
			asclon = util.normalize(asclon)
		i = math.pi+math.radians(asclon)-RoundChart.DEG30/2

		signs = common.common.signs

		j = 0
		while (j < chart.Chart.SIGN_NUM):
			x = cx+math.cos(i)*self.rSign
			y = cy+math.sin(i)*self.rSign
			txtId = self.can.create_text(x, y, font=self.fntSymbolSigns, text=signs[j], fill=clr)
			i -= RoundChart.DEG30
			j += 1


	def drawHouses(self, chouses, r1, r2):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrframe)
		if (self.bw):
			clr = self.black_rgb
		asc = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			dif = math.radians(util.normalize(asc-chouses.cusps[i]))
			x1 = cx+math.cos(math.pi+dif)*r1
			y1 = cy+math.sin(math.pi+dif)*r1
			x2 = cx+math.cos(math.pi+dif)*r2
			y2 = cy+math.sin(math.pi+dif)*r2
			line = self.can.create_line(x1, y1, x2, y2, fill=clr, width=1)


	def drawHouseNames(self, chrt, rHouseNames):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrframe)
		if (self.bw):
			clr = self.black_rgb
		asc = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			width = 0.0
			if (i != houses.Houses.HOUSE_NUM):
				width = chrt.houses.cusps[i+1]-chrt.houses.cusps[i]
			else:
				width = chrt.houses.cusps[1]-chrt.houses.cusps[houses.Houses.HOUSE_NUM]

			width = util.normalize(width)
			halfwidth = math.radians(width/2.0)
			dif = math.radians(util.normalize(asc-chrt.houses.cusps[i]))
			
			x = cx+math.cos(math.pi+dif-halfwidth)*rHouseNames
			y = cy+math.sin(math.pi+dif-halfwidth)*rHouseNames
			if (i == 1 or i == 2):
				xoffs = 0
				yoffs = self.symbolSize/4
				if (i == 2):
					xoffs = self.symbolSize/8
			else:
				xoffs = self.symbolSize/4
				yoffs = self.symbolSize/4

			txtId = self.can.create_text(x, y, font=self.fntText, text=common.common.housenames[i-1], fill=clr)
	

	def drawAscMC(self, ascmc, r1, r2, rArrow):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrAscMC)
		if (self.bw):
			clr = self.black_rgb

		w = 3
		if (self.chartsize <= RoundChart.MEDIUM_SIZE):
			w = 2

		for i in range(4):
			ang = math.pi+math.radians(self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON])
			if (i == 0):
				ang -= math.radians(ascmc[houses.Houses.ASC][houses.Houses.LON])
			if (i == 1):
				ang -= math.radians(ascmc[houses.Houses.ASC][houses.Houses.LON])+math.pi
			if (i == 2):
				ang -= math.radians(ascmc[houses.Houses.MC][houses.Houses.LON])
			if (i == 3):
				ang -= math.radians(ascmc[houses.Houses.MC][houses.Houses.LON])+math.pi

			x1 = cx+math.cos(ang)*r1
			y1 = cy+math.sin(ang)*r1
			x2 = cx+math.cos(ang)*r2
			y2 = cy+math.sin(ang)*r2
			if (i == 0 or i == 2):
				line = self.can.create_line(x1, y1, x2, y2, fill=clr, width=w, arrow='last')
			else:
				line = self.can.create_line(x1, y1, x2, y2, fill=clr, width=w)


	def drawData(self, chrt):
		juliantxt = ''
		bctxt = ''
		if (chrt.time.cal == chtime.Time.JULIAN):
			juliantxt = texts.txtscommon['J']
		if (chrt.time.bc):
			bctxt = texts.txtscommon['BC']
		datetxt = texts.months[chrt.time.omonth-1]+' '+str(chrt.time.oday)+', '+str(chrt.time.oyear)+' '+juliantxt+' '+bctxt
		timetxt = str(chrt.time.hour).zfill(2)+':'+str(chrt.time.minute).zfill(2)+':'+str(chrt.time.second).zfill(2)+' '+texts.zoneList[chrt.time.zt]
		placetxt = chrt.place.placename
		dirlontxt = texts.txtscommon['E']
		if (not chrt.place.east):
			dirlontxt = texts.txtscommon['W']
		dirlattxt = texts.txtscommon['N']
		if (not chrt.place.north):
			dirlattxt = texts.txtscommon['S']
		coordtxt = (str(chrt.place.deglon)).zfill(2)+self.deg_symbol+(str(chrt.place.minlon)).zfill(2)+"'"+dirlontxt+'  '+(str(chrt.place.deglat)).zfill(2)+self.deg_symbol+(str(chrt.place.minlat)).zfill(2)+"'"+dirlattxt
		nametxt = chrt.name
		typetxt = texts.typeList[chrt.htype]
		ayantxt = texts.txtsayanamsa['Tropical']
		if (self.options.ayanamsa != 0):
			ayantxt = texts.ayanamsaList[self.options.ayanamsa]
		hstxt = texts.hsystemList[self.options.hsys]
		ar = (6, 2, 5, 1, 4, 0, 3)	
		daysym = common.common.planets[ar[chrt.time.ph.weekday]]
		hoursym = common.common.planets[chrt.time.ph.planetaryhour]
		dayhourtxt = daysym+'   '+hoursym

		fntsize = self.dataTxtSize
		fnttxt = self.fntDataText
		fntsym = self.fntSymbolData
		offsy = self.chartsize/12
		if (self.options.showboundsround):
			fnttxt = self.fntDataText2
			fntsym = self.fntSymbolData2
			fntsize = self.dataTxtSize2
			offsy = self.chartsize/16

		SPACE = fntsize/8
		LINE_HEIGHT = (SPACE+fntsize+SPACE)

		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrtexts)
		if (self.bw):
			clr = self.black_rgb
		x = cx
		y = cy-offsy

		txtId = self.can.create_text(x, y, font=fnttxt, text=datetxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+LINE_HEIGHT, font=fnttxt, text=timetxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+2*LINE_HEIGHT, font=fnttxt, text=placetxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+3*LINE_HEIGHT, font=fnttxt, text=coordtxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+4*LINE_HEIGHT, font=fnttxt, text=nametxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+5*LINE_HEIGHT, font=fnttxt, text=typetxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+6*LINE_HEIGHT, font=fnttxt, text=ayantxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+7*LINE_HEIGHT, font=fnttxt, text=hstxt, justify='center', fill=clr)
		txtId = self.can.create_text(x, y+8*LINE_HEIGHT, font=fntsym, text=dayhourtxt, justify='center', fill=clr)


	def drawCuspsPos(self, cusps):
		cx = self.center[0]
		cy = self.center[1]
		clr = util.getRGBTxt(self.options.clrtexts)
		if (self.bw):
			clr = self.black_rgb
		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		for i in range (1, houses.Houses.HOUSE_NUM+1):
			lon = cusps[i]
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)
			(d, m, s) = util.decToDeg(lon)
			d = d%chart.Chart.SIGN_DEG
			
			degtxt = str(d).zfill(2)+self.deg_symbol
			x = cx+math.cos(math.pi+math.radians(asclon-cusps[i]))*self.rPosCusps
			y = cy+math.sin(math.pi+math.radians(asclon-cusps[i]))*self.rPosCusps
			txtId = self.can.create_text(x, y, font=self.fntText, text=degtxt, fill=clr)

			mintxt = str(m).zfill(2)+"'"
			x = cx+math.cos(math.pi+math.radians(asclon-cusps[i]))*self.rPosCuspsMin
			y = cy+math.sin(math.pi+math.radians(asclon-cusps[i]))*self.rPosCuspsMin
			txtId = self.can.create_text(x, y, font=self.fntSmallText2, text=mintxt.zfill(2), fill=clr)


	def drawObjLines(self, objshift, lons, r1, r2):
		clr = util.getRGBTxt(self.options.clrframe)
		if (self.bw):
			clr = self.black_rgb
		w = 2
		if (self.chartsize <= RoundChart.MEDIUM_SIZE):
			w = 1

		num = len(lons)
		for i in range(num):
			self.drawPlanetLine(objshift, lons[i], i, r1, r2, clr, w)


	def drawPlanetLine(self, objshift, lon, iD, r1, r2, clr, w):
		cx = self.center[0]
		cy = self.center[1]

		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		x1 = cx+math.cos(math.pi+math.radians(asclon-lon))*r1
		y1 = cy+math.sin(math.pi+math.radians(asclon-lon))*r1
		x2 = cx+math.cos(math.pi+math.radians(asclon-lon-objshift[iD]))*r2
		y2 = cy+math.sin(math.pi+math.radians(asclon-lon-objshift[iD]))*r2
		line = self.can.create_line(x1, y1, x2, y2, fill=clr, width=w)


	def getIdOrder(self, lons):
		idorder = [] #this could be passed, it would be faster e.g. pl: [0, 1, 2, 3, 4, 5...]
		order = lons[:]
		length = len(lons)
		for i in range(length):
			idorder.append(i)

		#Bubble sort (very slow)
		for j in range(length):
			for i in range(length-1):
				if (order[i] > order[i+1]):
					tmp = order[i]
					order[i] = order[i+1]
					order[i+1] = tmp
					tmp = idorder[i]
					idorder[i] = idorder[i+1]
					idorder[i+1] = tmp
			
		return idorder


	def drawSymbols(self, shift, lons, objs, rets, fnts, clrs, radius, radiusR, outer=False):
		cx = self.center[0]
		cy = self.center[1]
		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		num = len(lons)
		for i in range(num):
			x = cx+math.cos(math.pi+math.radians(asclon-lons[i]-shift[i]))*radius
			y = cy+math.sin(math.pi+math.radians(asclon-lons[i]-shift[i]))*radius	
			
			clr = util.getRGBTxt(clrs[i])
			if (self.bw):
				clr = self.black_rgb

			txtId = self.can.create_text(x, y, font=fnts[i], text=objs[i], fill=clr)

			retrfont = self.fntRetr
			if (not outer):
				#Position
				lon = lons[i]
				if (self.options.ayanamsa != 0):
					lon -= self.chart.ayanamsa
					lon = util.normalize(lon)
				(d, m, s) = util.decToDeg(lon)
				d = d%chart.Chart.SIGN_DEG
#				d, m = util.roundDeg(d%chart.Chart.SIGN_DEG, m, s)
				
				degtxt = str(d).zfill(2)+self.deg_symbol
				x = cx+math.cos(math.pi+math.radians(asclon-lons[i]-shift[i]))*self.rPosDeg
				y = cy+math.sin(math.pi+math.radians(asclon-lons[i]-shift[i]))*self.rPosDeg
				txtId = self.can.create_text(x, y, font=self.fntText, text=degtxt, fill=clr)

				mintxt = str(m).zfill(2)+"'"
				x = cx+math.cos(math.pi+math.radians(asclon-lons[i]-shift[i]))*self.rPosMin
				y = cy+math.sin(math.pi+math.radians(asclon-lons[i]-shift[i]))*self.rPosMin
				txtId = self.can.create_text(x, y, font=self.fntSmallText2, text=mintxt.zfill(2), fill=clr)
			else:
				retrfont = self.fntRetrOuter

			#Retrograde
			if (rets[i]):
				x = cx+math.cos(math.pi+math.radians(asclon-lons[i]-shift[i]))*radiusR
				y = cy+math.sin(math.pi+math.radians(asclon-lons[i]-shift[i]))*radiusR

				txtId = self.can.create_text(x, y, font=retrfont, text=common.common.retr, fill=clr)


	def arrangeObjs(self, objs, lons, fnts, idorder, rObj):
		'''Arranges Objects so they won't overlap each other'''

		objnum = len(objs)
		objshift = []
		for i in range(objnum):
			objshift.append(0.0)

		self.w1 = self.fntSymbol.measure('D')
		self.w2 = self.fntSymbol.measure('D')
		self.h1 = self.h2 = self.fntSymbol.metrics('linespace')

		#doArrange arranges consecutive two objects only(0 and 1, 1 and 2, ...), this is why we need to do it objnum+1 times
		shifted = True
		while(shifted):
			shifted = self.doArrange(objshift, objs, lons, fnts, idorder, rObj)

		#Arrange 360-0 transition also
		#We only shift forward at 360-0
		shifted = self.doShift(objnum-1, 0, objs[idorder[objnum-1]], objs[idorder[0]], objshift, lons, fnts, idorder, rObj, True)

		if (shifted):
				while(shifted):
					shifted = self.doArrange(objshift, objs, lons, fnts, idorder, rObj, True)
		#check if beyond (not overlapping but beyond)
		else:
			if (lons[idorder[objnum-1]] > 300.0 and lons[idorder[0]] < 60.0):
				lon1 = lons[idorder[objnum-1]]+objshift[idorder[objnum-1]]
				lon2 = lons[idorder[0]]+360.0+objshift[idorder[0]]

				if (lon1 > lon2):
					dist = lon1-lon2
					objshift[idorder[0]] += dist
					self.doShift(objnum-1, 0, objs[idorder[objnum-1]], objs[idorder[0]], objshift, lons, fnts, idorder, rObj, True)

					for i in range(objnum-1):
						lon1 = lons[idorder[i]]+objshift[idorder[i]]
						lon2 = lons[idorder[i+1]]+objshift[idorder[i+1]]
						if (lon1 < 180.0 and lon2 < 180.0):
							if (lon1 > lon2):
								dist = lon1-lon2
								objshift[idorder[i+1]] += dist
								self.doShift(i, i+1, objs[idorder[i]], objs[idorder[i+1]], objshift, lons, fnts, idorder, rObj, True)
							else:
								break
						else:
							break

					for i in range(objnum):
						self.doArrange(objshift, objs, lons, fnts, idorder, rObj, True)

		return objshift[:]


	def doArrange(self, objshift, objs, lons, fnts, idorder, rObj, forward = False):
		objnum = len(objshift)
		shifted = False

		for i in range(objnum-1):
			if(self.doShift(i, i+1, objs[idorder[i]], objs[idorder[i+1]], objshift, lons, fnts, idorder, rObj, forward)):
				shifted = True

		return shifted


	def doShift(self, id1, id2, o1, o2, objshift, lons, fnts, idorder, rObj, forward = False):
		cx = self.center[0]
		cy = self.center[1]
		shifted = False

		asclon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		x1 = cx+math.cos(math.pi+math.radians(asclon-lons[idorder[id1]]-objshift[idorder[id1]]))*rObj
		y1 = cy+math.sin(math.pi+math.radians(asclon-lons[idorder[id1]]-objshift[idorder[id1]]))*rObj
		x2 = cx+math.cos(math.pi+math.radians(asclon-lons[idorder[id2]]-objshift[idorder[id2]]))*rObj
		y2 = cy+math.sin(math.pi+math.radians(asclon-lons[idorder[id2]]-objshift[idorder[id2]]))*rObj

		if (len(o1) > 3): #otherwise long texts at the bottom or top of the chart would be pushed to far away due to their width.
			o1 = o1[0:3]
		if (len(o2) > 3):
			o2 = o2[0:3]

		#Unfortunately this would be slow!
#		w1 = fnts[idorder[id1]].measure(o1)
#		w2 = fnts[idorder[id2]].measure(o2)
#		h1 = h2 = fnts[idorder[id2]].metrics('linespace')

		while (self.overlap(x1, y1, self.w1, self.h1, x2, y2, self.w2, self.h2)):
			if (not forward):
				objshift[idorder[id1]] -= 0.1
			objshift[idorder[id2]] += 0.1

			x1 = cx+math.cos(math.pi+math.radians(asclon-lons[idorder[id1]]-objshift[idorder[id1]]))*rObj
			y1 = cy+math.sin(math.pi+math.radians(asclon-lons[idorder[id1]]-objshift[idorder[id1]]))*rObj
			x2 = cx+math.cos(math.pi+math.radians(asclon-lons[idorder[id2]]-objshift[idorder[id2]]))*rObj
			y2 = cy+math.sin(math.pi+math.radians(asclon-lons[idorder[id2]]-objshift[idorder[id2]]))*rObj

			if (not shifted):
				shifted = True

		return shifted


	def overlap(self, x1, y1, w1, h1, x2, y2, w2, h2):
		xoverlap = (x1 <= x2 and x2 <= x1+w1) or (x2 <= x1 and x1 <= x2+w2)
		yoverlap = (y1 <= y2 and y2 <= y1+h1) or (y2 <= y1 and y1 <= y2+h2)

		if (xoverlap and yoverlap):
			return True

		return False




