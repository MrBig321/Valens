from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import queue
import planets
import findtime
import util
import texts


class AbortFindTime:
	def __init__(self):
		self.abort = False

	def aborting(self):
		self.abort = True

	def clearAborting(self):
		self.abort = False

	def isAborting(self):
		return self.abort


class FindTimeDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent, opts):
		self.parent = parent
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtscommon['Transits'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		self.abort = AbortFindTime()
		self.theend = False

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#BC panel
		bcpanel = ttk.LabelFrame(frame, text='')
		bcpanel.grid(column=0, row=0, padx=FindTimeDlg.PANELDISTX, pady=FindTimeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.bc = BooleanVar()
		self.bc.set(False)
		bcbtn = ttk.Checkbutton(bcpanel, text=texts.txtsfindtimedlg['BC'], variable=self.bc, onvalue=True)
		bcbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		#planets panel
			#Saturn
		plspanel = ttk.LabelFrame(frame, text='')
		plspanel.grid(column=0, row=1, columnspan=2, rowspan=2, padx=FindTimeDlg.PANELDISTX, pady=FindTimeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.SATURN])
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W,E))
		self.satdeg = StringVar()
		satdegcmd = plspanel.register(self.validateSatDeg)
		satdegentry = ttk.Entry(plspanel, textvariable=self.satdeg, width=4, validate='key', validatecommand=(satdegcmd, '%d'))
		satdegentry.grid(column=1, row=0, padx=5, pady=5, sticky=(W,E))
		self.satdeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=0, padx=5, pady=5, sticky=(W,E))
		self.satmin = StringVar()
		satmincmd = plspanel.register(self.validateSatMin)
		self.satminentry = ttk.Entry(plspanel, textvariable=self.satmin, width=3, validate='key', validatecommand=(satmincmd, '%d'))
		self.satminentry.grid(column=3, row=0, padx=5, pady=5, sticky=(W,E))
		self.satmin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=0, padx=5, pady=5, sticky=(W,E))
		self.satsec = StringVar()
		satseccmd = plspanel.register(self.validateSatSec)
		self.satsecentry = ttk.Entry(plspanel, textvariable=self.satsec, width=3, validate='key', validatecommand=(satseccmd, '%d'))
		self.satsecentry.grid(column=5, row=0, padx=5, pady=5, sticky=(W,E))
		self.satsec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=0, padx=5, pady=5, sticky=(W,E))
		self.sat = BooleanVar()
		self.sat.set(False)
		self.satbtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.sat, onvalue=True)
		self.satbtn.grid(column=7, row=0, padx=5, pady=5, sticky=(W))
			#Jupiter
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.JUPITER])
		label.grid(column=0, row=1, padx=5, pady=5, sticky=(W,E))
		self.jupdeg = StringVar()
		jupdegcmd = plspanel.register(self.validateJupDeg)
		jupdegentry = ttk.Entry(plspanel, textvariable=self.jupdeg, width=4, validate='key', validatecommand=(jupdegcmd, '%d'))
		jupdegentry.grid(column=1, row=1, padx=5, pady=5, sticky=(W,E))
		self.jupdeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=1, padx=5, pady=5, sticky=(W,E))
		self.jupmin = StringVar()
		jupmincmd = plspanel.register(self.validateJupMin)
		self.jupminentry = ttk.Entry(plspanel, textvariable=self.jupmin, width=3, validate='key', validatecommand=(jupmincmd, '%d'))
		self.jupminentry.grid(column=3, row=1, padx=5, pady=5, sticky=(W,E))
		self.jupmin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=1, padx=5, pady=5, sticky=(W,E))
		self.jupsec = StringVar()
		jupseccmd = plspanel.register(self.validateJupSec)
		self.jupsecentry = ttk.Entry(plspanel, textvariable=self.jupsec, width=3, validate='key', validatecommand=(jupseccmd, '%d'))
		self.jupsecentry.grid(column=5, row=1, padx=5, pady=5, sticky=(W,E))
		self.jupsec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=1, padx=5, pady=5, sticky=(W,E))
		self.jup = BooleanVar()
		self.jup.set(False)
		self.jupbtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.jup, onvalue=True)
		self.jupbtn.grid(column=7, row=1, padx=5, pady=5, sticky=(W))
			#Mars
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.MARS])
		label.grid(column=0, row=2, padx=5, pady=5, sticky=(W,E))
		self.mardeg = StringVar()
		mardegcmd = plspanel.register(self.validateMarDeg)
		mardegentry = ttk.Entry(plspanel, textvariable=self.mardeg, width=4, validate='key', validatecommand=(mardegcmd, '%d'))
		mardegentry.grid(column=1, row=2, padx=5, pady=5, sticky=(W,E))
		self.mardeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=2, padx=5, pady=5, sticky=(W,E))
		self.marmin = StringVar()
		marmincmd = plspanel.register(self.validateMarMin)
		self.marminentry = ttk.Entry(plspanel, textvariable=self.marmin, width=3, validate='key', validatecommand=(marmincmd, '%d'))
		self.marminentry.grid(column=3, row=2, padx=5, pady=5, sticky=(W,E))
		self.marmin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=2, padx=5, pady=5, sticky=(W,E))
		self.marsec = StringVar()
		marseccmd = plspanel.register(self.validateMarSec)
		self.marsecentry = ttk.Entry(plspanel, textvariable=self.marsec, width=3, validate='key', validatecommand=(marseccmd, '%d'))
		self.marsecentry.grid(column=5, row=2, padx=5, pady=5, sticky=(W,E))
		self.marsec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=2, padx=5, pady=5, sticky=(W,E))
		self.mar = BooleanVar()
		self.mar.set(False)
		self.marbtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.mar, onvalue=True)
		self.marbtn.grid(column=7, row=2, padx=5, pady=5, sticky=(W))
			#Sun
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.SUN])
		label.grid(column=0, row=3, padx=5, pady=5, sticky=(W,E))
		self.sundeg = StringVar()
		sundegcmd = plspanel.register(self.validateSunDeg)
		sundegentry = ttk.Entry(plspanel, textvariable=self.sundeg, width=4, validate='key', validatecommand=(sundegcmd, '%d'))
		sundegentry.grid(column=1, row=3, padx=5, pady=5, sticky=(W,E))
		self.sundeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=3, padx=5, pady=5, sticky=(W,E))
		self.sunmin = StringVar()
		sunmincmd = plspanel.register(self.validateSunMin)
		self.sunminentry = ttk.Entry(plspanel, textvariable=self.sunmin, width=3, validate='key', validatecommand=(sunmincmd, '%d'))
		self.sunminentry.grid(column=3, row=3, padx=5, pady=5, sticky=(W,E))
		self.sunmin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=3, padx=5, pady=5, sticky=(W,E))
		self.sunsec = StringVar()
		sunseccmd = plspanel.register(self.validateSunSec)
		self.sunsecentry = ttk.Entry(plspanel, textvariable=self.sunsec, width=3, validate='key', validatecommand=(sunseccmd, '%d'))
		self.sunsecentry.grid(column=5, row=3, padx=5, pady=5, sticky=(W,E))
		self.sunsec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=3, padx=5, pady=5, sticky=(W,E))
