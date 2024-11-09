from tkinter import *
from tkinter import ttk
import chart
import modernplanets
import placspec
import texts
import util


class Speculum2Dlg:

	def __init__(self, parentdlg, parent, chrt, opts):
		self.parentdlg = parentdlg
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsspeculum['Speculum2'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
#		frame.configure(width=300)
#		frame.grid_columnconfigure(0, weight=1)
#		frame.grid_rowconfigure(0, weight=1)
#		frame.columnconfigure(0, weight=1)
#		frame.rowconfigure(0, weight=1)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
#		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		self.tree = ttk.Treeview(frame, columns=('adlat', 'sa', 'md', 'hd', 'th', 'hod'), selectmode='none', height=8)#, 'pmp', 'adph', 'poh', 'aodo'), selectmode='none')#, height=20)

#		self.tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		self.tree.column('#0', width=100, anchor='center')
		self.tree.column('adlat', width=120, anchor='center')
		self.tree.column('sa', width=120, anchor='center')
		self.tree.column('md', width=120, anchor='center')
		self.tree.column('hd', width=120, anchor='center')
		self.tree.column('th', width=120, anchor='center')
		self.tree.column('hod', width=120, anchor='center')
#		self.tree.column('pmp', width=120, anchor='center')
#		self.tree.column('adph', width=120, anchor='center')
#		self.tree.column('poh', width=120, anchor='center')
#		self.tree.column('aodo', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	self.tree.heading('#0', text='Planets')
		self.tree.heading('adlat', text=texts.txtsspeculum['AscDiffLat'])
		self.tree.heading('sa', text=texts.txtsspeculum['Semiarcus'])
		self.tree.heading('md', text=texts.txtsspeculum['Meridiandist'])
		self.tree.heading('hd', text=texts.txtsspeculum['Horizondist'])
		self.tree.heading('th', text=texts.txtsspeculum['TemporalHour'])
		self.tree.heading('hod', text=texts.txtsspeculum['HourlyDist'])
#		self.tree.heading('pmp', text=texts.txtsspeculum['PMP'])
#		self.tree.heading('adph', text=texts.txtsspeculum['AscDiffPole'])
#		self.tree.heading('poh', text=texts.txtsspeculum['PoleHeight'])
#		self.tree.heading('aodo', text=texts.txtsspeculum['AODO'])
		tagtxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag', 'moontag', 'anodetag')
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		self.deg_symbol = '\u00b0'

		self.iids = []
		plnum = len(texts.planets)
		for i in range(plnum):
			adlat = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADLAT]
			sa = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.SA]
			md = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.MD]
			hd = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HD]
			th = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.TH]
			hod = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HOD]
#			pmp = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.PMP]
#			adph = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADPH]
#			poh = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.POH]
#			aodo = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.AODO]

			#ADLAT
			d, m, s = util.decToDeg(adlat)
			sign = ''
			if (adlat < 0.0):
				sign = '-'
			adlattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#SA
			d, m, s = util.decToDeg(sa)
			sign = 'D'
			if (sa < 0.0):
				sign = 'N'
			satxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#MD
			d, m, s = util.decToDeg(md)
			sign = 'M'
			if (md < 0.0):
				sign = 'I'
			mdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HD
			d, m, s = util.decToDeg(hd)
			sign = 'A'
			if (hd < 0.0):
				sign = 'D'
			hdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#TH
			d, m, s = util.decToDeg(th)
			sign = 'D'
			if (th < 0.0):
				sign = 'N'
			thtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HOD
			d, m, s = util.decToDeg(hod)
			sign = 'D'
			if (hod < 0.0):
				sign = 'N'
			hodtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#PMP
#			d, m, s = util.decToDeg(pmp)
#			pmptxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#ADPH
#			d, m, s = util.decToDeg(adph)
#			adphtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#POH
#			d, m, s = util.decToDeg(poh)
#			pohtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#AODO
#			d, m, s = util.decToDeg(aodo)
#			sign = 'A'
#			if (aodo < 0.0):
#				sign = 'D'
#			aodotxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			if (self.options.clrtextsintablesblack):
				self.tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				self.tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))
#			iid = self.tree.insert('', 'end', text=texts.planets[i], values=(adlattxt, satxt, mdtxt, hdtxt, thtxt, hodtxt, pmptxt, adphtxt, pohtxt, aodotxt), tags=tagtxts[i])
			self.iids.append(self.tree.insert('', 'end', text=texts.planets[i], values=(adlattxt, satxt, mdtxt, hdtxt, thtxt, hodtxt), tags=tagtxts[i]))

		#Modern
		moderntagtxts = ('uranustag', 'neptunetag', 'plutotag')
		for i in range(modernplanets.Planets.PLANETS_NUM):
			adlat = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADLAT]
			sa = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.SA]
			md = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.MD]
			hd = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HD]
			th = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.TH]
			hod = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HOD]
