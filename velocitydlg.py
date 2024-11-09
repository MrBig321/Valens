from tkinter import *
from tkinter import ttk
import planet
import texts
import util


class VelocityDlg:

	def __init__(self, parentdlg, parent, chrt, opts):
		self.parentdlg = parentdlg
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsvelocity['Velocity'])
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
		self.tree = ttk.Treeview(frame, columns=('inlong', 'inlat'), selectmode='none', height=8)

#		self.tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		self.tree.column('#0', width=80, anchor='center')
		self.tree.column('inlong', width=120, anchor='center')
		self.tree.column('inlat', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	self.tree.heading('#0', text='Planets')
		self.tree.heading('inlong', text=texts.txtsvelocity['InLong'])
		self.tree.heading('inlat', text=texts.txtsvelocity['InLat'])
		tagtxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag', 'moontag', 'anodetag')
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		self.deg_symbol = '\u00b0'

		self.iids = []
		plnum = len(texts.planets)
		for i in range(plnum):
			splon = self.chart.planets.planets[i].data[planet.Planet.SPLON]
			splat = self.chart.planets.planets[i].data[planet.Planet.SPLAT]

			d,m,s = util.decToDeg(splon)
			sign = ''
			if (splon < 0.0):
				sign = '-'
			txtsplon = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'

			d,m,s = util.decToDeg(splat)
			sign = ''
			if (splat < 0.0):
				sign = '-'
			txtsplat = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'

			if (self.options.clrtextsintablesblack):
				self.tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				self.tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))
			self.iids.append(self.tree.insert('', 'end', text=texts.planets[i], values=(txtsplon, txtsplat), tags=tagtxts[i]))

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
			splon = self.chart.planets.planets[i].data[planet.Planet.SPLON]
			splat = self.chart.planets.planets[i].data[planet.Planet.SPLAT]

			d,m,s = util.decToDeg(splon)
			sign = ''
			if (splon < 0.0):
				sign = '-'
			txtsplon = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'

			d,m,s = util.decToDeg(splat)
			sign = ''
			if (splat < 0.0):
				sign = '-'
			txtsplat = sign+(str(d)).rjust(2)+self.deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'

			self.tree.item(self.iids[i], values=(txtsplon, txtsplat))


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