#		self.sun = BooleanVar()
#		self.sun.set(False)
#		sunbtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.sun, onvalue=True)
#		sunbtn.grid(column=7, row=3, padx=5, pady=5, sticky=(W))
			#Venus
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.VENUS])
		label.grid(column=0, row=4, padx=5, pady=5, sticky=(W,E))
		self.vendeg = StringVar()
		vendegcmd = plspanel.register(self.validateVenDeg)
		vendegentry = ttk.Entry(plspanel, textvariable=self.vendeg, width=4, validate='key', validatecommand=(vendegcmd, '%d'))
		vendegentry.grid(column=1, row=4, padx=5, pady=5, sticky=(W,E))
		self.vendeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=4, padx=5, pady=5, sticky=(W,E))
		self.venmin = StringVar()
		venmincmd = plspanel.register(self.validateVenMin)
		self.venminentry = ttk.Entry(plspanel, textvariable=self.venmin, width=3, validate='key', validatecommand=(venmincmd, '%d'))
		self.venminentry.grid(column=3, row=4, padx=5, pady=5, sticky=(W,E))
		self.venmin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=4, padx=5, pady=5, sticky=(W,E))
		self.vensec = StringVar()
		venseccmd = plspanel.register(self.validateVenSec)
		self.vensecentry = ttk.Entry(plspanel, textvariable=self.vensec, width=3, validate='key', validatecommand=(venseccmd, '%d'))
		self.vensecentry.grid(column=5, row=4, padx=5, pady=5, sticky=(W,E))
		self.vensec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=4, padx=5, pady=5, sticky=(W,E))
		self.ven = BooleanVar()
		self.ven.set(False)
		self.venbtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.ven, onvalue=True)
		self.venbtn.grid(column=7, row=4, padx=5, pady=5, sticky=(W))
			#Mercury
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.MERCURY])
		label.grid(column=0, row=5, padx=5, pady=5, sticky=(W,E))
		self.merdeg = StringVar()
		merdegcmd = plspanel.register(self.validateMerDeg)
		merdegentry = ttk.Entry(plspanel, textvariable=self.merdeg, width=4, validate='key', validatecommand=(merdegcmd, '%d'))
		merdegentry.grid(column=1, row=5, padx=5, pady=5, sticky=(W,E))
		self.merdeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=5, padx=5, pady=5, sticky=(W,E))
		self.mermin = StringVar()
		mermincmd = plspanel.register(self.validateMerMin)
		self.merminentry = ttk.Entry(plspanel, textvariable=self.mermin, width=3, validate='key', validatecommand=(mermincmd, '%d'))
		self.merminentry.grid(column=3, row=5, padx=5, pady=5, sticky=(W,E))
		self.mermin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=5, padx=5, pady=5, sticky=(W,E))
		self.mersec = StringVar()
		merseccmd = plspanel.register(self.validateMerSec)
		self.mersecentry = ttk.Entry(plspanel, textvariable=self.mersec, width=3, validate='key', validatecommand=(merseccmd, '%d'))
		self.mersecentry.grid(column=5, row=5, padx=5, pady=5, sticky=(W,E))
		self.mersec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=5, padx=5, pady=5, sticky=(W,E))
		self.mer = BooleanVar()
		self.mer.set(False)
		self.merbtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.mer, onvalue=True)
		self.merbtn.grid(column=7, row=5, padx=5, pady=5, sticky=(W))
			#Moon
		label = ttk.Label(plspanel, text=texts.planets[planets.Planets.MOON])
		label.grid(column=0, row=6, padx=5, pady=5, sticky=(W,E))
		self.moodeg = StringVar()
		moodegcmd = plspanel.register(self.validateMooDeg)
		moodegentry = ttk.Entry(plspanel, textvariable=self.moodeg, width=4, validate='key', validatecommand=(moodegcmd, '%d'))
		moodegentry.grid(column=1, row=6, padx=5, pady=5, sticky=(W,E))
		self.moodeg.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['D'])
		label.grid(column=2, row=6, padx=5, pady=5, sticky=(W,E))
		self.moomin = StringVar()
		moomincmd = plspanel.register(self.validateMooMin)
		self.moominentry = ttk.Entry(plspanel, textvariable=self.moomin, width=3, validate='key', validatecommand=(moomincmd, '%d'))
		self.moominentry.grid(column=3, row=6, padx=5, pady=5, sticky=(W,E))
		self.moomin.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['M'])
		label.grid(column=4, row=6, padx=5, pady=5, sticky=(W,E))
		self.moosec = StringVar()
		mooseccmd = plspanel.register(self.validateMooSec)
		self.moosecentry = ttk.Entry(plspanel, textvariable=self.moosec, width=3, validate='key', validatecommand=(mooseccmd, '%d'))
		self.moosecentry.grid(column=5, row=6, padx=5, pady=5, sticky=(W,E))
		self.moosec.set('0')
		label = ttk.Label(plspanel, text=texts.txtsfindtimedlg['S'])
		label.grid(column=6, row=6, padx=5, pady=5, sticky=(W,E))
