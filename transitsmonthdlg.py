from tkinter import *
from tkinter import ttk
import chart
import transits
import texts
import util


class TransitsMonthDlg:

	def __init__(self, parent, trans, year, month, opts):
		self.parent = parent
		self.options = opts

		titletxt = texts.txtstransitsmonth['Transits']+'('+str(year)+'.'+texts.months[month-1]+')'

		self.win = Toplevel()
		self.win.title(titletxt)
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
		tree = ttk.Treeview(frame, columns=('time', 'transit'), selectmode='none', height=15)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=50, anchor='center')
		tree.column('time', width=120, anchor='center')
		tree.column('transit', width=300, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

		tree.heading('#0', text=texts.txtstransitsmonth['Day'])
		tree.heading('time', text=texts.txtstransitsmonth['Time']+'('+texts.txtstransitsmonth['GMT']+')')
		tree.heading('transit', text=texts.txtstransitsmonth['Transit'])

		tree.tag_configure('black', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		tree.tag_configure('text', background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		num = len(trans)
		for i in range(num):
			daytxt = str(trans[i].day)
			h, m, s = util.decToDeg(trans[i].time)
			txttime = (str(h)).zfill(2)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)

			txttr = texts.planets[trans[i].plt]+' '
			txtretr = ''
			if (trans[i].pltretr == transits.Transit.RETR):
				txtretr = 'R '
			txtretr2 = ''
			if (trans[i].objretr == transits.Transit.RETR):
				txtretr2 = 'R '

			if (trans[i].objtype == transits.Transit.ASCMC):
				txttr += txtretr+texts.aspects[trans[i].aspect]+' '+texts.ascmc[trans[i].obj]
			if (trans[i].objtype == transits.Transit.PLANET):
				txttr += txtretr+texts.aspects[trans[i].aspect]+' '+texts.planets[trans[i].obj]+' '+txtretr2
			if (trans[i].objtype == transits.Transit.SIGN):
				s2 = texts.signs[trans[i].obj]
				s1 = texts.signs[11]
				if (trans[i].obj > 0):
					s1 = texts.signs[trans[i].obj-1]
				txttr += txtretr+s1+' | '+s2
			if (trans[i].objtype == transits.Transit.ANTISCION):
				txttr += txtretr+texts.aspects[trans[i].aspect]+' Ant '+texts.planets[trans[i].obj]+' '+txtretr

			if (trans[i].objtype == transits.Transit.LOT):
				txttr += txtretr+texts.aspects[trans[i].aspect]+' '+texts.lotsList[trans[i].obj]

			if (trans[i].objtype == transits.Transit.SYZYGY):
				txttr += txtretr+texts.aspects[trans[i].aspect]+' '+texts.txtscommon['Syzygy']

			if (self.options.clrtextsintablesblack):
				iid = tree.insert('', 'end', text=daytxt, values=(txttime, txttr), tags='black')
			else:
				iid = tree.insert('', 'end', text=daytxt, values=(txttime, txttr), tags='text')

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
#		self.win.grab_set()							# events go only to this wnd (this makes Modal-Dialog)
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






