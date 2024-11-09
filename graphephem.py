from tkinter import *
from tkinter import font
import chart
import planets
import common
import util
import texts


class GraphEphem:

	SMALL_SIZE = 400
	INTERMEDIATE_SIZE = 500
	MEDIUM_SIZE = 600

	def __init__(self, parent, year, posArr, opts, wndsize):

		self.parent = parent
		self.year = year
		self.posArr = posArr
		self.options = opts

		self.bw = False
		bkg_rgb = util.getRGBTxt(opts.clrbackground) 
		self.can = Canvas(self.parent, bd=0, highlightthickness=0, bg=bkg_rgb)


	def drawCanvas(self, wndsize):
		self.can.delete("all")
		w, h = wndsize
		self.w, self.h = wndsize
		self.tableSize = int(min(self.w, self.h))
		self.planetSymbolSize = int(self.tableSize/40)
		self.BORDER = self.planetSymbolSize
		self.spaceSize = int(self.planetSymbolSize/3)
		y1 = self.BORDER
		y2 = self.h-4*self.BORDER
		self.signSize = int((y2-y1)/(chart.Chart.SIGN_NUM+2)) #Number of signs(12) and 2 margins (up and down)
		self.signSymbolSize = int(self.signSize/2)
		self.fontSize = self.planetSymbolSize
		x1 = 2*self.BORDER+self.signSymbolSize+self.spaceSize
		x2 = self.w-2*self.BORDER
		self.monthSize = int((x2-x1)/13) #Number of months(12) and margin
		self.txtSymbolSize = int(self.monthSize/4)

		self.txtSymbolSize = int(min(self.signSize, self.monthSize)/3)
		self.signSymbolSize = self.txtSymbolSize

#		self.fntPlanets = ImageFont.truetype(common.common.symbols, self.planetSymbolSize)
		self.fntPlanets = font.Font(family='Valens', size=self.planetSymbolSize)
		self.fntPlanetsTup = ('Valens', self.planetSymbolSize)
#		self.fntSigns = ImageFont.truetype(common.common.symbols, self.signSymbolSize)
		self.fntSigns = font.Font(family='Valens', size=self.signSymbolSize)
		self.fntSignsTup = ('Valens', self.signSymbolSize)
#		self.fntTxt = ImageFont.truetype(common.common.abc, self.txtSymbolSize)
		self.fntTxt = font.Font(family='Valens', size=self.txtSymbolSize)
		self.fntTxtTup = ('Helvetica', self.txtSymbolSize)

		tableclr = util.getRGBTxt((0,0,0))
		txtclr = util.getRGBTxt((0,0,0))
		bkgclr = util.getRGBTxt((255,255,255))
		plsclr = util.getRGBTxt((0,0,0))
		signsclr = util.getRGBTxt((0,0,0))
		clrbkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		if (not self.bw):
			bkgclr = util.getRGBTxt(self.options.clrbackground)
			tableclr = util.getRGBTxt(self.options.clrframe)
			txtclr = util.getRGBTxt(self.options.clrtexts)
			signsclr = util.getRGBTxt(self.options.clrsigns)
			self.can.configure(bg=clrbkg_rgb)
		else:
			self.can.configure(bg=bkgclr)

		#Test (draws az 'A' to (0, 0). There is also the border of the window)
#		wsym = self.fntPlanets.measure('A')
#		hsym = self.fntSigns.cget('size')
#		txtId = self.can.create_text(wsym/2, hsym, font=self.fntTxtTup, text='A', fill=util.getRGBTxt(self.options.clrtexts))###
#		bb = self.can.create_rectangle(self.can.bbox(txtId), fill="red", outline='red')
#		self.can.tag_lower(bb, txtId)

		w = 4
		if (self.tableSize <= GraphEphem.SMALL_SIZE):
			w = 2
		elif (self.tableSize <= GraphEphem.MEDIUM_SIZE):
			w = 3

		x1 = 2*self.BORDER+self.signSymbolSize+self.spaceSize
		y1 = self.BORDER
		x2 = x1
		y2 = self.h-self.BORDER
		line = self.can.create_line(x1, y1, x2, y2, fill=tableclr, width=w)

		x1 = self.BORDER
		y1 = self.h-4*self.BORDER
		x2 = self.w-self.BORDER
		y2 = self.h-4*self.BORDER
		line = self.can.create_line(x1, y1, x2, y2, fill=tableclr, width=w)

		y1 = self.h-4*self.BORDER
		for i in range(chart.Chart.SIGN_NUM+1):
			y1 -= self.signSize
		x1 = 2*self.BORDER+self.signSymbolSize+self.spaceSize