#		self.moo = BooleanVar()
#		self.moo.set(False)
#		moobtn = ttk.Checkbutton(plspanel, text=texts.txtsfindtimedlg['R'], variable=self.moo, onvalue=True)
#		moobtn.grid(column=7, row=6, padx=5, pady=5, sticky=(W))
		#Use panel
		usepanel = ttk.LabelFrame(frame, text=texts.txtsfindtimedlg['Use'])
		usepanel.grid(column=1, row=0, padx=FindTimeDlg.PANELDISTX, pady=FindTimeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.minute = BooleanVar()
		self.minute.set(True)
		self.minutebtn = ttk.Checkbutton(usepanel, text=texts.txtsfindtimedlg['Minute'], variable=self.minute, onvalue=True, command=self.onUseMin)
		self.minutebtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.second = BooleanVar()
		self.second.set(True)
		self.secondbtn = ttk.Checkbutton(usepanel, text=texts.txtsfindtimedlg['Second'], variable=self.second, onvalue=True, command=self.onUseSec)
		self.secondbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.retrograde = BooleanVar()
		self.retrograde.set(True)
		self.retrogradebtn = ttk.Checkbutton(usepanel, text=texts.txtsfindtimedlg['Retrograde'], variable=self.retrograde, onvalue=True, command=self.onUseRetr)
		self.retrogradebtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		#Approximation
		approxpanel = ttk.LabelFrame(frame, text=texts.txtsfindtimedlg['Approx'])
		approxpanel.grid(column=2, row=0, padx=FindTimeDlg.PANELDISTX, pady=FindTimeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.approx = BooleanVar()
		self.approx.set(False)
		approxbtn = ttk.Checkbutton(approxpanel, text=texts.txtsfindtimedlg['Use'], variable=self.approx, onvalue=True, command=self.onApprox)
		approxbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.approxdeg = StringVar()
		approxdegcmd = approxpanel.register(self.validateApproxDeg)
		self.approxdegentry = ttk.Entry(approxpanel, textvariable=self.approxdeg, width=4, validate='key', validatecommand=(approxdegcmd, '%d'))
		self.approxdegentry.grid(column=1, row=0, padx=5, pady=5, sticky=(W,E))
		self.approxdeg.set('0')
		self.approxdeglabel = ttk.Label(approxpanel, text=texts.txtsfindtimedlg['D'])
		self.approxdeglabel.grid(column=2, row=0, padx=5, pady=5, sticky=(W,E))
		self.approxmin = StringVar()
		approxmincmd = approxpanel.register(self.validateApproxMin)
		self.approxminentry = ttk.Entry(approxpanel, textvariable=self.approxmin, width=3, validate='key', validatecommand=(approxmincmd, '%d'))
		self.approxminentry.grid(column=3, row=0, padx=5, pady=5, sticky=(W,E))
		self.approxmin.set('0')
		self.approxminlabel = ttk.Label(approxpanel, text=texts.txtsfindtimedlg['M'])
		self.approxminlabel.grid(column=4, row=0, padx=5, pady=5, sticky=(W,E))
		self.approxsec = StringVar()
		approxseccmd = approxpanel.register(self.validateApproxSec)
		self.approxsecentry = ttk.Entry(approxpanel, textvariable=self.approxsec, width=3, validate='key', validatecommand=(approxseccmd, '%d'))
		self.approxsecentry.grid(column=5, row=0, padx=5, pady=5, sticky=(W,E))
		self.approxsec.set('0')
		self.approxseclabel = ttk.Label(approxpanel, text=texts.txtsfindtimedlg['S'])
		self.approxseclabel.grid(column=6, row=0, padx=5, pady=5, sticky=(W,E))
		self.enableApprox('disabled')

		#List
		bkg_rgb = util.getRGBTxt((255, 255, 255))
		listpanel = ttk.LabelFrame(frame, text='')
		listpanel.grid(column=2, row=1, padx=FindTimeDlg.PANELDISTX, pady=FindTimeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.tree = ttk.Treeview(listpanel, columns=('date', 'time'), selectmode='none', height=5)
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)

#		self.tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		self.tree.column('#0', width=50, anchor='center')
		self.tree.column('date', width=120, anchor='center')
		self.tree.column('time', width=120, anchor='center')

		ysb = ttk.Scrollbar(listpanel, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(listpanel, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	self.tree.heading('#0', text='Planets')
		self.tree.heading('date', text=texts.txtsfindtimedlg['Date'])
		self.tree.heading('time', text=texts.txtsfindtimedlg['Time'])

		self.iids = []

		self.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Start-button
		startpanel = ttk.LabelFrame(frame, text='')
		startpanel.grid(column=2, row=2, padx=FindTimeDlg.PANELDISTX, pady=FindTimeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.startbtn = ttk.Button(startpanel, width=10, text=texts.txtsfindtimedlg['Start'], command=self.onStartBtn)
		self.startbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W,E))
		self.stopbtn = ttk.Button(startpanel, width=10, text=texts.txtsfindtimedlg['Stop'], command=self.onStopBtn)
		self.stopbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W,E))

		self.stopbtn.configure(state='disabled')

		#progbar
		self.progbar = ttk.Progressbar(startpanel, mode='indeterminate', orient='horizontal', length=100)#, maximum=6000)
#		self.progbar['value'] = 0
		self.progbar.grid(column=0, row=1, columnspan=2, padx=5, pady=5, sticky=(W,E))

		self.prtext = ttk.Label(startpanel, text=texts.txtsfindtimedlg['Year']+': '+'0')
		self.prtext.grid(column=2, row=1, padx=5, pady=5, sticky=(W,E))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=2, row=3, padx=5, pady=5, sticky=(S,E))

		satdegentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onStopBtn(self, event=None):
		self.abort.aborting()
		self.progbar.stop()
		self.startbtn.configure(state='normal')
		self.stopbtn.configure(state='disabled')


	def onStartBtn(self, event=None):
		if (not self.validate()):
			return

		self.prtext['text'] = texts.txtsfindtimedlg['Year']+': '+'0'
		self.startbtn.configure(state='disabled')
		self.stopbtn.configure(state='normal')
		self.abort.clearAborting()

		#clear-list
		num = len(self.iids) 
		if (num != 0):
			for i in range(num):
				self.tree.delete(self.iids[i])
			del self.iids[:]

		bc = self.bc.get()

		saturnlon = float(self.satdeg.get())
		if (self.minute.get()):
			saturnlon += float(self.satmin.get())/60.0
		if (self.second.get()):
			saturnlon += float(self.satsec.get())/3600.0
		saturnretr = self.sat.get()

		jupiterlon = float(self.jupdeg.get())
		if (self.minute.get()):
			jupiterlon += float(self.jupmin.get())/60.0
		if (self.second.get()):
			jupiterlon += float(self.jupsec.get())/3600.0
		jupiterretr = self.jup.get()

		marslon = float(self.mardeg.get())
		if (self.minute.get()):
			marslon += float(self.marmin.get())/60.0
		if (self.second.get()):
			marslon += float(self.marsec.get())/3600.0
		marsretr = self.mar.get()

		sunlon = float(self.sundeg.get())
		if (self.minute.get()):
			sunlon += float(self.sunmin.get())/60.0
		if (self.second.get()):
			sunlon += float(self.sunsec.get())/3600.0
		sunretr = False #self.sun.get()

		venuslon = float(self.vendeg.get())
		if (self.minute.get()):
			venuslon += float(self.venmin.get())/60.0
		if (self.second.get()):
			venuslon += float(self.vensec.get())/3600.0
		venusretr = self.ven.get()

		mercurylon = float(self.merdeg.get())
		if (self.minute.get()):
			mercurylon += float(self.mermin.get())/60.0
		if (self.second.get()):
			mercurylon += float(self.mersec.get())/3600.0
		mercuryretr = self.mer.get()

		moonlon = float(self.moodeg.get())
		if (self.minute.get()):
			moonlon += float(self.moomin.get())/60.0
		if (self.second.get()):
			moonlon += float(self.moosec.get())/3600.0
		moonretr = False #self.moo.get()

		useapprox = self.approx.get()
		approxdeg = float(self.approxdeg.get())
		approxmin = float(self.approxmin.get())
		approxsec = float(self.approxsec.get())

		ftdata = ((saturnlon, saturnretr), (jupiterlon, jupiterretr), (marslon, marsretr), (sunlon, sunretr), (venuslon, venusretr) ,(mercurylon, mercuryretr), (moonlon, moonretr))

		usemin = self.minute.get()
		usesec = self.second.get()
		useretr = self.retrograde.get()
		ftdatause = (usemin, usesec, useretr)

		ftdataapprox = (useapprox, approxdeg, approxmin, approxsec)

		self.progbar.start()

		self.queue = queue.Queue()
		self.queueyear = queue.Queue()
		threadId = findtime.FindTime(bc, ftdata, ftdatause, ftdataapprox, self.abort, self.queue, self.queueyear).start()
		self.parent.after(1000, self.processQueues)

		self.queue.join()			# wait for taskdone
		self.queueyear.join()


	def processQueues(self):
