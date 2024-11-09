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


class HellenisticChart:
#	SMALL_SIZE = 400
#	MEDIUM_SIZE = 600

	ASC = 0
	MC = 1
	BASE = 2
	SATURN = 2
	JUPITER = 3
	MARS = 4
	SUN = 5
	VENUS = 6
	MERCURY = 7
	MOON = 8
	ANODE = 9
	LOTS = 10
	FORTUNE = 10
	SPIRIT= 11
	EROS = 12
	VICTORY = 13
	NECESSITY = 14
	COURAGE = 15
	NEMESIS = 16
	SYZYGY = 17

	MAXSYMBOLNUMPERCOLUM = 6


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
		self.can.delete("all")
		w, h = wndsize
		msi = min(w, h)
		maxradius = msi/2
		cen = (w/2, h/2)
		ratio = 0.9
		if ((chrt.full and opts.outer != options.Options.NONE) or chrt2 != None):
			ratio = 0.75		# max 6
			outerextra12_y2 = 0
			outerextra12_y3 = 0
			outerextra12_y4 = 0
			maxnum = 0
			maxnumleftright = 0
			maxnumtopbottom = 0
			if (chrt2 != None):
				maxnum, maxnumleftright, maxnumtopbottom, ars = self.getMaxSymbolNumPerSigns(chrt2, opts)
			else:
				dat = chrt.antis
				if (opts.outer == options.Options.DODEC):
					dat = chrt.dodec
				maxnum, maxnumleftright, maxnumtopbottom, ars = self.getMaxSymbolNumPerSignsAntisDodec(dat, chrt.ayanamsa, opts)

			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				ratio = 0.65		# 12
				outerextra12_y2 = maxradius/106	# for 12 symbols, i.e. ratio=0.65
				outerextra12_y3 = maxradius/40
				outerextra12_y4 = maxradius/28

		radius = maxradius*ratio
		signsize = int(radius/14)
		plsize = int(radius/16)
		datasize = int(radius/28)
		retrsize = int(radius/36)
		self.xspace = int(radius/50)

		self.black_rgb = util.getRGBTxt((0, 0, 0))
		white_rgb = util.getRGBTxt((255, 255, 255))
		bkg_rgb = white_rgb
		frame_rgb = self.black_rgb
		signs_rgb = self.black_rgb
		if (not self.bw):
			bkg_rgb = util.getRGBTxt(opts.clrbackground)
			frame_rgb = util.getRGBTxt(opts.clrframe) 
			signs_rgb = util.getRGBTxt(opts.clrsigns) 
		self.can.configure(bg=bkg_rgb)

		self.signfont = font.Font(family='Valens', size=signsize)
		self.datafont = font.Font(family='Helvetica', size=datasize)
		self.plfont = font.Font(family='Valens', size=plsize)
		self.retrfont = font.Font(family='Valens', size=retrsize)
		plsize2 = self.plfont.metrics('linespace')

		#vertical lines
		x = cen[0]-radius/3
		y = cen[1]-radius
		line = self.can.create_line(x, y, x, y+2*radius, fill=frame_rgb, width=2)
		x = cen[0]+radius/3
		line = self.can.create_line(x, y, x, y+2*radius, fill=frame_rgb, width=2)

		#horizontal lines
		x = cen[0]-radius
		y = cen[1]-radius/3
		line = self.can.create_line(x, y, x+2*radius, y, fill=frame_rgb, width=2)
		y = cen[1]+radius/3
		line = self.can.create_line(x, y, x+2*radius, y, fill=frame_rgb, width=2)

		#diagonals
		x = cen[0]-radius
		y = cen[1]-radius
		line = self.can.create_line(x, y, x+2*radius/3, y+2*radius/3, fill=frame_rgb, width=2)
		x = cen[0]+radius
		y = cen[1]-radius
		line = self.can.create_line(x, y, x-2*radius/3, y+2*radius/3, fill=frame_rgb, width=2)
		x = cen[0]-radius
		y = cen[1]+radius
		line = self.can.create_line(x, y, x+2*radius/3, y-2*radius/3, fill=frame_rgb, width=2)
		x = cen[0]+radius
		y = cen[1]+radius
		line = self.can.create_line(x, y, x-2*radius/3, y-2*radius/3, fill=frame_rgb, width=2)

		#data
		if (opts.showdata):
			self.drawData(chrt, opts, wndsize, chrt2, ratio)

		#signs
		offs = plsize/2
		signpos = ((cen[0]-radius-offs, cen[1]), (cen[0]-radius-offs, cen[1]+2*radius/3), (cen[0]-2*radius/3, cen[1]+radius+offs), (cen[0], cen[1]+radius+offs), (cen[0]+2*radius/3, cen[1]+radius+offs), (cen[0]+radius+offs, cen[1]+2*radius/3), (cen[0]+radius+offs, cen[1]), (cen[0]+radius+offs, cen[1]-2*radius/3), (cen[0]+2*radius/3, cen[1]-radius-offs), (cen[0], cen[1]-radius-offs), (cen[0]-2*radius/3, cen[1]-radius-offs), (cen[0]-radius-offs, cen[1]-2*radius/3))
		asclon = chrt.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (opts.ayanamsa != 0):
			asclon -= chrt.ayanamsa
			asclon = util.normalize(asclon)					
		ascsign = int(asclon/chart.Chart.SIGN_DEG)
		signsyms = common.common.signs
		hsign = 0 #signFont.cget('size')
		for i in range(ascsign, chart.Chart.SIGN_NUM):
			wsign = 0 #signFont.measure(signsyms[i])
			txtSign = self.can.create_text(signpos[i-ascsign][0]-wsign/2, signpos[i-ascsign][1]-hsign/2, font=self.signfont, text=signsyms[i], fill=signs_rgb)
		for i in range(0, ascsign):
			wsign = 0 #signFont.measure(signsyms[i])
			txtSign = self.can.create_text(signpos[i-ascsign][0]-wsign/2, signpos[i-ascsign][1]-hsign/2, font=self.signfont, text=signsyms[i], fill=signs_rgb)

		#arrays of angular places (e.g. ar1_6: there are 6 symbols in place I)
		#1st place: 
		xorig = cen[0]-3*radius/4
		yorig = cen[1]
		ar1_1 = ((xorig, yorig), )
		ar1_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar1_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar1_4 = ((xorig, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar1_5 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2))
		ar1_6 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar1_7 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar1_8 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar1_9 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar1_10 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar1_11 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar1_12 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-5*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+5*plsize2/2))

		arplace1 = (ar1_1, ar1_2, ar1_3, ar1_4, ar1_5, ar1_6, ar1_7, ar1_8, ar1_9, ar1_10, ar1_11, ar1_12)

		#7th place:
		xorig = cen[0]+3*radius/4-3*plsize
		yorig = cen[1]
		ar7_1 = ((xorig, yorig), )
		ar7_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar7_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar7_4 = ((xorig, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar7_5 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2))
		ar7_6 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar7_7 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar7_8 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar7_9 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar7_10 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar7_11 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar7_12 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-5*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+5*plsize2/2))

		arplace7 = (ar7_1, ar7_2, ar7_3, ar7_4, ar7_5, ar7_6, ar7_7, ar7_8, ar7_9, ar7_10, ar7_11, ar7_12)

		#10st place: 
		xorig = cen[0]-3*plsize/2
		yorig = cen[1]-3*radius/4+plsize2
		ar10_1 = ((xorig, yorig), )
		ar10_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar10_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar10_4 = ((xorig, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar10_5 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2))
		ar10_6 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar10_7 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar10_8 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar10_9 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar10_10 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar10_11 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar10_12 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-5*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+5*plsize2/2))

		arplace10 = (ar10_1, ar10_2, ar10_3, ar10_4, ar10_5, ar10_6, ar10_7, ar10_8, ar10_9, ar10_10, ar10_11, ar10_12)

		#4st place: 
		xorig = cen[0]-3*plsize/2
		yorig = cen[1]+3*radius/4-3*plsize/2
		ar4_1 = ((xorig, yorig), )
		ar4_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar4_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar4_4 = ((xorig, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar4_5 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2))
		ar4_6 = ((xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar4_7 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2))
		ar4_8 = ((xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar4_9 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar4_10 = ((xorig-3*plsize/2, yorig-2*plsize2), (xorig-3*plsize/2, yorig-plsize2), (xorig-3*plsize/2, yorig), (xorig-3*plsize/2, yorig+plsize2), (xorig-3*plsize/2, yorig+2*plsize2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar4_11 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-plsize2), (xorig+3*plsize, yorig), (xorig+3*plsize, yorig+plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar4_12 = ((xorig-3*plsize/2, yorig-5*plsize2/2), (xorig-3*plsize/2, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2/2), (xorig-3*plsize/2, yorig+3*plsize2/2), (xorig-3*plsize/2, yorig+5*plsize2/2), (xorig+3*plsize, yorig-5*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-plsize2/2), (xorig+3*plsize, yorig+plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+5*plsize2/2))

		arplace4 = (ar4_1, ar4_2, ar4_3, ar4_4, ar4_5, ar4_6, ar4_7, ar4_8, ar4_9, ar4_10, ar4_11, ar4_12)

		#12th place
		xorig = cen[0]-3*radius/4-3*plsize/2
		yorig = cen[1]-radius/2-plsize2
		ar12_1 = ((xorig, yorig), )
		ar12_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar12_3 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar12_4 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig-plsize, yorig+2*plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar12_5 = ((xorig-plsize, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig-plsize, yorig+2*plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar12_6 = ((xorig-plsize, yorig-3*plsize2/2), (xorig-plsize, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2), (xorig+5*plsize/2, yorig+plsize2), (xorig-plsize, yorig+2*plsize2), (xorig+3*plsize, yorig+2*plsize2))
		ar12_7 = ((xorig-5*plsize/2, yorig-5*plsize2/2), (xorig-plsize, yorig-3*plsize2/2), (xorig-plsize, yorig-plsize2/2), (xorig-3*plsize/2, yorig+plsize2), (xorig+5*plsize/2, yorig+plsize2), (xorig-plsize, yorig+2*plsize2), (xorig+3*plsize, yorig+2*plsize2))


		arplace12 = (ar12_1, ar12_2, ar12_3, ar12_4, ar12_5, ar12_6, ar12_7)

		#6th place
		xorig = cen[0]+3*radius/4
		yorig = cen[1]+radius/2
		ar6_1 = ((xorig, yorig+plsize2/2), )
		ar6_2 = ((xorig, yorig), (xorig, yorig+plsize2))
		ar6_3 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar6_4 = ((xorig-3*plsize, yorig-plsize2), (xorig+plsize, yorig-plsize2), (xorig, yorig+plsize2/2), (xorig, yorig+3*plsize2/2))
		ar6_5 = ((xorig-3*plsize, yorig-plsize2), (xorig+plsize, yorig-plsize2), (xorig-2*plsize-plsize/4, yorig), (xorig+3*plsize/2, yorig), (xorig, yorig+3*plsize2/2))
		ar6_6 = ((xorig-3*plsize, yorig-plsize2), (xorig+plsize, yorig-plsize2), (xorig-2*plsize-plsize/4, yorig), (xorig+3*plsize/2, yorig), (xorig, yorig+3*plsize2/2), (xorig+3*plsize/2, yorig+3*plsize2))
		ar6_7 = ((xorig-3*plsize, yorig-plsize2), (xorig+plsize, yorig-plsize2), (xorig-2*plsize-plsize/4, yorig), (xorig+3*plsize/2, yorig), (xorig-plsize, yorig+plsize2), (xorig+plsize, yorig+2*plsize2), (xorig+5*plsize/2, yorig+3*plsize2))

		arplace6 = (ar6_1, ar6_2, ar6_3, ar6_4, ar6_5, ar6_6, ar6_7)

		#2nd place
		xorig = cen[0]-3*radius/4-3*plsize/2
		yorig = cen[1]+radius/2+plsize2/2
		ar2_1 = ((xorig, yorig), )
		ar2_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar2_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar2_4 = ((xorig-plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig, yorig), (xorig, yorig+plsize2))
		ar2_5 = ((xorig-plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig, yorig), (xorig, yorig+plsize2), (xorig-plsize, yorig+2*plsize2))
		ar2_6 = ((xorig-plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig+5*plsize/2, yorig-plsize2/2), (xorig-plsize, yorig+plsize2), (xorig-plsize, yorig+2*plsize2))
		ar2_7 = ((xorig-plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig-3*plsize/2, yorig-plsize2/2), (xorig+5*plsize/2, yorig-plsize2/2), (xorig-plsize, yorig+plsize2), (xorig-plsize, yorig+2*plsize2), (xorig-5*plsize/2, yorig+3*plsize2))

		arplace2 = (ar2_1, ar2_2, ar2_3, ar2_4, ar2_5, ar2_6, ar2_7)

		#8th place
		xorig = cen[0]+3*radius/4
		yorig = cen[1]-radius/2-plsize2/2
		ar8_1 = ((xorig, yorig), )
		ar8_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar8_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar8_4 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig-3*plsize, yorig+3*plsize2/2), (xorig+plsize, yorig+3*plsize2/2))
		ar8_5 = ((xorig+plsize, yorig-2*plsize2), (xorig, yorig-plsize2), (xorig, yorig), (xorig-3*plsize, yorig+3*plsize2/2), (xorig+plsize, yorig+3*plsize2/2))
		ar8_6 = ((xorig+plsize, yorig-2*plsize2), (xorig, yorig-plsize2), (xorig-5*plsize/2, yorig+plsize2/2), (xorig+3*plsize/2, yorig+plsize2/2), (xorig-3*plsize, yorig+3*plsize2/2), (xorig+plsize, yorig+3*plsize2/2))
		ar8_7 = ((xorig+5*plsize/2, yorig-3*plsize2), (xorig+plsize, yorig-2*plsize2), (xorig, yorig-plsize2), (xorig-5*plsize/2, yorig+plsize2/2), (xorig+3*plsize/2, yorig+plsize2/2), (xorig-3*plsize, yorig+3*plsize2/2), (xorig+plsize, yorig+3*plsize2/2))

		arplace8 = (ar8_1, ar8_2, ar8_3, ar8_4, ar8_5, ar8_6, ar8_7)

		#3th place
		xorig = cen[0]-radius/2-plsize
		yorig = cen[1]+3*radius/4
		ar3_1 = ((xorig, yorig), )
		ar3_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar3_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar3_4 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig-7*plsize/2, yorig+3*plsize2/2), (xorig+plsize/2, yorig+3*plsize2/2))
		ar3_5 = ((xorig+plsize-plsize/4, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig-7*plsize/2, yorig+2*plsize2), (xorig+plsize/2, yorig+2*plsize2))
		ar3_6 = ((xorig+plsize-plsize/4, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig-3*plsize, yorig+plsize2), (xorig+plsize-plsize/4, yorig+plsize2), (xorig-7*plsize/2, yorig+2*plsize2), (xorig+plsize/2, yorig+2*plsize2))
		ar3_7 = ((xorig+plsize-plsize/4, yorig-3*plsize2/2), (xorig-2*plsize, yorig+plsize2/2), (xorig, yorig-plsize2/2), (xorig-7*plsize/2, yorig+3*plsize2/2), (xorig+plsize-plsize/4, yorig+3*plsize2/2), (xorig-5*plsize, yorig+5*plsize2/2), (xorig+plsize/2, yorig+5*plsize2/2))

		arplace3 = (ar3_1, ar3_2, ar3_3, ar3_4, ar3_5, ar3_6, ar3_7)

		#5th place
		xorig = cen[0]+radius/2-plsize/2
		yorig = cen[1]+3*radius/4
		ar5_1 = ((xorig, yorig), )
		ar5_2 = ((xorig, yorig), (xorig, yorig+plsize2))
		ar5_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar5_4 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig-plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar5_5 = ((xorig-plsize, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize/2), (xorig-plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2))
		ar5_6 = ((xorig-plsize, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize/2), (xorig-plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2), (xorig-plsize, yorig+5*plsize2/2))
		ar5_7 = ((xorig-plsize, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize/2), (xorig-plsize, yorig+3*plsize2/2), (xorig+3*plsize, yorig+3*plsize2/2), (xorig-plsize, yorig+5*plsize2/2), (xorig+5*plsize, yorig+5*plsize2/2))

		arplace5 = (ar5_1, ar5_2, ar5_3, ar5_4, ar5_5, ar5_6, ar5_7)

		#9th place
		xorig = cen[0]+radius/2-plsize/2
		yorig = cen[1]-3*radius/4
		ar9_1 = ((xorig, yorig), )
		ar9_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar9_3 = ((xorig, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2))
		ar9_4 = ((xorig-plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig, yorig), (xorig, yorig+plsize2))
		ar9_5 = ((xorig-plsize, yorig-3*plsize2/2), (xorig+3*plsize, yorig-3*plsize2/2), (xorig, yorig), (xorig, yorig+plsize2), (xorig-plsize-plsize/4, yorig+2*plsize2))
		ar9_6 = ((xorig-plsize, yorig-2*plsize2), (xorig-plsize, yorig-plsize2), (xorig+3*plsize, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2), (xorig-plsize-plsize/4, yorig+2*plsize2))
		ar9_7 = ((xorig-plsize, yorig-2*plsize2), (xorig+3*plsize, yorig-2*plsize2), (xorig-plsize, yorig-plsize2), (xorig+3*plsize, yorig-plsize2), (xorig, yorig), (xorig, yorig+plsize2), (xorig-plsize-plsize/4, yorig+2*plsize2))

		arplace9 = (ar9_1, ar9_2, ar9_3, ar9_4, ar9_5, ar9_6, ar9_7)

		#11th place
		xorig = cen[0]-radius/2-plsize
		yorig = cen[1]-3*radius/4
		ar11_1 = ((xorig, yorig), )
		ar11_2 = ((xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar11_3 = ((xorig, yorig-3*plsize2/2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar11_4 = ((xorig-7*plsize/2, yorig-2*plsize2), (xorig+plsize/2, yorig-2*plsize2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2))
		ar11_5 = ((xorig-7*plsize/2, yorig-2*plsize2), (xorig+plsize/2, yorig-2*plsize2), (xorig, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig+plsize/2, yorig+3*plsize2/2))
		ar11_6 = ((xorig-7*plsize/2, yorig-2*plsize2), (xorig+plsize/2, yorig-2*plsize2), (xorig-3*plsize, yorig-plsize2), (xorig+plsize/2+plsize/4, yorig-plsize2), (xorig, yorig+plsize2/2), (xorig+plsize/2, yorig+3*plsize2/2))
		ar11_7 = ((xorig-7*plsize/2, yorig-2*plsize2), (xorig+plsize/2, yorig-5*plsize2/2), (xorig+plsize/2, yorig-3*plsize2/2), (xorig-3*plsize, yorig-plsize2), (xorig+plsize/2+plsize/4, yorig-plsize2/2), (xorig, yorig+plsize2/2), (xorig+plsize/2, yorig+3*plsize2/2))

		arplace11 = (ar11_1, ar11_2, ar11_3, ar11_4, ar11_5, ar11_6, ar11_7)

		arplaces = (arplace1, arplace2, arplace3, arplace4, arplace5, arplace6, arplace7, arplace8, arplace9, arplace10, arplace11, arplace12)

		if ((chrt.full and opts.outer != options.Options.NONE) or chrt2 != None):
			#1
			xorigO1 = cen[0]-19*maxradius/20
			yorigO1 = cen[1]
			xorigO2 = cen[0]-4*maxradius/5
			yorigO2 = cen[1]
			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = xorigO1
				xorigO1 = xorigO2
				xorigO2 = tmp

			arO1_1 = ((xorigO1, yorigO1), )
			arO1_2 = ((xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2))
			arO1_3 = ((xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2))
			arO1_4 = ((xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2))
			arO1_5 = ((xorigO1, yorigO1-2*plsize2), (xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2), (xorigO1, yorigO1+2*plsize2))
			arO1_6 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2))
			arO1_7 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2))
			arO1_8 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2))
			arO1_9 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2))
			arO1_10 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2))
			arO1_11 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-2*plsize2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2), (xorigO2, yorigO2+2*plsize2))
			arO1_12 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2), (xorigO2, yorigO2+5*plsize2/2))

			arplaceO1 = (arO1_1, arO1_2, arO1_3, arO1_4, arO1_5, arO1_6, arO1_7, arO1_8, arO1_9, arO1_10, arO1_11, arO1_12)

			#12
			xorigO1 = cen[0]-19*maxradius/20
			yorigO1 = cen[1]-10*maxradius/20
			xorigO2 = cen[0]-4*maxradius/5
			yorigO2 = cen[1]-10*maxradius/20
			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				yorigO1 = cen[1]-10*maxradius/23
				yorigO2 = cen[1]-10*maxradius/23
				tmp = xorigO1
				xorigO1 = xorigO2
				xorigO2 = tmp

			arO12_1 = ((xorigO1, yorigO1), )
			arO12_2 = ((xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2))
			arO12_3 = ((xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2))
			arO12_4 = ((xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2))
			arO12_5 = ((xorigO1, yorigO1-2*plsize2), (xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2), (xorigO1, yorigO1+2*plsize2))
			arO12_6 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2))
			arO12_7 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2))
			arO12_8 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2))
			arO12_9 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2))
			arO12_10 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2))
			arO12_11 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-2*plsize2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2), (xorigO2, yorigO2+2*plsize2))
			arO12_12 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2), (xorigO2, yorigO2+5*plsize2/2))

			arplaceO12 = (arO12_1, arO12_2, arO12_3, arO12_4, arO12_5, arO12_6, arO12_7, arO12_8, arO12_9, arO12_10, arO12_11, arO12_12)

			#2
			xorigO1 = cen[0]-19*maxradius/20
			yorigO1 = cen[1]+10*maxradius/20
			xorigO2 = cen[0]-4*maxradius/5
			yorigO2 = cen[1]+10*maxradius/20
			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				yorigO1 = cen[1]+10*maxradius/23
				yorigO2 = cen[1]+10*maxradius/23
				tmp = xorigO1
				xorigO1 = xorigO2
				xorigO2 = tmp

			arO2_1 = ((xorigO1, yorigO1), )
			arO2_2 = ((xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2))
			arO2_3 = ((xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2))
			arO2_4 = ((xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2))
			arO2_5 = ((xorigO1, yorigO1-2*plsize2), (xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2), (xorigO1, yorigO1+2*plsize2))
			arO2_6 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2))
			arO2_7 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2))
			arO2_8 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2))
			arO2_9 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2))
			arO2_10 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2))
			arO2_11 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-2*plsize2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2), (xorigO2, yorigO2+2*plsize2))
			arO2_12 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2), (xorigO2, yorigO2+5*plsize2/2))

			arplaceO2 = (arO2_1, arO2_2, arO2_3, arO2_4, arO2_5, arO2_6, arO2_7, arO2_8, arO2_9, arO2_10, arO2_11, arO2_12)

			#7
			xorigO1 = cen[0]+19*maxradius/22
			yorigO1 = cen[1]
			xorigO2 = cen[0]+28*maxradius/38
			yorigO2 = cen[1]
			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = xorigO1
				xorigO1 = xorigO2
				xorigO2 = tmp

			arO7_1 = ((xorigO1, yorigO1), )
			arO7_2 = ((xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2))
			arO7_3 = ((xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2))
			arO7_4 = ((xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2))
			arO7_5 = ((xorigO1, yorigO1-2*plsize2), (xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2), (xorigO1, yorigO1+2*plsize2))
			arO7_6 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2))
			arO7_7 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2))
			arO7_8 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2))
			arO7_9 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2))
			arO7_10 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2))
			arO7_11 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-2*plsize2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2), (xorigO2, yorigO2+2*plsize2))
			arO7_12 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2), (xorigO2, yorigO2+5*plsize2/2))

			arplaceO7 = (arO7_1, arO7_2, arO7_3, arO7_4, arO7_5, arO7_6, arO7_7, arO7_8, arO7_9, arO7_10, arO7_11, arO7_12)

			#8
			xorigO1 = cen[0]+19*maxradius/22
			yorigO1 = cen[1]-10*maxradius/20
			xorigO2 = cen[0]+28*maxradius/38
			yorigO2 = cen[1]-10*maxradius/20
			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				yorigO1 = cen[1]-10*maxradius/23
				yorigO2 = cen[1]-10*maxradius/23
				tmp = xorigO1
				xorigO1 = xorigO2
				xorigO2 = tmp

			arO8_1 = ((xorigO1, yorigO1), )
			arO8_2 = ((xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2))
			arO8_3 = ((xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2))
			arO8_4 = ((xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2))
			arO8_5 = ((xorigO1, yorigO1-2*plsize2), (xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2), (xorigO1, yorigO1+2*plsize2))
			arO8_6 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2))
			arO8_7 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2))
			arO8_8 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2))
			arO8_9 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2))
			arO8_10 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2))
			arO8_11 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-2*plsize2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2), (xorigO2, yorigO2+2*plsize2))
			arO8_12 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2), (xorigO2, yorigO2+5*plsize2/2))

			arplaceO8 = (arO8_1, arO8_2, arO8_3, arO8_4, arO8_5, arO8_6, arO8_7, arO8_8, arO8_9, arO8_10, arO8_11, arO8_12)

			#6
			xorigO1 = cen[0]+19*maxradius/22
			yorigO1 = cen[1]+10*maxradius/20
			xorigO2 = cen[0]+28*maxradius/38
			yorigO2 = cen[1]+10*maxradius/20
			if (maxnum > HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				yorigO1 = cen[1]+10*maxradius/23
				yorigO2 = cen[1]+10*maxradius/23
				tmp = xorigO1
				xorigO1 = xorigO2
				xorigO2 = tmp

			arO6_1 = ((xorigO1, yorigO1), )
			arO6_2 = ((xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2))
			arO6_3 = ((xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2))
			arO6_4 = ((xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2))
			arO6_5 = ((xorigO1, yorigO1-2*plsize2), (xorigO1, yorigO1-plsize2), (xorigO1, yorigO1), (xorigO1, yorigO1+plsize2), (xorigO1, yorigO1+2*plsize2))
			arO6_6 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2))
			arO6_7 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2))
			arO6_8 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2))
			arO6_9 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2))
			arO6_10 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2))
			arO6_11 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-2*plsize2), (xorigO2, yorigO2-plsize2), (xorigO2, yorigO2), (xorigO2, yorigO2+plsize2), (xorigO2, yorigO2+2*plsize2))
			arO6_12 = ((xorigO1, yorigO1-5*plsize2/2), (xorigO1, yorigO1-3*plsize2/2), (xorigO1, yorigO1-plsize2/2), (xorigO1, yorigO1+plsize2/2), (xorigO1, yorigO1+3*plsize2/2), (xorigO1, yorigO1+5*plsize2/2), (xorigO2, yorigO2-5*plsize2/2), (xorigO2, yorigO2-3*plsize2/2), (xorigO2, yorigO2-plsize2/2), (xorigO2, yorigO2+plsize2/2), (xorigO2, yorigO2+3*plsize2/2), (xorigO2, yorigO2+5*plsize2/2))

			arplaceO6 = (arO6_1, arO6_2, arO6_3, arO6_4, arO6_5, arO6_6, arO6_7, arO6_8, arO6_9, arO6_10, arO6_11, arO6_12)

			#10
			xorigO1 = cen[0]-2*maxradius/12
			xorigO2 = cen[0]-maxradius/30
			xorigO3 = cen[0]+2*maxradius/18
			yorigO1 = cen[1]-19*maxradius/20
			yorigO2 = cen[1]-19*maxradius/22-outerextra12_y2
			yorigO3 = cen[1]-38*maxradius/49-outerextra12_y3
			yorigO4 = cen[1]-38*maxradius/55-outerextra12_y4

			if (maxnum <= HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = yorigO1
				yorigO1 = yorigO2
				yorigO2 = tmp
			else:
				for i in range(houses.Houses.HOUSE_NUM):
					place = i-ascsign
					if (place < 0):
						place += chart.Chart.SIGN_NUM
					if (place == 9):	#is it the 10th place?
						if (ars[i] < 10):	# Are there less than 10 symbols in it? If yes, move down the symbols one line
							tmp = yorigO1
							yorigO1 = yorigO4
							tmp2 = yorigO2
							yorigO2 = yorigO3
							yorigO3 = tmp2
							yorigO4 = tmp
						break


			arO10_1 = ((xorigO2, yorigO1), )
			arO10_2 = ((xorigO2, yorigO1), (xorigO3, yorigO1))
			arO10_3 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1))
			arO10_4 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO3, yorigO2))
			arO10_5 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO10_6 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO10_7 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO3, yorigO3))
			arO10_8 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO10_9 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO10_10 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO3, yorigO4))
			arO10_11 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO2, yorigO4), (xorigO3, yorigO4))
			arO10_12 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO1, yorigO4), (xorigO2, yorigO4), (xorigO3, yorigO4))

			arplaceO10 = (arO10_1, arO10_2, arO10_3, arO10_4, arO10_5, arO10_6, arO10_7, arO10_8, arO10_9, arO10_10, arO10_11, arO10_12)

			#11
			xorigO1 = cen[0]-2*maxradius/12-5*maxradius/11
			xorigO2 = cen[0]-maxradius/30-5*maxradius/11
			xorigO3 = cen[0]+2*maxradius/18-5*maxradius/11
			yorigO1 = cen[1]-19*maxradius/20
			yorigO2 = cen[1]-19*maxradius/22-outerextra12_y2
			yorigO3 = cen[1]-38*maxradius/49-outerextra12_y3
			yorigO4 = cen[1]-38*maxradius/55-outerextra12_y4
			if (maxnum <= HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = yorigO1
				yorigO1 = yorigO2
				yorigO2 = tmp
			else:
				for i in range(houses.Houses.HOUSE_NUM):
					place = i-ascsign
					if (place < 0):
						place += chart.Chart.SIGN_NUM
					if (place == 10):
						if (ars[i] < 10):
							tmp = yorigO1
							yorigO1 = yorigO4
							tmp2 = yorigO2
							yorigO2 = yorigO3
							yorigO3 = tmp2
							yorigO4 = tmp
						break

			arO11_1 = ((xorigO2, yorigO1), )
			arO11_2 = ((xorigO2, yorigO1), (xorigO3, yorigO1))
			arO11_3 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1))
			arO11_4 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO3, yorigO2))
			arO11_5 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO11_6 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO11_7 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO3, yorigO3))
			arO11_8 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO11_9 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO11_10 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO3, yorigO4))
			arO11_11 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO2, yorigO4), (xorigO3, yorigO4))
			arO11_12 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO1, yorigO4), (xorigO2, yorigO4), (xorigO3, yorigO4))

			arplaceO11 = (arO11_1, arO11_2, arO11_3, arO11_4, arO11_5, arO11_6, arO11_7, arO11_8, arO11_9, arO11_10, arO11_11, arO11_12)

			#9
			xorigO1 = cen[0]+10*maxradius/36
			xorigO2 = cen[0]+10*maxradius/24
			xorigO3 = cen[0]+10*maxradius/18
			yorigO1 = cen[1]-19*maxradius/20
			yorigO2 = cen[1]-19*maxradius/22-outerextra12_y2
			yorigO3 = cen[1]-38*maxradius/49-outerextra12_y3
			yorigO4 = cen[1]-38*maxradius/55-outerextra12_y4
			if (maxnum <= HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = yorigO1
				yorigO1 = yorigO2
				yorigO2 = tmp
			else:
				for i in range(houses.Houses.HOUSE_NUM):
					place = i-ascsign
					if (place < 0):
						place += chart.Chart.SIGN_NUM
					if (place == 8):
						if (ars[i] < 10):
							tmp = yorigO1
							yorigO1 = yorigO4
							tmp2 = yorigO2
							yorigO2 = yorigO3
							yorigO3 = tmp2
							yorigO4 = tmp
						break

			arO9_1 = ((xorigO2, yorigO1), )
			arO9_2 = ((xorigO2, yorigO1), (xorigO3, yorigO1))
			arO9_3 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1))
			arO9_4 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO3, yorigO2))
			arO9_5 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO9_6 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO9_7 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO3, yorigO3))
			arO9_8 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO9_9 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO9_10 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO3, yorigO4))
			arO9_11 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO2, yorigO4), (xorigO3, yorigO4))
			arO9_12 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO1, yorigO4), (xorigO2, yorigO4), (xorigO3, yorigO4))

			arplaceO9 = (arO9_1, arO9_2, arO9_3, arO9_4, arO9_5, arO9_6, arO9_7, arO9_8, arO9_9, arO9_10, arO9_11, arO9_12)

			#3
			xorigO1 = cen[0]-2*maxradius/12-5*maxradius/11
			xorigO2 = cen[0]-maxradius/30-5*maxradius/11
			xorigO3 = cen[0]+2*maxradius/18-5*maxradius/11
			yorigO1 = cen[1]+19*maxradius/20
			yorigO2 = cen[1]+19*maxradius/22+outerextra12_y2
			yorigO3 = cen[1]+38*maxradius/49+outerextra12_y3
			yorigO4 = cen[1]+38*maxradius/55+outerextra12_y4
			if (maxnum <= HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = yorigO1
				yorigO1 = yorigO2
				yorigO2 = tmp
			else:
				for i in range(houses.Houses.HOUSE_NUM):
					place = i-ascsign
					if (place < 0):
						place += chart.Chart.SIGN_NUM
					if (place == 2):
						if (ars[i] < 10):
							tmp = yorigO1
							yorigO1 = yorigO4
							tmp2 = yorigO2
							yorigO2 = yorigO3
							yorigO3 = tmp2
							yorigO4 = tmp
						break

			arO3_1 = ((xorigO2, yorigO1), )
			arO3_2 = ((xorigO2, yorigO1), (xorigO3, yorigO1))
			arO3_3 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1))
			arO3_4 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO3, yorigO2))
			arO3_5 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO3_6 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO3_7 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO3, yorigO3))
			arO3_8 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO3_9 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO3_10 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO3, yorigO4))
			arO3_11 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO2, yorigO4), (xorigO3, yorigO4))
			arO3_12 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO1, yorigO4), (xorigO2, yorigO4), (xorigO3, yorigO4))

			arplaceO3 = (arO3_1, arO3_2, arO3_3, arO3_4, arO3_5, arO3_6, arO3_7, arO3_8, arO3_9, arO3_10, arO3_11, arO3_12)

			#4
			xorigO1 = cen[0]-2*maxradius/12
			xorigO2 = cen[0]-maxradius/30
			xorigO3 = cen[0]+2*maxradius/18
			yorigO1 = cen[1]+19*maxradius/20
			yorigO2 = cen[1]+19*maxradius/22+outerextra12_y2
			yorigO3 = cen[1]+38*maxradius/49+outerextra12_y3
			yorigO4 = cen[1]+38*maxradius/55+outerextra12_y4
			if (maxnum <= HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = yorigO1
				yorigO1 = yorigO2
				yorigO2 = tmp
			else:
				for i in range(houses.Houses.HOUSE_NUM):
					place = i-ascsign
					if (place < 0):
						place += chart.Chart.SIGN_NUM
					if (place == 3):
						if (ars[i] < 10):
							tmp = yorigO1
							yorigO1 = yorigO4
							tmp2 = yorigO2
							yorigO2 = yorigO3
							yorigO3 = tmp2
							yorigO4 = tmp
						break

			arO4_1 = ((xorigO2, yorigO1), )
			arO4_2 = ((xorigO2, yorigO1), (xorigO3, yorigO1))
			arO4_3 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1))
			arO4_4 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO3, yorigO2))
			arO4_5 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO4_6 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO4_7 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO3, yorigO3))
			arO4_8 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO4_9 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO4_10 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO3, yorigO4))
			arO4_11 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO2, yorigO4), (xorigO3, yorigO4))
			arO4_12 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO1, yorigO4), (xorigO2, yorigO4), (xorigO3, yorigO4))

			arplaceO4 = (arO4_1, arO4_2, arO4_3, arO4_4, arO4_5, arO4_6, arO4_7, arO4_8, arO4_9, arO4_10, arO4_11, arO4_12)

			#5
			xorigO1 = cen[0]+10*maxradius/36
			xorigO2 = cen[0]+10*maxradius/24
			xorigO3 = cen[0]+10*maxradius/18
			yorigO1 = cen[1]+19*maxradius/20
			yorigO2 = cen[1]+19*maxradius/22+outerextra12_y2
			yorigO3 = cen[1]+38*maxradius/49+outerextra12_y3
			yorigO4 = cen[1]+38*maxradius/55+outerextra12_y4
			if (maxnum <= HellenisticChart.MAXSYMBOLNUMPERCOLUM):
				tmp = yorigO1
				yorigO1 = yorigO2
				yorigO2 = tmp
			else:
				for i in range(houses.Houses.HOUSE_NUM):
					place = i-ascsign
					if (place < 0):
						place += chart.Chart.SIGN_NUM
					if (place == 4):
						if (ars[i] < 10):
							tmp = yorigO1
							yorigO1 = yorigO4
							tmp2 = yorigO2
							yorigO2 = yorigO3
							yorigO3 = tmp2
							yorigO4 = tmp
						break

			arO5_1 = ((xorigO2, yorigO1), )
			arO5_2 = ((xorigO2, yorigO1), (xorigO3, yorigO1))
			arO5_3 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1))
			arO5_4 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO3, yorigO2))
			arO5_5 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO5_6 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2))
			arO5_7 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO3, yorigO3))
			arO5_8 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO5_9 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3))
			arO5_10 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO3, yorigO4))
			arO5_11 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO2, yorigO4), (xorigO3, yorigO4))
			arO5_12 = ((xorigO1, yorigO1), (xorigO2, yorigO1), (xorigO3, yorigO1), (xorigO1, yorigO2), (xorigO2, yorigO2), (xorigO3, yorigO2), (xorigO1, yorigO3), (xorigO2, yorigO3), (xorigO3, yorigO3), (xorigO1, yorigO4), (xorigO2, yorigO4), (xorigO3, yorigO4))

			arplaceO5 = (arO5_1, arO5_2, arO5_3, arO5_4, arO5_5, arO5_6, arO5_7, arO5_8, arO5_9, arO5_10, arO5_11, arO5_12)

			arplacesO = (arplaceO1, arplaceO2, arplaceO3, arplaceO4, arplaceO5, arplaceO6, arplaceO7, arplaceO8, arplaceO9, arplaceO10, arplaceO11, arplaceO12)

			arsignsposO = [[], [], [], [], [], [], [], [], [], [], [], []]

			if (chrt.full and chrt2 == None):
				if (opts.outer == options.Options.ANTIS):
					num = len(chrt.antis.ascmclons)
					for i in range(num):
						lon = chrt.antis.ascmclons[i]
						if (opts.ayanamsa != 0):
							lon -= chrt.ayanamsa
							lon = util.normalize(lon)
						sign = int(lon/chart.Chart.SIGN_DEG)
						arsignsposO[sign].append((i, lon, False))
					num = len(chrt.antis.plslons)
					for i in range(num):
						lon = chrt.antis.plslons[i]
						if (opts.ayanamsa != 0):
							lon -= chrt.ayanamsa
							lon = util.normalize(lon)
						sign = int(lon/chart.Chart.SIGN_DEG)
						arsignsposO[sign].append((HellenisticChart.BASE+i, lon, chrt.planets.planets[i].data[planet.Planet.SPLON] < 0.0))
					num = len(chrt.antis.lotslons)
					for i in range(num):
						if (opts.lots[i]):
							lon = chrt.antis.lotslons[i]
							if (opts.ayanamsa != 0):
								lon -= chrt.ayanamsa
								lon = util.normalize(lon)
							sign = int(lon/chart.Chart.SIGN_DEG)
							arsignsposO[sign].append((HellenisticChart.LOTS+i, lon, False))
					if (opts.syzygy):
						lon = chrt.antis.syzlon
						if (opts.ayanamsa != 0):
							lon -= chrt.ayanamsa
							lon = util.normalize(lon)
						sign = int(lon/chart.Chart.SIGN_DEG)
						arsignsposO[sign].append((HellenisticChart.SYZYGY, lon, False))
	
				elif (opts.outer == options.Options.DODEC):
					num = len(chrt.dodec.ascmclons)
					for i in range(num):
						lon = chrt.dodec.ascmclons[i]
						sign = int(lon/chart.Chart.SIGN_DEG)
						arsignsposO[sign].append((i, lon, False))
					num = len(chrt.dodec.plslons)
					for i in range(num):
						lon = chrt.dodec.plslons[i]
						sign = int(lon/chart.Chart.SIGN_DEG)
						arsignsposO[sign].append((HellenisticChart.BASE+i, lon, chrt.planets.planets[i].data[planet.Planet.SPLON] < 0.0))
					num = len(chrt.dodec.lotslons)
					for i in range(num):
						if (opts.lots[i]):
							lon = chrt.dodec.lotslons[i]
							sign = int(lon/chart.Chart.SIGN_DEG)
							arsignsposO[sign].append((HellenisticChart.LOTS+i, lon, False))
					if (opts.syzygy):
						lon = chrt.dodec.syzlon
						sign = int(lon/chart.Chart.SIGN_DEG)
						arsignsposO[sign].append((HellenisticChart.SYZYGY, lon, False))

			if (chrt2 != None):
				self.fillSigns(chrt2, arsignsposO, opts)

			# Outer symbols
			if ((chrt.full and opts.outer != options.Options.NONE) or chrt2 != None):
				self.drawSymbols(arsignsposO, arplacesO, ascsign, opts)