#			pmp = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.PMP]
#			adph = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADPH]
#			poh = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.POH]
#			aodo = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.AODO]

			#ADLAT
			d, m, s = util.decToDeg(adlat)
			sign = ''
			if (adlat < 0.0):
				sign = '-'
			adlattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#SA
			d, m, s = util.decToDeg(sa)
			sign = 'D'
			if (sa < 0.0):
				sign = 'N'
			satxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#MD
			d, m, s = util.decToDeg(md)
			sign = 'M'
			if (md < 0.0):
				sign = 'I'
			mdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HD
			d, m, s = util.decToDeg(hd)
			sign = 'A'
			if (hd < 0.0):
				sign = 'D'
			hdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#TH
			d, m, s = util.decToDeg(th)
			sign = 'D'
			if (th < 0.0):
				sign = 'N'
			thtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HOD
			d, m, s = util.decToDeg(hod)
			sign = 'D'
			if (hod < 0.0):
				sign = 'N'
			hodtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#PMP
#			d, m, s = util.decToDeg(pmp)
#			pmptxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#ADPH
#			d, m, s = util.decToDeg(adph)
#			adphtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#POH
#			d, m, s = util.decToDeg(poh)
#			pohtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#AODO
#			d, m, s = util.decToDeg(aodo)
#			sign = 'A'
#			if (aodo < 0.0):
#				sign = 'D'
#			aodotxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			if (self.options.clrtextsintablesblack):
				self.tree.tag_configure(moderntagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				self.tree.tag_configure(moderntagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))
			self.iids.append(self.tree.insert('', 'end', text=texts.modernplanets[i], values=(adlattxt, satxt, mdtxt, hdtxt, thtxt, hodtxt), tags=moderntagtxts[i]))

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
			self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def updateWnd(self, chrt, opts, chrt2):
		if (chrt2 != None):
			self.chart = chrt2
		if (opts != None):
			self.options = opts

		plnum = len(texts.planets)
		for i in range(plnum):
			adlat = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADLAT]
			sa = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.SA]
			md = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.MD]
			hd = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HD]
			th = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.TH]
			hod = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HOD]
#			pmp = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.PMP]
#			adph = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADPH]
#			poh = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.POH]
#			aodo = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.AODO]

			#ADLAT
			d, m, s = util.decToDeg(adlat)
			sign = ''
			if (adlat < 0.0):
				sign = '-'
			adlattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#SA
			d, m, s = util.decToDeg(sa)
			sign = 'D'
			if (sa < 0.0):
				sign = 'N'
			satxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#MD
			d, m, s = util.decToDeg(md)
			sign = 'M'
			if (md < 0.0):
				sign = 'I'
			mdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HD
			d, m, s = util.decToDeg(hd)
			sign = 'A'
			if (hd < 0.0):
				sign = 'D'
			hdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#TH
			d, m, s = util.decToDeg(th)
			sign = 'D'
			if (th < 0.0):
				sign = 'N'
			thtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HOD
			d, m, s = util.decToDeg(hod)
			sign = 'D'
			if (hod < 0.0):
				sign = 'N'
			hodtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#PMP
#			d, m, s = util.decToDeg(pmp)
#			pmptxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#ADPH
#			d, m, s = util.decToDeg(adph)
#			adphtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#POH
#			d, m, s = util.decToDeg(poh)
#			pohtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#AODO
#			d, m, s = util.decToDeg(aodo)
#			sign = 'A'
#			if (aodo < 0.0):
#				sign = 'D'
#			aodotxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			self.tree.item(self.iids[i], values=(adlattxt, satxt, mdtxt, hdtxt, thtxt, hodtxt))

		#Modern
		moderntagtxts = ('uranustag', 'neptunetag', 'plutotag')
		for i in range(modernplanets.Planets.PLANETS_NUM):
			adlat = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADLAT]
			sa = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.SA]
			md = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.MD]
			hd = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HD]
			th = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.TH]
			hod = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.HOD]
#			pmp = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.PMP]
#			adph = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.ADPH]
#			poh = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.POH]
#			aodo = self.chart.planets.planets[i].speculum.data[placspec.PlacidianSpeculum.AODO]

			#ADLAT
			d, m, s = util.decToDeg(adlat)
			sign = ''
			if (adlat < 0.0):
				sign = '-'
			adlattxt = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#SA
			d, m, s = util.decToDeg(sa)
			sign = 'D'
			if (sa < 0.0):
				sign = 'N'
			satxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#MD
			d, m, s = util.decToDeg(md)
			sign = 'M'
			if (md < 0.0):
				sign = 'I'
			mdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HD
			d, m, s = util.decToDeg(hd)
			sign = 'A'
			if (hd < 0.0):
				sign = 'D'
			hdtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#TH
			d, m, s = util.decToDeg(th)
			sign = 'D'
			if (th < 0.0):
				sign = 'N'
			thtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#HOD
			d, m, s = util.decToDeg(hod)
			sign = 'D'
			if (hod < 0.0):
				sign = 'N'
			hodtxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#PMP
#			d, m, s = util.decToDeg(pmp)
#			pmptxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#ADPH
#			d, m, s = util.decToDeg(adph)
#			adphtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#POH
#			d, m, s = util.decToDeg(poh)
#			pohtxt = (str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#AODO
#			d, m, s = util.decToDeg(aodo)
#			sign = 'A'
#			if (aodo < 0.0):
#				sign = 'D'
#			aodotxt = sign+(str(d)).rjust(3)+self.deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			self.tree.item(self.iids[plnum+i], values=(adlattxt, satxt, mdtxt, hdtxt, thtxt, hodtxt))


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






