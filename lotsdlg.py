from tkinter import *
from tkinter import ttk
import chart
import lots2
import texts
import util


class Lots2Dlg:

	def __init__(self, parentdlg, parent, chrt, opts):
		self.parentdlg = parentdlg
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtslots2dlg['Lots'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
#		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		self.tree = ttk.Treeview(frame, columns=('name', 'form', 'lon'), selectmode='none', height=10)

#		self.tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		self.tree.column('#0', width=40, anchor='center')
		self.tree.column('name', width=120, anchor='center')
		self.tree.column('formula', width=120, anchor='center')
		self.tree.column('lon', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	self.tree.heading('#0', text='Planets')
		self.tree.heading('name', text=texts.txtslots2dlg['Name'])
		self.tree.heading('form', text=texts.txtslots2dlg['Formula'])
		self.tree.heading('lon', text=texts.txtslots2dlg['Longitude'])
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		if (self.options.clrtextsintablesblack):
			tree.tag_configure('astrotext', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			tree.tag_configure('astrotext', background=bkg_rgb, foreground=txt_rgb)

		self.iids = []
		lotsnum = len(chrt.lots2.data)
		for i in range(lotsnum):
			nametxt = self.chart.lots2.data[i][lots2.Lots2.NAME]
			formulatxt = self.chart.lots2.data[i][lots2.Lots2.FORMULA]
			lon = self.chart.lots2.data[i][lots2.Lots2.LONG]
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)
			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			self.iids.append(self.tree.insert('', 'end', text=str(i+1)+'.', values=(nametxt, formulatxt, lontxt), tags='astrotext'))

		self.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
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

		lotsnum = len(chrt.lots2.data)
		for i in range(lotsnum):
			nametxt = self.chart.lots2.data[i][lots2.Lots2.NAME]
			formulatxt = self.chart.lots2.data[i][lots2.Lots2.FORMULA]
			lon = self.chart.lots2.data[i][lots2.Lots2.LONG]
			if (self.options.ayanamsa != 0):
				lon -= self.chart.ayanamsa
				lon = util.normalize(lon)
			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			self.tree.item(self.iids[i], values=(nametxt, formulatxt, lontxt))


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