#		print('processQueues')
		try:
			msg=self.queue.get(0)
			self.queue.task_done()
			num = len(self.iids)+1
			datetxt = str(msg[0])+'.'+str(msg[1])+'.'+str(msg[2])
			h,m,s = util.decToDeg(msg[3])
			timetxt = str(h)+':'+str(m).zfill(2)+':'+str(s).zfill(2)
			self.iids.append(self.tree.insert('', 'end', text=str(num), values=(datetxt, timetxt)))
		except queue.Empty:
			pass
		try:
			msgyear=self.queueyear.get(0)
			self.queueyear.task_done()
			self.prtext['text'] = texts.txtsfindtimedlg['Year']+': '+str(msgyear)
#			self.progbar['value'] = msgyear
#			print(msgyear)
			if (not self.abort.isAborting()):
				self.parent.after(300, self.processQueues)
			else:

				if (not self.theend):
					self.progbar.stop()
					self.startbtn.configure(state='normal')
					self.stopbtn.configure(state='disabled')
		except queue.Empty:
			if (not self.abort.isAborting()):
				self.parent.after(300, self.processQueues)
			else:
				if (not self.theend):
					self.progbar.stop()
					self.startbtn.configure(state='normal')
					self.stopbtn.configure(state='disabled')


	def onApprox(self, event=None):
		if (self.approx.get()):
			self.enableApprox('normal')
		else:
			self.enableApprox('disabled')


	def onUseMin(self, event=None):
		if (self.minute.get()):
			self.secondbtn.configure(state='normal')
			self.enableMins('normal')
		else:
			self.second.set(False)
			self.secondbtn.configure(state='disabled')
			self.enableMins('disabled')
			self.enableSecs('disabled')


	def onUseSec(self, event=None):
		if (self.second.get()):
			self.enableSecs('normal')
		else:
			self.enableSecs('disabled')


	def onUseRetr(self, event=None):
		if (self.retrograde.get()):
			self.enableRetrs('normal')
		else:
			self.enableRetrs('disabled')


	def enableMins(self, val):
		self.satminentry.configure(state=val)
		self.jupminentry.configure(state=val)
		self.marminentry.configure(state=val)
		self.sunminentry.configure(state=val)
		self.venminentry.configure(state=val)
		self.merminentry.configure(state=val)
		self.moominentry.configure(state=val)


	def enableSecs(self, val):
		self.satsecentry.configure(state=val)
		self.jupsecentry.configure(state=val)
		self.marsecentry.configure(state=val)
		self.sunsecentry.configure(state=val)
		self.vensecentry.configure(state=val)
		self.mersecentry.configure(state=val)
		self.moosecentry.configure(state=val)


	def enableRetrs(self, val):
		self.satbtn.configure(state=val)
		self.jupbtn.configure(state=val)
		self.marbtn.configure(state=val)
		self.venbtn.configure(state=val)
		self.merbtn.configure(state=val)


	def enableApprox(self, val):
		self.approxdegentry.configure(state=val)
		self.approxdeglabel.configure(state=val)
		self.approxminentry.configure(state=val)
		self.approxminlabel.configure(state=val)
		self.approxsecentry.configure(state=val)
		self.approxseclabel.configure(state=val)


	def validateSatDeg(self, why):
		n = self.satdeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateSatMin(self, why):
		n = self.satmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSatSec(self, why):
		n = self.satsec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateJupDeg(self, why):
		n = self.jupdeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateJupMin(self, why):
		n = self.jupmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateJupSec(self, why):
		n = self.jupsec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMarDeg(self, why):
		n = self.mardeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateMarMin(self, why):
		n = self.marmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMarSec(self, why):
		n = self.marsec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSunDeg(self, why):
		n = self.sundeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateSunMin(self, why):
		n = self.sunmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSunSec(self, why):
		n = self.sunsec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateVenDeg(self, why):
		n = self.vendeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateVenMin(self, why):
		n = self.venmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateVenSec(self, why):
		n = self.vensec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMerDeg(self, why):
		n = self.merdeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateMerMin(self, why):
		n = self.mermin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMerSec(self, why):
		n = self.mersec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMooDeg(self, why):
		n = self.moodeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateMooMin(self, why):
		n = self.moomin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMooSec(self, why):
		n = self.moosec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateApproxDeg(self, why):
		n = self.approxdeg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateApproxMin(self, why):
		n = self.approxmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateApproxSec(self, why):
		n = self.approxsec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validate(self):
		satdeg = self.satdeg.get()
		satmin = self.satmin.get()
		satsec = self.satsec.get()

		jupdeg = self.jupdeg.get()
		jupmin = self.jupmin.get()
		jupsec = self.jupsec.get()

		mardeg = self.mardeg.get()
		marmin = self.marmin.get()
		marsec = self.marsec.get()

		sundeg = self.sundeg.get()
		sunmin = self.sunmin.get()
		sunsec = self.sunsec.get()

		vendeg = self.vendeg.get()
		venmin = self.venmin.get()
		vensec = self.vensec.get()

		merdeg = self.merdeg.get()
		mermin = self.mermin.get()
		mersec = self.mersec.get()

		moodeg = self.moodeg.get()
		moomin = self.moomin.get()
		moosec = self.moosec.get()

		approxdeg = self.approxdeg.get()
		approxmin = self.approxmin.get()
		approxsec = self.approxsec.get()

		if (satdeg=='' or satmin=='' or satsec=='' or jupdeg=='' or jupmin=='' or jupsec=='' or mardeg=='' or marmin=='' or marsec=='' or sundeg=='' or sunmin=='' or sunsec=='' or vendeg=='' or venmin=='' or vensec=='' or merdeg=='' or mermin=='' or mersec=='' or moodeg=='' or moomin=='' or moosec=='' or approxdeg=='' or approxmin=='' or approxsec==''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(satdeg)
			int(satmin)
			int(satsec)
			int(jupdeg)
			int(jupmin)
			int(jupsec)
			int(mardeg)
			int(marmin)
			int(marsec)
			int(sundeg)
			int(sunmin)
			int(sunsec)
			int(vendeg)
			int(venmin)
			int(vensec)
			int(merdeg)
			int(mermin)
			int(mersec)
			int(moodeg)
			int(moomin)
			int(moosec)
			int(approxdeg)
			int(approxmin)
			int(approxsec)
		except ValueError:
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumericFieldsDigits'])
			return False

		return True


	def ok(self, event=None):
		self.theend = True
		self.abort.aborting()
		val = self.validate()
		if (not val):
			self.allright = False
			return False
		else:
			self.allright = True

		self.destroy()


	def doModal(self):
		self.win.focus_set()
		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def cancel(self):
		self.theend = True
		self.abort.aborting()
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