#		y1 = self.BORDER
		x2 = x1
		y2 = self.h-4*self.BORDER
		for i in range(13):
			x1 += self.monthSize
			x2 += self.monthSize
			line = self.can.create_line(x1, y1, x2, y2, fill=tableclr, width=1, dash=(6, 3))

		x1 = 2*self.BORDER+self.signSymbolSize+self.spaceSize
		y1 = self.h-4*self.BORDER
#		x2 = self.w-self.BORDER
		y2 = self.h-4*self.BORDER
		for i in range(chart.Chart.SIGN_NUM+1):
			y1 -= self.signSize
			y2 -= self.signSize
			line = self.can.create_line(x1, y1, x2, y2, fill=tableclr, width=1, dash=(6, 3))

		#positions of planets
		plpixelpos = []
		pltoppixelpos = []
		plstopids = []
		plstop = []
		plbottompixelpos = []
		plsbottomids = []
		plsbottom = []
		xOrig = 2*self.BORDER+self.signSymbolSize+self.spaceSize+self.monthSize
		yOrig = self.h-4*self.BORDER-self.signSize
		yOrig2 = yOrig
		for i in range(chart.Chart.SIGN_NUM):
			yOrig2 -= self.signSize
		pixelsPer360 = self.signSize*chart.Chart.SIGN_NUM
		pixelsPer365 = self.monthSize*12
		scale360 = pixelsPer360/360.0
		scale365 = pixelsPer365/365.0
		plnum = len(self.posArr)
		posnum = len(self.posArr[0]) 
		for pl in range(planets.Planets.PLANETS_NUM-1): #Moon excepted
			prevx = prevy = 0.0
			for i in range(posnum):
				x = xOrig+i*scale365
				y = yOrig-self.posArr[pl][i]*scale360

				if (i == 0):
					plpixelpos.append(y)

				if (not self.bw):
					plsclr = util.getRGBTxt(self.options.clrplanets[pl])

				w = 2
				if (self.tableSize <= GraphEphem.INTERMEDIATE_SIZE):
					w = 1
