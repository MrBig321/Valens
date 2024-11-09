from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font  #
import common
import lots
import options
import texts


class AppearanceDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsappearancedlg['Appearance'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Chart Panel
		chartpanel = ttk.LabelFrame(frame, text=texts.txtsappearancedlg['Chart'])
		chartpanel.grid(column=0, row=0, padx=AppearanceDlg.PANELDISTX, pady=AppearanceDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.chartformat = StringVar()
		hellbtn = ttk.Radiobutton(chartpanel, text=texts.txtsappearancedlg['Hellenistic'], variable=self.chartformat, value='hell')
		hellbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		roundbtn = ttk.Radiobutton(chartpanel, text=texts.txtsappearancedlg['Round'], variable=self.chartformat, value='round')
		roundbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.chartformat.set('hell')

		#General Panel
		generalpanel = ttk.LabelFrame(frame, text=texts.txtsappearancedlg['General'])
		generalpanel.grid(column=0, row=1, padx=AppearanceDlg.PANELDISTX, pady=AppearanceDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.boundsH = BooleanVar()
		boundsHbtn = ttk.Checkbutton(generalpanel, text=texts.txtsappearancedlg['BoundsH'], variable=self.boundsH, onvalue=True)
		boundsHbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.boundsH.set(False)
		self.boundsR = BooleanVar()
		boundsRbtn = ttk.Checkbutton(generalpanel, text=texts.txtsappearancedlg['BoundsR'], variable=self.boundsR, onvalue=True)
		boundsRbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.boundsR.set(False)
		self.topo = BooleanVar()
		topobtn = ttk.Checkbutton(generalpanel, text=texts.txtsappearancedlg['Topocentric'], variable=self.topo, onvalue=True)
		topobtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.topo.set(False)
		self.show = BooleanVar()
		showbtn = ttk.Checkbutton(generalpanel, text=texts.txtsappearancedlg['ShowData'], variable=self.show, onvalue=True)
		showbtn.grid(column=0, row=3, padx=5, pady=5, sticky=(W))
		self.show.set(False)
		self.cuspspos = BooleanVar()
		cuspsposbtn = ttk.Checkbutton(generalpanel, text=texts.txtsappearancedlg['ShowCuspsPos'], variable=self.cuspspos, onvalue=True)
		cuspsposbtn.grid(column=0, row=4, padx=5, pady=5, sticky=(W))
		self.cuspspos.set(False)

		#Outer Panel
		outerpanel = ttk.LabelFrame(frame, text=texts.txtsappearancedlg['Outer'])
		outerpanel.grid(column=0, row=2, rowspan=2, padx=AppearanceDlg.PANELDISTX, pady=AppearanceDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.outer = StringVar()
		nonebtn = ttk.Radiobutton(outerpanel, text=texts.txtsappearancedlg['None'], variable=self.outer, value='none')
		nonebtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		antisbtn = ttk.Radiobutton(outerpanel, text=texts.txtsappearancedlg['Antiscia'], variable=self.outer, value='antis')
		antisbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		dodecbtn = ttk.Radiobutton(outerpanel, text=texts.txtsappearancedlg['Dodecatemoria'], variable=self.outer, value='dodec')
		dodecbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.outer.set('none')

		astroFont = font.Font(family='Valens', size=14)
#		astroFont = ('Valens', 14)
		#Lots
		lotspanel = ttk.LabelFrame(frame, text=texts.txtsappearancedlg['Lots'])
		lotspanel.grid(column=1, row=0, rowspan=3, padx=AppearanceDlg.PANELDISTX, pady=AppearanceDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.fortune = BooleanVar()
		fortunebtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Fortune'], variable=self.fortune, onvalue=True)
		fortunebtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.fortune.set(True)
		fortunesym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.FORTUNE])
		fortunesym.grid(column=1, row=0, padx=5, pady=5, sticky=(W))

		self.spirit = BooleanVar()
		spiritbtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Spirit'], variable=self.spirit, onvalue=True)
		spiritbtn.grid(column=0, row=1, padx=5, pady=3, sticky=(W))
		self.spirit.set(True)
		spiritsym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.SPIRIT])
		spiritsym.grid(column=1, row=1, padx=5, pady=3, sticky=(W))

		self.eros = BooleanVar()
		erosbtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Eros'], variable=self.eros, onvalue=True)
		erosbtn.grid(column=0, row=2, padx=5, pady=3, sticky=(W))
		self.eros.set(False)
		erossym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.EROS])
		erossym.grid(column=1, row=2, padx=5, pady=3, sticky=(W))

		self.victory = BooleanVar()
		victorybtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Victory'], variable=self.victory, onvalue=True)
		victorybtn.grid(column=0, row=3, padx=5, pady=3, sticky=(W))
		self.victory.set(False)
		victorysym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.VICTORY])
		victorysym.grid(column=1, row=3, padx=5, pady=3, sticky=(W))

		self.necessity = BooleanVar()
		necessitybtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Necessity'], variable=self.necessity, onvalue=True)
		necessitybtn.grid(column=0, row=4, padx=5, pady=3, sticky=(W))
		self.necessity.set(False)
		necessitysym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.NECESSITY])
		necessitysym.grid(column=1, row=4, padx=5, pady=3, sticky=(W))

		self.courage = BooleanVar()
		couragebtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Courage'], variable=self.courage, onvalue=True)
		couragebtn.grid(column=0, row=5, padx=5, pady=3, sticky=(W))
		self.courage.set(False)
		couragesym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.COURAGE])
		couragesym.grid(column=1, row=5, padx=5, pady=3, sticky=(W))

		self.nemesis = BooleanVar()
		nemesisbtn = ttk.Checkbutton(lotspanel, text=texts.txtsappearancedlg['Nemesis'], variable=self.nemesis, onvalue=True)
		nemesisbtn.grid(column=0, row=6, padx=5, pady=5, sticky=(W))
		self.nemesis.set(False)
		nemesissym = ttk.Label(lotspanel, font=astroFont, text=common.common.lots[lots.Lots.NEMESIS])
		nemesissym.grid(column=1, row=6, padx=5, pady=5, sticky=(W))

		#Syzygy
		syzygypanel = ttk.LabelFrame(frame, text=texts.txtsappearancedlg['Syzygy'])
		syzygypanel.grid(column=1, row=3, padx=AppearanceDlg.PANELDISTX, pady=AppearanceDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.syzygy = BooleanVar()
		syzygybtn = ttk.Checkbutton(syzygypanel, text=texts.txtsappearancedlg['Syzygy'], variable=self.syzygy, onvalue=True)
		syzygybtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.syzygy.set(True)
		syzygysym = ttk.Label(syzygypanel, font=astroFont, text=common.common.syzygy)
		syzygysym.grid(column=1, row=0, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=4, padx=5, pady=5, sticky=(S,E))

		hellbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def initialize(self, opts):
		if (opts.hellenistic):
			self.chartformat.set('hell')
		else:
			self.chartformat.set('round')
		self.boundsH.set(opts.showbounds)
		self.boundsR.set(opts.showboundsround)
		self.topo.set(opts.topocentric)
		self.show.set(opts.showdata)
		self.cuspspos.set(opts.showcuspspos)
		if (opts.outer == options.Options.NONE):
			self.outer.set('none')
		elif (opts.outer == options.Options.ANTIS):
			self.outer.set('antis')
		elif (opts.outer == options.Options.DODEC):
			self.outer.set('dodec')

		ar = [self.fortune, self.spirit, self.eros, self.victory, self.necessity, self.courage, self.nemesis]
		for i in range(len(opts.lots)):
			ar[i].set(opts.lots[i])

		self.syzygy.set(opts.syzygy)


	def copyData(self):
		self.var_hellenistic = True
		if (self.chartformat.get() == 'round'):
			self.var_hellenistic = False
		self.var_boundsH = self.boundsH.get()
		self.var_boundsR = self.boundsR.get()
		self.var_topo = self.topo.get()
		self.var_show = self.show.get()
		self.var_cuspspos = self.cuspspos.get()

		self.var_outer = options.Options.NONE
		if (self.outer.get() == 'antis'):
			self.var_outer = options.Options.ANTIS
		elif (self.outer.get() == 'dodec'):
			self.var_outer = options.Options.DODEC

		self.var_lots = []
		ar = [self.fortune, self.spirit, self.eros, self.victory, self.necessity, self.courage, self.nemesis]
		for i in range(len(ar)):
			self.var_lots.append(ar[i].get())

		self.var_syzygy = self.syzygy.get()


	def check(self, opts):
		changed = False
		
		if (opts.hellenistic != self.var_hellenistic):
			opts.hellenistic = self.var_hellenistic
			changed = True

		if (opts.showbounds != self.var_boundsH):
			opts.showbounds = self.var_boundsH
			changed = True

		if (opts.showboundsround != self.var_boundsR):
			opts.showboundsround = self.var_boundsR
			changed = True

		if (opts.topocentric != self.var_topo):
			opts.topocentric = self.var_topo
			changed = True

		if (opts.showdata != self.var_show):
			opts.showdata = self.var_show
			changed = True

		if (opts.showcuspspos != self.var_cuspspos):
			opts.showcuspspos = self.var_cuspspos
			changed = True

		if (opts.outer != self.var_outer):
			opts.outer = self.var_outer
			changed = True

		for i in range(len(opts.lots)):
			if (opts.lots[i] != self.var_lots[i]):
				opts.lots[i] = self.var_lots[i]
				changed = True

		if (opts.syzygy != self.var_syzygy):
			opts.syzygy = self.var_syzygy
			changed = True

		return changed


	def ok(self, event=None):
		self.allright = True
		self.copyData()

		self.destroy()


	def doModal(self):
		self.win.focus_set()
		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def cancel(self):
		self.allright = False
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





