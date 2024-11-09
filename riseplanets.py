from tkinter import *
from tkinter import ttk
import riseset
import texts
import util


class RisePlanetsDlg:

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtriseset['RiseSet'])
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
		tree = ttk.Treeview(frame, columns=('rise', 'mc', 'set', 'ic'), selectmode='none', height=10)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=80, anchor='center')
		tree.column('rise', width=120, anchor='center')
		tree.column('mc', width=120, anchor='center')
		tree.column('set', width=120, anchor='center')
		tree.column('ic', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('rise', text=texts.txtsriseset['Rise'])
		tree.heading('mc', text=texts.txtsriseset['MC'])
		tree.heading('set', text=texts.txtsriseset['Set'])
		tree.heading('ic', text=texts.txtsriseset['IC'])
		tagtxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag', 'moontag')
#		ttk.Style().configure('Treeview', background="#383838", foreground="green", fieldbackground="red")
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		plnum = len(texts.planets)-1
		for i in range(plnum):
			h,m,s = util.decToDeg(self.chart.riseset.times[i][riseset.RiseSet.RISE])
			txtrise = (str(h)).zfill(2)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)
			h,m,s = util.decToDeg(self.chart.riseset.times[i][riseset.RiseSet.MC])
			txtmc = (str(h)).zfill(2)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)
			h,m,s = util.decToDeg(self.chart.riseset.times[i][riseset.RiseSet.SET])
			txtset = (str(h)).zfill(2)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)
			h,m,s = util.decToDeg(self.chart.riseset.times[i][riseset.RiseSet.IC])
			txtic = (str(h)).zfill(2)+':'+(str(m)).zfill(2)+':'+(str(s)).zfill(2)

			tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))
			iid = tree.insert('', 'end', text=texts.planets[i], values=(txtrise, txtmc, txtset, txtic), tags=tagtxts[i])

		tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

#		self.allright = False
		self.center()
#		self.win.geometry('%dx%d+%d+%d' % (400, 300, 0, 0))
#		self.win.update_idletasks()


	def ok(self):
#		self.allright = True
		self.destroy()


	def doModal(self):
		self.win.focus_set()
		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def cancel(self):
#		self.allright = False
		self.destroy()


	def destroy(self):
		self.win.destroy()


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






