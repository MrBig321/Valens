from tkinter import *
from tkinter import ttk
import chart
import houses
import planet
import planets
import modernplanets
import placspec
import texts
import util


class Speculum1Dlg:

	def __init__(self, parentdlg, parent, chrt, opts):
		self.parentdlg = parentdlg
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsspeculum['Speculum1'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
#		frame.configure(width=300)
#		frame.grid_columnconfigure(0, weight=1)
#		frame.grid_rowconfigure(0, weight=1)
#		frame.columnconfigure(0, weight=1)
#		frame.rowconfigure(0, weight=1)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		self.deg_symbol = '\u00b0'
#		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		self.tree = ttk.Treeview(frame, columns=('dir', 'long', 'lat', 'ra', 'decl'), selectmode='none', height=9)

#		self.tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		self.tree.column('#0', width=80, anchor='center')
		self.tree.column('dir', width=40, anchor='center')
		self.tree.column('long', width=120, anchor='center')
		self.tree.column('lat', width=120, anchor='center')
		self.tree.column('ra', width=120, anchor='center')
		self.tree.column('decl', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	self.tree.heading('#0', text='Planets')
		self.tree.heading('dir', text=texts.txtsspeculum['Dir'])
		self.tree.heading('long', text=texts.txtsspeculum['Longitude'])
		self.tree.heading('lat', text=texts.txtsspeculum['Latitude'])
		self.tree.heading('ra', text=texts.txtsspeculum['Rectascension'])
		self.tree.heading('decl', text=texts.txtsspeculum['Declination'])

		self.iids = []

		if (self.options.clrtextsintablesblack):
			self.tree.tag_configure('ascmc', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			self.tree.tag_configure('ascmc', background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))
		#Asc
		lon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			lon -= self.chart.ayanamsa
			lon = util.normalize(lon)
		d, m, s = util.decToDeg(lon)
		sign = int(d/chart.Chart.SIGN_DEG)
		pos = int(d%chart.Chart.SIGN_DEG)
		lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		lat = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LAT]
		d, m, s = util.decToDeg(lat)
		sign = ''
		if (lat < 0.0):
			sign = '-'
		lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		ra = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.RA] 
		d, m, s = util.decToDeg(ra)
		ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		decl = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.DECL] 
		d, m, s = util.decToDeg(decl)
		sign = ''
		if (decl < 0.0):
			sign = '-'
		decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		self.iids.append(self.tree.insert('', 'end', text=texts.txtsspeculum['Asc'], values=('', lontxt, lattxt, ratxt, decltxt), tags='ascmc'))
		#MC
		lon = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			lon -= self.chart.ayanamsa
			lon = util.normalize(lon)
		d, m, s = util.decToDeg(lon)
		sign = int(d/chart.Chart.SIGN_DEG)
		pos = int(d%chart.Chart.SIGN_DEG)
		lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		lat = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.LAT]
		d, m, s = util.decToDeg(lat)
		sign = ''
		if (lat < 0.0):
			sign = '-'
		lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		ra = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.RA] 
		d, m, s = util.decToDeg(ra)
		ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		decl = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.DECL] 
		d, m, s = util.decToDeg(decl)
		sign = ''
		if (decl < 0.0):
			sign = '-'
		decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		self.iids.append(self.tree.insert('', 'end', text=texts.txtsspeculum['MC'], values=('', lontxt, lattxt, ratxt, decltxt), tags='ascmc'))
		#Planets
		tagtxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag', 'moontag', 'anodetag')
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		plnum = len(texts.planets)
		for i in range(plnum):
			lon = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.LON]
			lat = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.LAT]
			ra = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.RA]
			decl = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.DECL]

			#direction
			dirtxt = ''
			if (self.chart.planets.planets[i].data[planet.Planet.SPLON] < 0.0):
				dirtxt = 'R'

			#lon
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)

			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#LAT
			d, m, s = util.decToDeg(lat)
			sign = ''
			if (lat < 0.0):
				sign = '-'
			if (i == planets.Planets.SUN):#Sun's latitude is always zero
				d, m, s = 0, 0, 0
				sign = ''
			lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#RA
			d, m, s = util.decToDeg(ra)
			ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#DECL
			d, m, s = util.decToDeg(decl)
			sign = ''
			if (decl < 0.0):
				sign = '-'
			decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			if (self.options.clrtextsintablesblack):
				self.tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				self.tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))
			self.iids.append(self.tree.insert('', 'end', text=texts.planets[i], values=(dirtxt, lontxt, lattxt, ratxt, decltxt), tags=tagtxts[i]))

		#Modern
		moderntagtxts = ('uranustag', 'neptunetag', 'plutotag')
		for i in range(modernplanets.Planets.PLANETS_NUM):
			lon = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.LON]
			lat = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.LAT]
			ra = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.RA]
			decl = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.DECL]

			#direction
			dirtxt = ''
			if (self.chart.modernplanets.planets[i].data[planet.Planet.SPLON] < 0.0):
				dirtxt = 'R'

			#lon
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)

			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#LAT
			d, m, s = util.decToDeg(lat)
			sign = ''
			if (lat < 0.0):
				sign = '-'
			lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#RA
			d, m, s = util.decToDeg(ra)
			ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#DECL
			d, m, s = util.decToDeg(decl)
			sign = ''
			if (decl < 0.0):
				sign = '-'
			decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			if (self.options.clrtextsintablesblack):
				self.tree.tag_configure(moderntagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				self.tree.tag_configure(moderntagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))
			self.iids.append(self.tree.insert('', 'end', text=texts.modernplanets[i], values=(dirtxt, lontxt, lattxt, ratxt, decltxt), tags=moderntagtxts[i]))

		self.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