#				symlon = 25.4578
#				symtxt = 'D'
#				symclr = util.getRGBTxt(opts.clrplanets[4])
#				wsym = self.plfont.measure(symtxt)
#				for i in range(12):
#					x = arplacesO[11][11][i][0]
#					y = arplacesO[11][11][i][1]
##				x = arplacesO[9][0][0][0]
##				y = arplacesO[9][0][0][1]
#					symtxtid = self.can.create_text(x, y, font=self.plfont, text=symtxt, fill=symclr)
#					bb = self.can.create_rectangle(self.can.bbox(symtxtid), outline=signs_rgb)
#
#					xr = x+wsym
#					wretr = 0.0
#					retrtxtid = self.can.create_text(xr, y, font=self.retrfont, text='T', fill=symclr)
#					sizeofretr = self.retrfont.measure('T')
#					wretr = sizeofretr+self.xspace
#					xd = xr+wretr
#					d, m, s = util.decToDeg(symlon)
#					pos = int(d%chart.Chart.SIGN_DEG)
#					#round up
#					pos += 1
#					degtxtid = self.can.create_text(xd, y, font=self.datafont, text=str(pos), fill=symclr)


		arsignspos = [[], [], [], [], [], [], [], [], [], [], [], []]
		self.fillSigns(chrt, arsignspos, opts)
		self.drawSymbols(arsignspos, arplaces, ascsign, opts)


	def fillSigns(self, chrt, ars, opts):
		lonasc = chrt.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (opts.ayanamsa != 0):
			lonasc -= chrt.ayanamsa
			lonasc = util.normalize(lonasc)

		sign = int(lonasc/chart.Chart.SIGN_DEG)
		ars[sign].append((HellenisticChart.ASC, lonasc, False))
		lonmc = chrt.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		if (opts.ayanamsa != 0):
			lonmc -= chrt.ayanamsa
			lonmc = util.normalize(lonmc)

		sign = int(lonmc/chart.Chart.SIGN_DEG)
		ars[sign].append((HellenisticChart.MC, lonmc, False))

		arplids = (HellenisticChart.SATURN, HellenisticChart.JUPITER, HellenisticChart.MARS, HellenisticChart.SUN, HellenisticChart.VENUS, HellenisticChart.MERCURY, HellenisticChart.MOON, HellenisticChart.ANODE)
		for i in range(planets.Planets.PLANETS_NUM+1):
			lonpl = chrt.planets.planets[i].data[planet.Planet.LON]
			if (opts.ayanamsa != 0):
				lonpl -= chrt.ayanamsa
				lonpl = util.normalize(lonpl)
			sign = int(lonpl/chart.Chart.SIGN_DEG)
			ars[sign].append((arplids[i], lonpl, chrt.planets.planets[i].data[planet.Planet.SPLON] < 0.0))

