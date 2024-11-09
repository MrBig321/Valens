from tkinter import *
from tkinter import ttk
import houses
import texts
import util


class MiscDlg:

	SIDTIME = 0
	OBL = 1
	JD = 2

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsmisc['Misc'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		tree = ttk.Treeview(frame, columns=('data'), selectmode='none', height=5)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=120, anchor='center')
		tree.column('data', width=160, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('data', text=texts.txtsmisc['Data'])
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		if (self.options.clrtextsintablesblack):
			tree.tag_configure('astrotext', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			tree.tag_configure('astrotext', background=bkg_rgb, foreground=txt_rgb)

		txts = (texts.txtsmisc['SidTime'], texts.txtsmisc['OblEcl'], texts.txtsmisc['JulianDay'])
		data = (self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.RA]/15.0, self.chart.obl[0], self.chart.time.jd)
		deg_symbol = '\u00b0'
		dnum = len(txts)
		for i in range(dnum):
			d, m, s = util.decToDeg(data[i])

			if (i == MiscDlg.SIDTIME):
				txt = str(d)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)
			elif i == (MiscDlg.OBL):
				txt = (str(d)).rjust(2)+deg_symbol+(str(m)).zfill(2)+"'"+(str(s)).zfill(2)+'"'
			elif i == (MiscDlg.JD):
				txt = str('{0:.6f}'.format(data[i]))
				txt = str(data[i])

			iid = tree.insert('', 'end', text=txts[i], values=(txt), tags='astrotext')

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






