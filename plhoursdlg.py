from tkinter import *
from tkinter import ttk
import plhours
import texts
import util


class PlHoursDlg:

	HOURSPERHALFDAY = 12

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsplhoursdlg['PlanetaryHours'])
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
		tree = ttk.Treeview(frame, columns=('start', 'end'), selectmode='none', height=12)

		tree.column('#0', width=80, anchor='center')
		tree.column('start', width=120, anchor='center')
		tree.column('end', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('start', text=texts.txtsplhoursdlg['Start'])
		tree.heading('end', text=texts.txtsplhoursdlg['End'])
		tagtxts = ('1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12')
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		deg_symbol = '\u00b0'
		self.begtime = 0.0
		if (self.chart.time.ph.daytime):
			begtime = self.chart.time.ph.risetime
		else:
			begtime = self.chart.time.ph.settime
		for i in range(PlHoursDlg.HOURSPERHALFDAY):
			hr = 0
			endtime = 0.0

			if (self.chart.time.ph.daytime):
				endtime = self.chart.time.ph.risetime+self.chart.time.ph.hrlen*(i+1)
				hr = i
			else:
				endtime = self.chart.time.ph.settime+self.chart.time.ph.hrlen*(i+1)
				hr = i+PlHoursDlg.HOURSPERHALFDAY

			planetaryhour = plhours.PlanetaryHours.PHs[self.chart.time.ph.weekday][hr]

			pltxt = texts.planets[planetaryhour]
			h, m, s = self.chart.time.ph.revTime(begtime, self.chart.time.cal)
			txtbeg = str(h)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
			h, m, s = self.chart.time.ph.revTime(endtime, self.chart.time.cal)
			txtend = str(h)+':'+str(m).zfill(2)+':'+str(s).zfill(2)

			if (self.options.clrtextsintablesblack):
				tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[planetaryhour]))
			iid = tree.insert('', 'end', text=pltxt, values=(txtbeg, txtend), tags=tagtxts[i])
			begtime = endtime

		tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
		self.center()


	def ok(self, event=None):
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