#		self.allright = False
		self.center()
#		self.win.geometry('%dx%d+%d+%d' % (400, 300, 0, 0))
#		self.win.update_idletasks()


	def ok(self, event=None):
#		self.allright = True
		self.destroy()


	def doModal(self, modal=False):
		self.win.focus_set()
		if (modal):
			self.win.grab_set()							# events go only to this wnd (this makes Modal-Dialog)
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def updateWnd(self, chrt, opts, chrt2):
		if (chrt2 != None):
			self.chart = chrt2
		if (opts != None):
			self.options = opts

		#Asc
		lon = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			lon -= self.chart.ayanamsa
			lon = util.normalize(lon)
		d, m, s = util.decToDeg(lon)
		sign = int(d/chart.Chart.SIGN_DEG)
		pos = int(d%chart.Chart.SIGN_DEG)
		lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		lat = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.LAT]
		d, m, s = util.decToDeg(lat)
		sign = ''
		if (lat < 0.0):
			sign = '-'
		lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		ra = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.RA] 
		d, m, s = util.decToDeg(ra)
		ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		decl = self.chart.houses.ascmc[houses.Houses.ASC][houses.Houses.DECL] 
		d, m, s = util.decToDeg(decl)
		sign = ''
		if (decl < 0.0):
			sign = '-'
		decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

		self.tree.item(self.iids[0], values=('', lontxt, lattxt, ratxt, decltxt))

		#MC
		lon = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.LON]
		if (self.options.ayanamsa != 0):
			lon -= self.chart.ayanamsa
			lon = util.normalize(lon)
		d, m, s = util.decToDeg(lon)
		sign = int(d/chart.Chart.SIGN_DEG)
		pos = int(d%chart.Chart.SIGN_DEG)
		lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		lat = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.LAT]
		d, m, s = util.decToDeg(lat)
		sign = ''
		if (lat < 0.0):
			sign = '-'
		lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		ra = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.RA] 
		d, m, s = util.decToDeg(ra)
		ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		decl = self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.DECL] 
		d, m, s = util.decToDeg(decl)
		sign = ''
		if (decl < 0.0):
			sign = '-'
		decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

		self.tree.item(self.iids[1], values=('', lontxt, lattxt, ratxt, decltxt))

		#Planets
		plnum = len(texts.planets)
		for i in range(plnum):
			lon = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.LON]
			lat = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.LAT]
			ra = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.RA]
			decl = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.DECL]

			#direction
			dirtxt = ''
			if (self.chart.planets.planets[i].data[planet.Planet.SPLON] < 0.0):
				dirtxt = 'R'

			#lon
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)

			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#LAT
			d, m, s = util.decToDeg(lat)
			sign = ''
			if (lat < 0.0):
				sign = '-'
			if (i == planets.Planets.SUN):#Sun's latitude is always zero
				d, m, s = 0, 0, 0
				sign = ''
			lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#RA
			d, m, s = util.decToDeg(ra)
			ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#DECL
			d, m, s = util.decToDeg(decl)
			sign = ''
			if (decl < 0.0):
				sign = '-'
			decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			self.tree.item(self.iids[i+2], values=(dirtxt, lontxt, lattxt, ratxt, decltxt))

		#Modern Planets
		for i in range(modernplanets.Planets.PLANETS_NUM):
			lon = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.LON]
			lat = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.LAT]
			ra = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.RA]
			decl = self.chart.modernplanets.planets[i].speculum.data[placspec.PlacidianSpeculum.DECL]

			#direction
			dirtxt = ''
			if (self.chart.modernplanets.planets[i].data[planet.Planet.SPLON] < 0.0):
				dirtxt = 'R'

			#lon
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)

			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#LAT
			d, m, s = util.decToDeg(lat)
			sign = ''
			if (lat < 0.0):
				sign = '-'
			lattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#RA
			d, m, s = util.decToDeg(ra)
			ratxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#DECL
			d, m, s = util.decToDeg(decl)
			sign = ''
			if (decl < 0.0):
				sign = '-'
			decltxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			self.tree.item(self.iids[i+2+plnum], values=(dirtxt, lontxt, lattxt, ratxt, decltxt))


	def destroy(self):
		self.win.destroy()
		if (self.parentdlg != None):
			self.parentdlg.destroying(self)


	def center(self):
		self.win.withdraw()
		self.win.update_idletasks()
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		w = self.win.winfo_reqwidth()
		h = self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()






