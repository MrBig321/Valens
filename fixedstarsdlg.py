from tkinter import *
from tkinter import ttk
import chart
import fixedstars
import texts
import util


class FixedStarsDlg:

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsfixedstars['Fixedstars'])
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
		tree = ttk.Treeview(frame, columns=('nomname', 'lon', 'lat', 'ra', 'decl'), selectmode='none', height=10)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=120, anchor='center')
		tree.column('nomname', width=100, anchor='center')
		tree.column('lon', width=110, anchor='center')
		tree.column('lat', width=100, anchor='center')
		tree.column('ra', width=110, anchor='center')
		tree.column('decl', width=100, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('nomname', text=texts.txtsfixedstars['Nomencl'])
		tree.heading('lon', text=texts.txtsfixedstars['Longitude'])
		tree.heading('lat', text=texts.txtsfixedstars['Latitude'])
		tree.heading('ra', text=texts.txtsfixedstars['Rectascension'])
		tree.heading('decl', text=texts.txtsfixedstars['Declination'])

		tagtxt = 'star'
		if (self.options.clrtextsintablesblack):
			tree.tag_configure(tagtxt, background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			tree.tag_configure(tagtxt, background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		num = len(self.chart.fixedstars.data)
		for i in range(num):
			name = self.chart.fixedstars.data[i][fixedstars.FixedStars.NAME]
			nnm = self.chart.fixedstars.data[i][fixedstars.FixedStars.NOMNAME]
			lon = self.chart.fixedstars.data[i][fixedstars.FixedStars.LON]
			lat = self.chart.fixedstars.data[i][fixedstars.FixedStars.LAT]
			ra = self.chart.fixedstars.data[i][fixedstars.FixedStars.RA]
			decl = self.chart.fixedstars.data[i][fixedstars.FixedStars.DECL]

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
			lattxt = sign+(str(d)).rjust(2)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#RA
			d, m, s = util.decToDeg(ra)
			ratxt = (str(d)).rjust(3)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			#DECL
			d, m, s = util.decToDeg(decl)
			sign = ''
			if (decl < 0.0):
				sign = '-'
			decltxt = sign+(str(d)).rjust(2)+deg_symbol+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'

			iid = tree.insert('', 'end', text=name, values=(nnm, lontxt, lattxt, ratxt, decltxt), tags=tagtxt)

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






