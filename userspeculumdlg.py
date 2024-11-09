from tkinter import *
from tkinter import ttk
import chart
import placspec
import texts
import util


class UserSpeculumDlg:

	def __init__(self, parent, spec, ayan, opts):
		self.parent = parent
		self.spec = spec
		self.ayan = ayan
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsspeculum['Speculum'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		deg_symbol = '\u00b0'
#		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		tree = ttk.Treeview(frame, columns=('data'), selectmode='none', height=10)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=120, anchor='center')
		tree.column('data', width=100, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('data', text=texts.txtsspeculum['Data'])

		if (self.options.clrtextsintablesblack):
			tree.tag_configure('texts', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			tree.tag_configure('texts', background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))

		txts = (texts.txtsspeculum['Longitude'], texts.txtsspeculum['Latitude'], texts.txtsspeculum['Rectascension'], texts.txtsspeculum['Declination'], texts.txtsspeculum['AscDiffLat'], texts.txtsspeculum['Semiarcus'], texts.txtsspeculum['Meridiandist'], texts.txtsspeculum['Horizondist'], texts.txtsspeculum['TemporalHour'], texts.txtsspeculum['HourlyDist']) 

		for i  in range(placspec.PlacidianSpeculum.HOD+1):
			val = spec.data[i]
			txt = ''
			if (i == placspec.PlacidianSpeculum.LON):
				if (self.options.ayanamsa != 0):
					val -= ayan
					val = util.normalize(val)
				d, m, s = util.decToDeg(val)
				sign = int(d/chart.Chart.SIGN_DEG)
				pos = int(d%chart.Chart.SIGN_DEG)
				txt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.LAT):
				d, m, s = util.decToDeg(val)
				sign = ''
				if (val < 0.0):
					sign = '-'
				txt = sign+(str(d)).rjust(2)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.RA):
				d, m, s = util.decToDeg(val)
				txt = (str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.DECL):
				d, m, s = util.decToDeg(val)
				sign = ''
				if (val < 0.0):
					sign = '-'
				txt = sign+(str(d)).rjust(2)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.ADLAT):
				d, m, s = util.decToDeg(val)
				sign = ''
				if (val < 0.0):
					sign = '-'
				txt = sign+(str(d)).rjust(2)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.SA):
				d, m, s = util.decToDeg(val)
				sign = 'D'
				if (val < 0.0):
					sign = 'N'
				txt = sign+(str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.MD):
				d, m, s = util.decToDeg(val)
				sign = 'M'
				if (val < 0.0):
					sign = 'I'
				txt = sign+(str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.HD):
				d, m, s = util.decToDeg(val)
				sign = 'A'
				if (val < 0.0):
					sign = 'D'
				txt = sign+(str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.TH):
				d, m, s = util.decToDeg(val)
				sign = 'D'
				if (val < 0.0):
					sign = 'N'
				txt = sign+(str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			elif (i == placspec.PlacidianSpeculum.HOD):
				d, m, s = util.decToDeg(val)
				sign = 'D'
				if (val < 0.0):
					sign = 'N'
				txt = sign+(str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'


			iid = tree.insert('', 'end', text=txts[i], values=(txt, ), tags='texts')

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


	def doModal(self, modal=False):
		self.win.focus_set()
		if (modal):
			self.win.grab_set()							# events go only to this wnd (this makes Modal-Dialog)
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






