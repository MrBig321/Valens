from tkinter import *
from tkinter import ttk
import chart
import planet
import planets
import texts
import util


class MidpointsDlg:

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtscommon['Midpoints'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
#		frame.configure(width=300)
#		frame.grid_columnconfigure(0, weight=1)
#		frame.grid_rowconfigure(0, weight=1)
#		frame.columnconfigure(0, weight=1)
#		frame.rowconfigure(0, weight=1)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		deg_symbol = '\u00b0'
#		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		tree = ttk.Treeview(frame, columns=('jup', 'mar', 'sun', 'ven', 'mer', 'moo'), selectmode='none', height=6)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=80, anchor='center')
		tree.column('jup', width=100, anchor='center')
		tree.column('mar', width=100, anchor='center')
		tree.column('sun', width=100, anchor='center')
		tree.column('ven', width=100, anchor='center')
		tree.column('mer', width=100, anchor='center')
		tree.column('moo', width=100, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('jup', text=texts.txtscommon['Jupiter'])
		tree.heading('mar', text=texts.txtscommon['Mars'])
		tree.heading('sun', text=texts.txtscommon['Sun'])
		tree.heading('ven', text=texts.txtscommon['Venus'])
		tree.heading('mer', text=texts.txtscommon['Mercury'])
		tree.heading('moo', text=texts.txtscommon['Moon'])

		#Planets
		tagtxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag')
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		ar = (6, 5, 4, 3, 2, 1)
		summa = 0
		for i in range(planets.Planets.PLANETS_NUM-1):
			artxt = []
			for j in range(planets.Planets.PLANETS_NUM-1-ar[i]):
				artxt.append('')	
			
			for j in range(ar[i]):
				lon = self.chart.midpoints.mids[summa+j].m
				if (self.options.ayanamsa != 0):
					lon -= self.chart.ayanamsa
					lon = util.normalize(lon)
				d, m, s = util.decToDeg(lon)
				sign = int(d/chart.Chart.SIGN_DEG)
				pos = int(d%chart.Chart.SIGN_DEG)
				lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
				artxt.append(lontxt)	

			summa += ar[i]

			if (self.options.clrtextsintablesblack):
				tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))
			iid = tree.insert('', 'end', text=texts.planets[i], values=(artxt), tags=tagtxts[i])

		tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

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


	def doModal(self):
		self.win.focus_set()
#		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def destroy(self):
		self.win.destroy()
		if (self.parent != None):
			self.parent.destroying(self)


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