#				line = self.can.create_line(x, y, x+1, y, fill=plsclr, width=w) # DrawPixel

				transition = ((prevy > self.h-4*self.BORDER-2*self.signSize and y < yOrig2+self.signSize) or (y > self.h-4*self.BORDER-2*self.signSize and prevy < yOrig2+self.signSize))
				if (i != 0 and not transition):
					line = self.can.create_line(prevx, prevy, x, y, fill=plsclr, width=w) 

				if (i != 0 and transition):
					if (prevy > self.h-4*self.BORDER-2*self.signSize and y < yOrig2+self.signSize):
						pltoppixelpos.append(x)
						plstopids.append(pl)
						plstop.append(common.common.planets[pl])

					if (y > self.h-4*self.BORDER-2*self.signSize and prevy < yOrig2+self.signSize):
						plbottompixelpos.append(x)
						plsbottomids.append(pl)
						plsbottom.append(common.common.planets[pl])

				prevx = x
				prevy = y

		#arrange
		bshift = self.arrange(common.common.planets, plpixelpos, yOrig2, yOrig)

		xOrig2 = xOrig
		for i in range(13):
			xOrig2 += self.monthSize
		if (len(plstop) > 1):
			bshifttop = self.arrange(plstop, pltoppixelpos, xOrig, xOrig2)
		if (len(plsbottom) > 1):
			bshiftbottom = self.arrange(plsbottom, plbottompixelpos, xOrig, xOrig2)

		#lines of planets
		x1 = 2*self.BORDER+self.signSymbolSize+self.spaceSize+self.monthSize-3*self.spaceSize
		x2 = 2*self.BORDER+self.signSymbolSize+self.spaceSize+self.monthSize
		for pl in range(planets.Planets.PLANETS_NUM-1): #Moon excepted
			y = plpixelpos[pl]

			if (not self.bw):
				plsclr = util.getRGBTxt(self.options.clrplanets[pl])
			line = self.can.create_line(x1, y+bshift[pl], x2, y, fill=plsclr, width=1) 

		#top
		if (len(plstop) != 0):
			y1 = yOrig2
			y2 = yOrig2-3*self.spaceSize
			plstopnum = len(plstop)
			for pl in range(plstopnum):
				x = pltoppixelpos[pl]

				if (not self.bw):
					plsclr = util.getRGBTxt(self.options.clrplanets[plstopids[pl]])

				if (len(plstop) > 1):
					line = self.can.create_line(x, y1, x+bshifttop[pl], y2, fill=plsclr, width=1) 
				else:
					line = self.can.create_line(x, y1, x, y2, fill=plsclr, width=1) 

		#bottom
		if (len(plsbottom) != 0):
			y1 = yOrig+3*self.spaceSize
			y2 = yOrig
			plsbottomnum = len(plsbottom)
			for pl in range(plsbottomnum):
				x = plbottompixelpos[pl]

				if (not self.bw):
					plsclr = util.getRGBTxt(self.options.clrplanets[plsbottomids[pl]])

				if (len(plsbottom) > 1):
					line = self.can.create_line(x+bshiftbottom[pl], y1, x, y2, fill=plsclr, width=1) 
				else:
					line = self.can.create_line(x, y1, x, y2, fill=plsclr, width=1) 

		#signs
		x = 2*self.BORDER
		y = self.h-4*self.BORDER-self.signSize
		hsym = 0#self.fntSigns.cget('size')
		for i in range(chart.Chart.SIGN_NUM):
			wsym = 0#self.fntSigns.measure(common.common.signs[i])
			txtSign = self.can.create_text(x, y-self.signSize/2-hsym/2-i*self.signSize, font=self.fntSignsTup, text=common.common.signs[i], fill=signsclr)

		#year
		txt = str(self.year)
		wtxt = 0#self.fntTxt.measure(txt)
		htxt = 0#self.fntTxt.cget('size')
		x = 2*self.BORDER+self.signSymbolSize+self.spaceSize
		y = self.h-3*self.BORDER+self.spaceSize
		offs = (self.monthSize-wtxt)/2
		txtId = self.can.create_text(x+offs, y, font=self.fntTxtTup, text=txt, fill=tableclr)

		#months
		x = 2*self.BORDER+self.signSymbolSize+self.spaceSize+self.monthSize
		y = self.h-3*self.BORDER+self.spaceSize
		mnum = len(texts.monthabbr)
		for i in range(mnum):
			txt = texts.monthabbr[i]
			wtxt = 0#self.fntTxt.measure(txt)
			offs = (self.monthSize-wtxt)/2
			txtId = self.can.create_text(x+i*self.monthSize+offs, y, font=self.fntTxtTup, text=txt, fill=tableclr)

		#planets
		x = 2*self.BORDER+self.signSymbolSize+self.spaceSize+self.monthSize-2*self.spaceSize
		hsym = 0#self.fntPlanets.cget('size')
		for pl in range(planets.Planets.PLANETS_NUM-1): #Moon excepted
			y = plpixelpos[pl]

			if (not self.bw):
				plsclr = util.getRGBTxt(self.options.clrplanets[pl])
			wsym = self.fntPlanets.measure(common.common.signs[pl])
			xoffs = 2*self.spaceSize+wsym/2
			txtId = self.can.create_text(x-xoffs,y-hsym/2+bshift[pl], font=self.fntPlanetsTup, text=common.common.planets[pl], fill=plsclr)

		#top
		hsym = self.fntPlanets.cget('size')
		if (len(plstop) != 0):
			y = yOrig2-2*self.spaceSize
			plstopnum = len(plstop)
			for pl in range(plstopnum):
				x = pltoppixelpos[pl]

				if (not self.bw):
					plsclr = util.getRGBTxt(self.options.clrplanets[plstopids[pl]])
				wsym = 0#self.fntPlanets.measure(plstop[pl])
				yoffs = 2*self.spaceSize+hsym/2

				if (len(plstop) > 1):
					txtId = self.can.create_text(x-wsym/2+bshifttop[pl], y-yoffs, font=self.fntPlanetsTup, text=plstop[pl], fill=plsclr)
				else:
					txtId = self.can.create_text(x-wsym/2, y-yoffs, font=self.fntPlanetsTup, text=plstop[pl], fill=plsclr)

		#bottom
		if (len(plsbottom) != 0):
			y = yOrig+2*self.spaceSize
			plsbootmnum = len(plsbottom)
			for pl in range(plsbottomnum):
				x = plbottompixelpos[pl]

				if (not self.bw):
					plsclr = util.getRGBTxt(self.options.clrplanets[plsbottomids[pl]])
				wsym = 0#self.fntPlanets.measure(plsbottom[pl])
				yoffs = 2*self.spaceSize+hsym/2

				if (len(plsbottom) > 1):
					txtId = self.can.create_text(x-wsym/2+bshiftbottom[pl], y+yoffs, font=self.fntPlanetsTup, text=plsbottom[pl], fill=plsclr)
				else:
					txtId = self.can.create_text(x-wsym/2, y+yoffs, font=self.fntPlanetsTup, text=plsbottom[pl], fill=plsclr)


	def arrange(self, pls, plpixelpos, smallerBOR, greaterBOR):
		'''Arranges bodies so they won't overlap each other'''

		bshift = []
		order = []
		mixed = []

		num = len(plpixelpos)
		for i in range(num):
			order.append(plpixelpos[i])
			mixed.append(i)
			bshift.append(0.0)

		for j in range(num):
			for i in range(num-1):
				if (order[i] > order[i+1]):
					tmp = order[i]
					order[i] = order[i+1]
					order[i+1] = tmp
					tmp = mixed[i]
					mixed[i] = mixed[i+1]
					mixed[i+1] = tmp


		#doArrange arranges consecutive two planets only(0 and 1, 1 and 2, ...), this is why we need to do it length+1 times
		self.w1 = self.fntPlanets.measure('D')
		self.w2 = self.fntPlanets.measure('D')
		shifted = True
		while(shifted):
			shifted = self.doArrange(num, pls, bshift, order, mixed)

		#Arrange borders
		BOR = smallerBOR
		#Left
		if (order[0]+bshift[mixed[0]] < BOR):
			diff = BOR-(order[0]+bshift[mixed[0]])
			bshift[mixed[0]] += diff

			#check the other bodies
			for i in range(num-1):
				w1 = self.fntPlanets.measure(pls[i])
				h1 = self.fntPlanets.cget('size')
				w2 = self.fntPlanets.measure(pls[i+1])
				h2 = self.fntPlanets.cget('size')

				x1 = order[i]+bshift[mixed[i]]
				x2 = order[i+1]+bshift[mixed[i+1]]

				if (order[i]+bshift[mixed[i]] > order[i+1]+bshift[mixed[i+1]] or self.overlap(x1, w1, x2, w2)):
					bshift[mixed[i+1]] += diff
				else:
					break

		#Right
		lenord = num-1

		val = order[lenord]+bshift[mixed[lenord]]
		if (order[lenord]+bshift[mixed[lenord]] > greaterBOR):
			diff = (order[lenord]+bshift[mixed[lenord]])-greaterBOR
			bshift[mixed[lenord]] -= diff

			#check the other bodies
			for i in range(lenord, 0, -1):
				w1 = self.fntPlanets.measure(pls[i-1])
				h1 = self.fntPlanets.cget('size')
				w2 = self.fntPlanets.measure(pls[i])
				h2 = self.fntPlanets.cget('size')

				x1 = order[i-1]+bshift[mixed[i-1]]
				x2 = order[i]+bshift[mixed[i]]

				if (order[i-1]+bshift[mixed[i-1]] > order[i]+bshift[mixed[i]] or self.overlap(x1, w1, x2, w2)):
					bshift[i-1] -= diff
				else:
					break

		return bshift[:]


	def doArrange(self, num, pls, bshift, order, mixed, forward = False):
		shifted = False

		for i in range(num-1):
			if(self.doShift(i, i+1, pls, bshift, order, mixed, forward)):
				shifted = True

		return shifted


	def doShift(self, b1, b2, pls, bshift, order, mixed, forward = False):
		shifted = False

		x1 = order[b1]+bshift[mixed[b1]]
		x2 = order[b2]+bshift[mixed[b2]]

#	Unfortunately this would be too slow
#		w1 = self.fntPlanets.measure(pls[mixed[b1]])
#		h1 = self.fntPlanets.cget('size')
#		w2 = self.fntPlanets.measure(pls[mixed[b2]])
#		h2 = self.fntPlanets.cget('size')

		while (self.overlap(x1, self.w1, x2, self.w2)):
			if (not forward):
				bshift[mixed[b1]] -= 0.1
			bshift[mixed[b2]] += 0.1

			x1 = order[b1]+bshift[mixed[b1]]
			x2 = order[b2]+bshift[mixed[b2]]

			if (not shifted):
				shifted = True

		return shifted


	def overlap(self, x1, w1, x2, w2):
		return (x1 <= x2 and x2 <= x1+w1+self.spaceSize) or (x2 <= x1 and x1 <= x2+w2+self.spaceSize)