#The seven planets and the moon's node should always be visible!
		#sort lons in signs (ars-arrays)
#		num = len(ars)
#		for k in range(num):
#			subnum = len(ars[k])
#			if (subnum <= 1):
#				continue
#			place = k-ascsign
#			if (place < 0):
#				place += chart.Chart.SIGN_NUM
#			#Bubble sort (very slow, but there are only a few items)
#			for j in range(subnum):
#				for i in range(subnum-1):
#					#if places 6, 7, 8 then in descending order
#					if (place == 5 or place == 6 or place == 7):
#						if (ars[k][i][1] < ars[k][i+1][1]):
#							tmp = ars[k][i]
#							ars[k][i] = ars[k][i+1]
#							ars[k][i+1] = tmp
#					else:
#						if (ars[k][i][1] > ars[k][i+1][1]):
#							tmp = ars[k][i]
#							ars[k][i] = ars[k][i+1]
#							ars[k][i+1] = tmp


		arlotids = (HellenisticChart.FORTUNE, HellenisticChart.SPIRIT, HellenisticChart.EROS, HellenisticChart.VICTORY, HellenisticChart.NECESSITY, HellenisticChart.COURAGE, HellenisticChart.NEMESIS)
		for i in range(lots.Lots.LOTS_NUM):
			if (opts.lots[i]):
				lonlot = chrt.lots.data[i]
				if (opts.ayanamsa != 0):
					lonlot -= chrt.ayanamsa
					lonlot = util.normalize(lonlot)
				sign = int(lonlot/chart.Chart.SIGN_DEG)
				ars[sign].append((arlotids[i], lonlot, False))

		if (opts.syzygy):
			lonsyz = chrt.syzygy.lon
			if (opts.ayanamsa != 0):
				lonsyz -= chrt.ayanamsa
				lonsyz = util.normalize(lonsyz)
			sign = int(lonsyz/chart.Chart.SIGN_DEG)
			ars[sign].append((HellenisticChart.SYZYGY, lonsyz, False))

		#sort lons in signs (ars-arrays)
#		num = len(ars)
#		for k in range(num):
#			subnum = len(ars[k])
#			if (subnum <= 1):
#				continue
#			place = k-ascsign
#			if (place < 0):
#				place += chart.Chart.SIGN_NUM
#			#Bubble sort (very slow, but there are only a few items)
#			for j in range(subnum):
#				for i in range(subnum-1):
#					#if places 6, 7, 8 then in descending order
#					if (place == 5 or place == 6 or place == 7):
#						if (ars[k][i][1] < ars[k][i+1][1]):
#							tmp = ars[k][i]
#							ars[k][i] = ars[k][i+1]
#							ars[k][i+1] = tmp
#					else:
#						if (ars[k][i][1] > ars[k][i+1][1]):
#							tmp = ars[k][i]
#							ars[k][i] = ars[k][i+1]
#							ars[k][i+1] = tmp


	def getMaxSymbolNumPerSigns(self, chrt, opts):
		ars = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		lonasc = chrt.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (opts.ayanamsa != 0):
			lonasc -= chrt.ayanamsa
			lonasc = util.normalize(lonasc)

		ascsign = int(lonasc/chart.Chart.SIGN_DEG)
		ars[ascsign] += 1

		lonmc = chrt.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		if (opts.ayanamsa != 0):
			lonmc -= chrt.ayanamsa
			lonmc = util.normalize(lonmc)

		sign = int(lonmc/chart.Chart.SIGN_DEG)
		ars[sign] += 1

		for i in range(planets.Planets.PLANETS_NUM+1):
			lonpl = chrt.planets.planets[i].data[planet.Planet.LON]
			if (opts.ayanamsa != 0):
				lonpl -= chrt.ayanamsa
				lonpl = util.normalize(lonpl)
			sign = int(lonpl/chart.Chart.SIGN_DEG)
			ars[sign] += 1

		for i in range(lots.Lots.LOTS_NUM):
			if (opts.lots[i]):
				lonlot = chrt.lots.data[i]
				if (opts.ayanamsa != 0):
					lonlot -= chrt.ayanamsa
					lonlot = util.normalize(lonlot)
				sign = int(lonlot/chart.Chart.SIGN_DEG)
				ars[sign] += 1

		if (opts.syzygy):
			lonsyz = chrt.syzygy.lon
			if (opts.ayanamsa != 0):
				lonsyz -= chrt.ayanamsa
				lonsyz = util.normalize(lonsyz)
			sign = int(lonsyz/chart.Chart.SIGN_DEG)
			ars[sign] += 1

		maxnum = 0
		maxnumleftright = 0
		maxnumtopbottom = 0
		for i in range(len(ars)):
			if (ars[i] > maxnum):
				maxnum = ars[i]

			place = i-ascsign
			if (place < 0):
				place += chart.Chart.SIGN_NUM

			if (place == 11 or place == 0 or place == 1 or place == 5 or place == 6 or place == 7):
				if (ars[i] > maxnumleftright):
					maxnumleftright = ars[i]
			else:
				if (ars[i] > maxnumtopbottom):
					maxnumtopbottom = ars[i]

		return maxnum, maxnumleftright, maxnumtopbottom, ars


	def getMaxSymbolNumPerSignsAntisDodec(self, dat, ayan, opts):
		ars = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		lonasc = dat.ascmclons[0]
		if (opts.outer != options.Options.DODEC and opts.ayanamsa != 0):
			lonasc -= ayan
			lonasc = util.normalize(lonasc)

		ascsign = int(lonasc/chart.Chart.SIGN_DEG)
		ars[ascsign] += 1

		lonmc = dat.ascmclons[1]
		if (opts.outer != options.Options.DODEC and opts.ayanamsa != 0):
			lonmc -= ayan
			lonmc = util.normalize(lonmc)

		sign = int(lonmc/chart.Chart.SIGN_DEG)
		ars[sign] += 1

		for i in range(planets.Planets.PLANETS_NUM+1):
			lonpl = dat.plslons[i]
			if (opts.outer != options.Options.DODEC and opts.ayanamsa != 0):
				lonpl -= ayan
				lonpl = util.normalize(lonpl)
			sign = int(lonpl/chart.Chart.SIGN_DEG)
			ars[sign] += 1

		for i in range(lots.Lots.LOTS_NUM):
			if (opts.lots[i]):
				lonlot = dat.lotslons[i]
				if (opts.outer != options.Options.DODEC and opts.ayanamsa != 0):
					lonlot -= ayan
					lonlot = util.normalize(lonlot)
				sign = int(lonlot/chart.Chart.SIGN_DEG)
				ars[sign] += 1

		if (opts.syzygy):
			lonsyz = dat.syzlon
			if (opts.outer != options.Options.DODEC and opts.ayanamsa != 0):
				lonsyz -= ayan
				lonsyz = util.normalize(lonsyz)
			sign = int(lonsyz/chart.Chart.SIGN_DEG)
			ars[sign] += 1

		maxnum = 0
		maxnumleftright = 0
		maxnumtopbottom = 0
		for i in range(len(ars)):
			if (ars[i] > maxnum):
				maxnum = ars[i]

			place = i-ascsign
			if (place < 0):
				place += chart.Chart.SIGN_NUM

			if (place == 11 or place == 0 or place == 1 or place == 5 or place == 6 or place == 7):
				if (ars[i] > maxnumleftright):
					maxnumleftright = ars[i]
			else:
				if (ars[i] > maxnumtopbottom):
					maxnumtopbottom = ars[i]

		return maxnum, maxnumleftright, maxnumtopbottom, ars


	def drawData(self, chrt, opts, wndsize, chrt2, ratio):
		w, h = wndsize
		msi = min(w, h)
		maxradius = msi/2
		cen = (w/2, h/2)
		radius = maxradius*ratio
		datasize = int(radius/20)
		x1 = cen[0]
		y1 = cen[1]-(radius/3)*0.85
		rowh = int(radius/14)
		texts_rgb = util.getRGBTxt(opts.clrtexts) 
		if (self.bw):
			texts_rgb = util.getRGBTxt((0, 0, 0)) 

		juliantxt = ''
		bctxt = ''
		if (chrt.time.cal == chtime.Time.JULIAN):
			juliantxt = texts.txtscommon['J']
		if (chrt.time.bc):
			bctxt = texts.txtscommon['BC']

		datetxt = texts.months[chrt.time.omonth-1]+' '+str(chrt.time.oday)+', '+str(chrt.time.oyear)+' '+juliantxt+' '+bctxt
		txtId = self.can.create_text(x1, y1, font=self.datafont, text=datetxt, justify='center', fill=texts_rgb)
		timetxt = str(chrt.time.hour).zfill(2)+':'+str(chrt.time.minute).zfill(2)+':'+str(chrt.time.second).zfill(2)+' '+texts.zoneList[chrt.time.zt]
		txtId = self.can.create_text(x1, y1+rowh, font=self.datafont, text=timetxt, justify='center', fill=texts_rgb)
		txtId = self.can.create_text(x1, y1+2*rowh, font=self.datafont, justify='center', text=chrt.place.placename, fill=texts_rgb)

		dirlontxt = texts.txtscommon['E']
		if (not chrt.place.east):
			dirlontxt = texts.txtscommon['W']
		dirlattxt = texts.txtscommon['N']
		if (not chrt.place.north):
			dirlattxt = texts.txtscommon['S']
	
		deg_symbol = '\u00b0'
		coordtxt = (str(chrt.place.deglon)).zfill(2)+deg_symbol+(str(chrt.place.minlon)).zfill(2)+"'"+dirlontxt+'  '+(str(chrt.place.deglat)).zfill(2)+deg_symbol+(str(chrt.place.minlat)).zfill(2)+"'"+dirlattxt
		txtId = self.can.create_text(x1, y1+3*rowh, font=self.datafont, text=coordtxt, justify='center', fill=texts_rgb)
		txtId = self.can.create_text(x1, y1+4*rowh, font=self.datafont, text=chrt.name, justify='center', fill=texts_rgb)
		typetxt = texts.typeList[chrt.htype]
		txtId = self.can.create_text(x1, y1+5*rowh, font=self.datafont, text=typetxt, justify='center', fill=texts_rgb)
		ayantxt = texts.txtsayanamsa['Tropical']
		if (opts.ayanamsa != 0):
			ayantxt = texts.ayanamsaList[opts.ayanamsa]
		txtId = self.can.create_text(x1, y1+6*rowh, font=self.datafont, text=ayantxt, justify='center', fill=texts_rgb)
		hstxt = texts.hsystemList[opts.hsys]
		txtId = self.can.create_text(x1, y1+7*rowh, font=self.datafont, text=hstxt, justify='center', fill=texts_rgb)

		plfont = font.Font(family='Valens', size=datasize)
		ar = (6, 2, 5, 1, 4, 0, 3)	
		daysym = common.common.planets[ar[chrt.time.ph.weekday]]
		hoursym = common.common.planets[chrt.time.ph.planetaryhour]
		dayhourtxt = daysym+'   '+hoursym
		txtId = self.can.create_text(x1, y1+8*rowh, font=plfont, text=dayhourtxt, justify='center', fill=texts_rgb)


	def drawSymbols(self, ars, arp, ascsign, opts):
		lotclrs = (opts.clrplanets[planets.Planets.MOON], opts.clrplanets[planets.Planets.SUN], opts.clrplanets[planets.Planets.VENUS], opts.clrplanets[planets.Planets.JUPITER], opts.clrplanets[planets.Planets.MERCURY], opts.clrplanets[planets.Planets.MARS], opts.clrplanets[planets.Planets.SATURN])
		sizeofretr = self.retrfont.measure('T')
		num = len(ars)
		for i in range(num):
			place = i-ascsign
			if (place < 0):
				place += chart.Chart.SIGN_NUM

			subnum = len(ars[i])
			if (subnum > len(arp[place])):
				subnum = len(arp[place])
			for j in range(subnum):
				symid = ars[i][j][0]
				symlon = ars[i][j][1]
				symretr = ars[i][j][2]

				symtxt = ''
				symclr = util.getRGBTxt((0,0,0)) 
				if (symid == HellenisticChart.ASC):
					symtxt = common.common.asc
					symclr = util.getRGBTxt(opts.clrAscMC)
				elif (symid == HellenisticChart.MC):
					symtxt = common.common.mc
					symclr = util.getRGBTxt(opts.clrAscMC)
				elif (symid < HellenisticChart.LOTS):
					symtxt = common.common.planets[symid-HellenisticChart.BASE]
					symclr = util.getRGBTxt(opts.clrplanets[symid-HellenisticChart.BASE])
				elif (symid < HellenisticChart.SYZYGY):
					symtxt = common.common.lots[symid-HellenisticChart.LOTS]
					symclr = util.getRGBTxt(lotclrs[symid-HellenisticChart.LOTS])
				else:
					symtxt = common.common.syzygy
					symclr = util.getRGBTxt(opts.clrsigns)

				if (self.bw):
					symclr = self.black_rgb

				wsym = self.plfont.measure(symtxt)
				x = arp[place][subnum-1][j][0]
				y = arp[place][subnum-1][j][1]
				symtxtid = self.can.create_text(x, y, font=self.plfont, text=symtxt, fill=symclr)
				if (not self.bw and opts.showbounds):
					bound = chart.getBound(symlon, opts)
					bound_rgb = util.getRGBTxt(opts.clrplanets[bound])
#					if (bound != symid-HellenisticChart.BASE):
#					bb = self.can.create_rectangle(self.can.bbox(symtxtid), fill=bound_rgb, outline=bound_rgb)
					bb = self.can.create_rectangle(self.can.bbox(symtxtid), outline=bound_rgb, width=2)
					self.can.tag_lower(bb, symtxtid)

				xr = x+wsym
				wretr = 0.0
				if (symid >= HellenisticChart.BASE and symid < HellenisticChart.LOTS and symretr):
					retrtxtid = self.can.create_text(xr, y, font=self.retrfont, text='T', fill=symclr)
					wretr = sizeofretr+self.xspace
				xd = xr+wretr
				d, m, s = util.decToDeg(symlon)
				pos = int(d%chart.Chart.SIGN_DEG)
				#round up
				pos += 1
				degtxtid = self.can.create_text(xd, y, font=self.datafont, text=str(pos), fill=symclr)






