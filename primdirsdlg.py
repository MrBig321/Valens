from tkinter import *
from tkinter import ttk
#from tkinter import messagebox
import chart
import planets
import primdirs
import userdlg
import texts


class PrimDirsDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	DEG = 0
	MIN = 1
	SEC = 2

	arsz = ('neither', 'promissor', 'significator', 'both')

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsprimdirsdlg['PrimaryDirs'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		self.puserlon = [0, 0, 0]
		self.puserlat = [0, 0, 0]
		self.pusersouthern = False
		self.suserlon = [0, 0, 0]
		self.suserlat = [0, 0, 0]
		self.susersouthern = False

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#UseLatitude panel
		usepanel = ttk.LabelFrame(frame, text=texts.txtsprimdirsdlg['UseSZ'])
		usepanel.grid(column=0, row=0, padx=PrimDirsDlg.PANELDISTX, pady=PrimDirsDlg.PANELDISTY, sticky=(W,N,S,E))
		self.usesz = StringVar()
		usenbtn = ttk.Radiobutton(usepanel, text=texts.txtsprimdirsdlg['SZNeither'], variable=self.usesz, command=self.onSZ, value='neither')
		usenbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		usepbtn = ttk.Radiobutton(usepanel, text=texts.txtsprimdirsdlg['SZPromissor'], variable=self.usesz, command=self.onSZ, value='promissor')
		usepbtn.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		usesbtn = ttk.Radiobutton(usepanel, text=texts.txtsprimdirsdlg['SZSignificator'], variable=self.usesz, command=self.onSZ, value='significator')
		usesbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		usebbtn = ttk.Radiobutton(usepanel, text=texts.txtsprimdirsdlg['SZBoth'], variable=self.usesz, command=self.onSZ, value='both')
		usebbtn.grid(column=0, row=3, padx=5, pady=0, sticky=(W))
		self.usesz.set('neither')
		self.usebian = BooleanVar()
		self.usebian.set(False)
		self.usebianbtn = ttk.Checkbutton(usepanel, text=texts.txtsprimdirsdlg['Bianchini'], variable=self.usebian, onvalue=True)
		self.usebianbtn.grid(column=0, row=4, padx=20, pady=5, sticky=(W))

		#Options panel
		optspanel = ttk.LabelFrame(frame, text='')
		optspanel.grid(column=0, row=1, padx=PrimDirsDlg.PANELDISTX, pady=PrimDirsDlg.PANELDISTY, sticky=(W,N,S,E))
		self.pasps2s = BooleanVar()
		self.pasps2s.set(False)
		pasps2sbtn = ttk.Checkbutton(optspanel, text=texts.txtsprimdirsdlg['ZodAspsPromsToSigs1'], variable=self.pasps2s, onvalue=True)
		pasps2sbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		label = ttk.Label(optspanel, text=texts.txtsprimdirsdlg['ZodAspsPromsToSigs2'])
		label.grid(column=0, row=1, padx=20, pady=0, sticky=(W))
		self.p2aspss = BooleanVar()
		self.p2aspss.set(False)
		p2aspssbtn = ttk.Checkbutton(optspanel, text=texts.txtsprimdirsdlg['ZodPromsToSigAsps1'], variable=self.p2aspss, onvalue=True)
		p2aspssbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		label = ttk.Label(optspanel, text=texts.txtsprimdirsdlg['ZodPromsToSigAsps2'])
		label.grid(column=0, row=3, padx=20, pady=0, sticky=(W))
		self.ascmcpr = BooleanVar()
		self.ascmcpr.set(False)
		ascmcprbtn = ttk.Checkbutton(optspanel, text=texts.txtsprimdirsdlg['ZodAscMCHCsAsProms'], variable=self.ascmcpr, onvalue=True)
		ascmcprbtn.grid(column=0, row=4, padx=5, pady=5, sticky=(W))

		#Planets panel
		plspanel = ttk.LabelFrame(frame, text='')
		plspanel.grid(column=1, row=0, rowspan=2, padx=PrimDirsDlg.PANELDISTX, pady=PrimDirsDlg.PANELDISTY, sticky=(W,N,S,E))
			#Promissors
		label = ttk.Label(plspanel, text=texts.txtsprimdirsdlg['Promissors'])
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.psat = BooleanVar()
		self.psat.set(False)
		psatbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.SATURN], variable=self.psat, onvalue=True)
		psatbtn.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.pjup = BooleanVar()
		self.pjup.set(False)
		pjupbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.JUPITER], variable=self.pjup, onvalue=True)
		pjupbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.pmar = BooleanVar()
		self.pmar.set(False)
		pmarbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.MARS], variable=self.pmar, onvalue=True)
		pmarbtn.grid(column=0, row=3, padx=5, pady=0, sticky=(W))
		self.psun = BooleanVar()
		self.psun.set(False)
		psunbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.SUN], variable=self.psun, onvalue=True)
		psunbtn.grid(column=0, row=4, padx=5, pady=5, sticky=(W))
		self.pven = BooleanVar()
		self.pven.set(False)
		pvenbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.VENUS], variable=self.pven, onvalue=True)
		pvenbtn.grid(column=0, row=5, padx=5, pady=0, sticky=(W))
		self.pmer = BooleanVar()
		self.pmer.set(False)
		pmerbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.MERCURY], variable=self.pmer, onvalue=True)
		pmerbtn.grid(column=0, row=6, padx=5, pady=5, sticky=(W))
		self.pmoo = BooleanVar()
		self.pmoo.set(False)
		pmoobtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.MOON], variable=self.pmoo, command=self.onPMoon, onvalue=True)
		pmoobtn.grid(column=0, row=7, padx=5, pady=0, sticky=(W))
		self.psecm = BooleanVar()
		self.psecm.set(False)
		self.psecmbtn = ttk.Checkbutton(plspanel, text=texts.txtsprimdirsdlg['SecondaryMotion'], variable=self.psecm, command=self.onPSecM, onvalue=True)
		self.psecmbtn.grid(column=0, row=8, columnspan=2, padx=20, pady=5, sticky=(W))
		self.psecmtyp = StringVar()
		self.psecmcombo = ttk.Combobox(plspanel, textvariable=self.psecmtyp, width=9, state='readonly', values=texts.smiterList)
		self.psecmcombo.grid(column=0, row=9, columnspan=2, padx=20, pady=0, sticky=(W))
		self.psecmtyp.set(texts.smiterList[0])
		self.psecmcombo.bind('<<ComboboxSelected>>', self.onPSecMSelected)
		self.pnod = BooleanVar()
		self.pnod.set(False)
		pnodbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.ANODE], variable=self.pnod, onvalue=True)
		pnodbtn.grid(column=0, row=10, padx=5, pady=5, sticky=(W))
		self.pbounds = BooleanVar()
		self.pbounds.set(False)
		pboundsbtn = ttk.Checkbutton(plspanel, text=texts.txtsprimdirsdlg['Bounds'], variable=self.pbounds, onvalue=True)
		pboundsbtn.grid(column=0, row=11, padx=5, pady=0, sticky=(W))
		self.puser = BooleanVar()
		self.puser.set(False)
		puserchkbtn = ttk.Checkbutton(plspanel, text='', variable=self.puser, command=self.onPChkUser, onvalue=True)
		puserchkbtn.grid(column=0, row=12, padx=5, pady=5, sticky=(W))
		self.puserbtn = ttk.Button(plspanel, text=texts.txtsprimdirsdlg['User'], width=5, command=self.onPUser)
		self.puserbtn.grid(column=0, row=12, padx=20, pady=0)
			#Aspects
		self.conj = BooleanVar()
		self.conj.set(False)
		conjbtn = ttk.Checkbutton(plspanel, text=texts.aspects[chart.Chart.CONIUNCTIO], variable=self.conj, onvalue=True)
		conjbtn.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		self.sext = BooleanVar()
		self.sext.set(False)
		sextbtn = ttk.Checkbutton(plspanel, text=texts.aspects[chart.Chart.SEXTIL], variable=self.sext, onvalue=True)
		sextbtn.grid(column=1, row=2, padx=5, pady=0, sticky=(W))
		self.quad = BooleanVar()
		self.quad.set(False)
		quadbtn = ttk.Checkbutton(plspanel, text=texts.aspects[chart.Chart.QUADRAT], variable=self.quad, onvalue=True)
		quadbtn.grid(column=1, row=3, padx=5, pady=5, sticky=(W))
		self.trig = BooleanVar()
		self.trig.set(False)
		trigbtn = ttk.Checkbutton(plspanel, text=texts.aspects[chart.Chart.TRIGON], variable=self.trig, onvalue=True)
		trigbtn.grid(column=1, row=4, padx=5, pady=0, sticky=(W))
		self.oppo = BooleanVar()
		self.oppo.set(False)
		oppobtn = ttk.Checkbutton(plspanel, text=texts.aspects[chart.Chart.OPPOSITIO], variable=self.oppo, onvalue=True)
		oppobtn.grid(column=1, row=5, padx=5, pady=5, sticky=(W))
			#Significator
		label = ttk.Label(plspanel, text=texts.txtsprimdirsdlg['Significators'])
		label.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
		self.sasc = BooleanVar()
		self.sasc.set(False)
		sascbtn = ttk.Checkbutton(plspanel, text=texts.ascmc[0], variable=self.sasc, onvalue=True)
		sascbtn.grid(column=2, row=1, padx=5, pady=0, sticky=(W))
		self.smc = BooleanVar()
		self.smc.set(False)
		smcbtn = ttk.Checkbutton(plspanel, text=texts.ascmc[1], variable=self.smc, onvalue=True)
		smcbtn.grid(column=2, row=2, padx=5, pady=5, sticky=(W))
		self.ssat = BooleanVar()
		self.ssat.set(False)
		ssatbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.SATURN], variable=self.ssat, onvalue=True)
		ssatbtn.grid(column=2, row=3, padx=5, pady=0, sticky=(W))
		self.sjup = BooleanVar()
		self.sjup.set(False)
		sjupbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.JUPITER], variable=self.sjup, onvalue=True)
		sjupbtn.grid(column=2, row=4, padx=5, pady=5, sticky=(W))
		self.smar = BooleanVar()
		self.smar.set(False)
		smarbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.MARS], variable=self.smar, onvalue=True)
		smarbtn.grid(column=2, row=5, padx=5, pady=0, sticky=(W))
		self.ssun = BooleanVar()
		self.ssun.set(False)
		ssunbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.SUN], variable=self.ssun, onvalue=True)
		ssunbtn.grid(column=2, row=6, padx=5, pady=5, sticky=(W))
		self.sven = BooleanVar()
		self.sven.set(False)
		svenbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.VENUS], variable=self.sven, onvalue=True)
		svenbtn.grid(column=2, row=7, padx=5, pady=0, sticky=(W))
		self.smer = BooleanVar()
		self.smer.set(False)
		smerbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.MERCURY], variable=self.smer, onvalue=True)
		smerbtn.grid(column=2, row=8, padx=5, pady=5, sticky=(W))
		self.smoo = BooleanVar()
		self.smoo.set(False)
		smoobtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.MOON], variable=self.smoo, onvalue=True)
		smoobtn.grid(column=2, row=9, padx=5, pady=0, sticky=(W))
		self.snod = BooleanVar()
		self.snod.set(False)
		snodbtn = ttk.Checkbutton(plspanel, text=texts.planets[planets.Planets.ANODE], variable=self.snod, onvalue=True)
		snodbtn.grid(column=2, row=10, padx=5, pady=5, sticky=(W))
		self.suser = BooleanVar()
		self.suser.set(False)
		suserchkbtn = ttk.Checkbutton(plspanel, text='', variable=self.suser, command=self.onSChkUser, onvalue=True)
		suserchkbtn.grid(column=2, row=11, padx=5, pady=0, sticky=(W))
		self.suserbtn = ttk.Button(plspanel, text=texts.txtsprimdirsdlg['User'], width=5, command=self.onSUser)
		self.suserbtn.grid(column=2, row=11, padx=20, pady=0)
		#Key panel
		keypanel = ttk.LabelFrame(frame, text=texts.txtsprimdirsdlg['Keys'])
		keypanel.grid(column=2, row=0, padx=PrimDirsDlg.PANELDISTX, pady=PrimDirsDlg.PANELDISTY, sticky=(W,N,S,E))
		self.keydyn = StringVar()
		self.keydyn.set('static')
		keydynbtn = ttk.Radiobutton(keypanel, text=texts.txtsprimdirsdlg['Dynamic'], variable=self.keydyn, command=self.onKeyDyn, value='dynamic')
		keydynbtn.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky=(W))
		keystatbtn = ttk.Radiobutton(keypanel, text=texts.txtsprimdirsdlg['Static'], variable=self.keydyn, command=self.onKeyDyn, value='static')
		keystatbtn.grid(column=0, row=1, columnspan=2, padx=5, pady=0, sticky=(W))
		self.keytyp = StringVar()
		self.keycombo = ttk.Combobox(keypanel, textvariable=self.keytyp, width=20, state='readonly', values=texts.typeListStat)
		self.keycombo.grid(column=0, row=2, columnspan=3, padx=5, pady=10, sticky=(W))
		self.keytyp.set(texts.typeListStat[0])
		self.keycombo.bind('<<ComboboxSelected>>', self.onKeySelected)
		self.deglabel = ttk.Label(keypanel, text=texts.txtsprimdirsdlg['Deg']+':')
		self.deglabel.grid(column=0, row=3, padx=5, pady=0, sticky=(W))
		self.deg = StringVar()
		degcmd = keypanel.register(self.validateDeg)
		self.degentry = ttk.Entry(keypanel, textvariable=self.deg, width=3, validate='key', validatecommand=(degcmd, '%d'))
		self.degentry.grid(column=0, row=4, padx=5, pady=0, sticky=(W))
		self.deg.set('')
		self.minlabel = ttk.Label(keypanel, text=texts.txtsprimdirsdlg['Min']+':')
		self.minlabel.grid(column=1, row=3, padx=5, pady=0, sticky=(W))
		self.min = StringVar()
		mincmd = keypanel.register(self.validateMin)
		self.minentry = ttk.Entry(keypanel, textvariable=self.min, width=3, validate='key', validatecommand=(mincmd, '%d'))
		self.minentry.grid(column=1, row=4, padx=5, pady=0, sticky=(W))
		self.min.set('')
		self.seclabel = ttk.Label(keypanel, text=texts.txtsprimdirsdlg['Sec']+':')
		self.seclabel.grid(column=2, row=3, padx=5, pady=0, sticky=(W))
		self.sec = StringVar()
		seccmd = keypanel.register(self.validateSec)
		self.secentry = ttk.Entry(keypanel, textvariable=self.sec, width=3, validate='key', validatecommand=(seccmd, '%d'))
		self.secentry.grid(column=2, row=4, padx=5, pady=0, sticky=(W))
		self.sec.set('')
		self.coefflabel = ttk.Label(keypanel, text=texts.txtsprimdirsdlg['Coefficient']+':')
		self.coefflabel.grid(column=0, row=5, columnspan=2, padx=5, pady=0, sticky=(W))
		self.coeff = StringVar()
		self.coeffentry = ttk.Entry(keypanel, textvariable=self.coeff, width=10)
		self.coeffentry.grid(column=0, row=6, columnspan=2, padx=5, pady=0, sticky=(W))
		self.coeff.set('')
		self.coeffentry.configure(state='disable')


		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		cancelbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=2, row=1, padx=15, pady=15, sticky=(S,E))

		usenbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onPMoon(self, event=None):
		if (self.pmoo.get()):
			self.psecmbtn.configure(state='normal')
			if (self.psecm.get()):
				self.psecmcombo.configure(state='normal')
			else:
				self.psecmcombo.configure(state='disabled')
		else:
			self.psecmbtn.configure(state='disable')
			self.psecmcombo.configure(state='disable')


	def onPSecM(self, event=None):
		if (self.psecm.get()):
			self.psecmcombo.configure(state='normal')
		else:
			self.psecmcombo.configure(state='disable')


	def onSZ(self, event=None):
		if (self.usesz.get() == 'both'):
			self.usebianbtn.configure(state='normal')
		else:
			self.usebianbtn.configure(state='disabled')


	def onPSecMSelected(self, event=None):
		self.psecmcombo.selection_clear()


	def onKeySelected(self, event=None):
		self.keycombo.selection_clear()

		if (self.keydyn.get() == 'static'):
			self.statsel = texts.typeListStat.index(self.keytyp.get())
			if (self.statsel != primdirs.PrimDirs.USER and self.prevstatsel == 3):
				if (self.deg.get() == ''):
					self.user[PrimDirsDlg.DEG] = 0
				else:
					self.user[PrimDirsDlg.DEG] = int(self.deg.get())

				if (self.minentry.get() == ''):
					self.user[PrimDirsDlg.MIN] = 0
				else:
					self.user[PrimDirsDlg.MIN] = int(self.min.get())

				if (self.secentry.get() == ''):
					self.user[PrimDirsDlg.SEC] = 0
				else:
					self.user[PrimDirsDlg.SEC] = int(self.sec.get())

			user = False
			txt = 'disable'
			if (self.statsel == primdirs.PrimDirs.USER):
				user = True
				txt = 'normal'

			self.degentry.configure(state=txt)
			self.minentry.configure(state=txt)
			self.secentry.configure(state=txt)
			deg = minu = sec = 0
			coeff = 0.0
			if (not user):
				deg = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.SEC]
				coeff = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.COEFF]
			else:
				deg = self.user[PrimDirsDlg.DEG]
				minu = self.user[PrimDirsDlg.MIN]
				sec = self.user[PrimDirsDlg.SEC]
				val = (deg+minu/60.0+sec/3600.0) 
				if (val != 0.0):
					coeff = 1.0/val
				else:
					coeff = 0.0

			self.deg.set(str(deg))
			self.min.set(str(minu))
			self.sec.set(str(sec))
			self.coeff.set(str(coeff))

			self.prevstatsel = self.statsel

		else:
			self.dynsel = texts.typeListDyn.index(self.keytyp.get())
	

	def onPUser(self):
		dlg = userdlg.UserDlg(self.win)
		dlg.initialize(self.puserlon, self.puserlat, self.pusersouthern)
		dlg.doModal()
		if (dlg.allright):
			self.puserlon[PrimDirsDlg.DEG] = dlg.var_deg
			self.puserlon[PrimDirsDlg.MIN] = dlg.var_min
			self.puserlon[PrimDirsDlg.SEC] = dlg.var_sec
			self.puserlat[PrimDirsDlg.DEG] = dlg.var_deg2
			self.puserlat[PrimDirsDlg.MIN] = dlg.var_min2
			self.puserlat[PrimDirsDlg.SEC] = dlg.var_sec2
			self.pusersouthern = dlg.var_southern


	def onPChkUser(self):
		if (self.puser.get()):
			self.puserbtn.configure(state='normal')
		else:
			self.puserbtn.configure(state='disable')


	def onSUser(self):
		dlg = userdlg.UserDlg(self.win)
		dlg.initialize(self.suserlon, self.suserlat, self.susersouthern)
		dlg.doModal()
		if (dlg.allright):
			self.suserlon[PrimDirsDlg.DEG] = dlg.var_deg
			self.suserlon[PrimDirsDlg.MIN] = dlg.var_min
			self.suserlon[PrimDirsDlg.SEC] = dlg.var_sec
			self.suserlat[PrimDirsDlg.DEG] = dlg.var_deg2
			self.suserlat[PrimDirsDlg.MIN] = dlg.var_min2
			self.suserlat[PrimDirsDlg.SEC] = dlg.var_sec2
			self.susersouthern = dlg.var_southern


	def onSChkUser(self):
		if (self.suser.get()):
			self.suserbtn.configure(state='normal')
		else:
			self.suserbtn.configure(state='disable')


	def onKeyDyn(self, event=None):
		if (self.keydyn.get() == 'dynamic'):
			self.keycombo['values']=texts.typeListDyn
			self.keytyp.set(texts.typeListDyn[self.dynsel])

			if (self.statsel == primdirs.PrimDirs.USER):
				if (self.deg.get() == ''):
					self.user[PrimDirsDlg.DEG] = 0
				else:
					self.user[PrimDirsDlg.DEG] = int(self.deg.get())

				if (self.minentry.get() == ''):
					self.user[PrimDirsDlg.MIN] = 0
				else:
					self.user[PrimDirsDlg.MIN] = int(self.min.get())

				if (self.secentry.get() == ''):
					self.user[PrimDirsDlg.SEC] = 0
				else:
					self.user[PrimDirsDlg.SEC] = int(self.sec.get())

			self.degentry.configure(state='disabled')
			self.minentry.configure(state='disabled')
			self.secentry.configure(state='disabled')
			self.deg.set('')
			self.min.set('')
			self.sec.set('')
			self.coeff.set('')
		else:
			self.keycombo['values']=texts.typeListStat
			self.keytyp.set(texts.typeListStat[self.statsel])

			user = False
			txt = 'disable'
			if (self.statsel == primdirs.PrimDirs.USER):
				user = True
				txt = 'normal'

			self.degentry.configure(state=txt)
			self.minentry.configure(state=txt)
			self.secentry.configure(state=txt)
			deg = minu = sec = 0
			coeff = 0.0
			if (not user):
				deg = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.SEC]
				coeff = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.COEFF]
			else:
				deg = self.user[PrimDirsDlg.DEG]
				minu = self.user[PrimDirsDlg.MIN]
				sec = self.user[PrimDirsDlg.SEC]
				val = (deg+minu/60.0+sec/3600.0) 
				if (val != 0.0):
					coeff = 1.0/val
				else:
					coeff = 0.0

			self.deg.set(str(deg))
			self.min.set(str(minu))
			self.sec.set(str(sec))
			self.coeff.set(str(coeff))


	def validateDeg(self, why):
		n = self.deg.get()
		if ((len(n) >= 1) and (int(why) == 1)):
			return False

		return True


	def validateMin(self, why):
		n = self.min.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSec(self, why):
		n = self.sec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def initialize(self, opts):
		self.usesz.set(PrimDirsDlg.arsz[opts.subzodiacal])
		self.usebian.set(opts.bianchini)
		self.onSZ()

		self.pasps2s.set(opts.zodpromsigasps[0])
		self.p2aspss.set(opts.zodpromsigasps[1])
		self.ascmcpr.set(opts.ascmchcsasproms)

		parr = (self.psat, self.pjup, self.pmar, self.psun, self.pven, self.pmer, self.pmoo, self.pnod)
		num = len(parr)
		for i in range(num):
			parr[i].set(opts.promplanets[i])

		self.psecm.set(opts.pdsecmotion)
		self.psecmtyp.set(texts.smiterList[opts.pdsecmotioniter])
		self.pbounds.set(opts.pdbounds)

		self.onPMoon()

		self.puser.set(opts.pduser)
		self.puserlon = opts.pduserlon[:]
		self.puserlat = opts.pduserlat[:]
		self.pusersouthern = opts.pdusersouthern
		self.onPChkUser()

		arr = (self.conj, self.sext, self.quad, self.trig, self.oppo)
		num = len(arr)
		for i in range(num):
			arr[i].set(opts.pdaspects[i])

		self.sasc.set(opts.sigascmc[0])
		self.smc.set(opts.sigascmc[1])

		sarr = (self.ssat, self.sjup, self.smar, self.ssun, self.sven, self.smer, self.smoo, self.snod)
		num = len(sarr)
		for i in range(num):
			sarr[i].set(opts.sigplanets[i])

		self.suser.set(opts.pduser2)
		self.suserlon = opts.pduser2lon[:]
		self.suserlat = opts.pduser2lat[:]
		self.susersouthern = opts.pduser2southern
		self.onSChkUser()

		self.dynsel = opts.pdkeyd
		self.statsel = opts.pdkeys
		self.prevstatsel = 0
		self.user = [opts.pdkeydeg, opts.pdkeymin, opts.pdkeysec]

		if (opts.pdkeydyn):
			self.keydyn.set('dynamic')
			self.keycombo['values']=texts.typeListDyn
			self.keytyp.set(texts.typeListDyn[self.dynsel])

			self.degentry.configure(state='disabled')
			self.minentry.configure(state='disabled')
			self.secentry.configure(state='disabled')
			self.deg.set('')
			self.min.set('')
			self.sec.set('')
			self.coeff.set('')
		else:
			self.keydyn.set('static')
			self.keycombo['values']=texts.typeListStat
			self.keytyp.set(texts.typeListStat[self.statsel])

			user = False
			txt = 'disable'
			if (self.statsel == primdirs.PrimDirs.USER):
				user = True
				txt = 'normal'

			self.degentry.configure(state=txt)
			self.minentry.configure(state=txt)
			self.secentry.configure(state=txt)
			deg = minu = sec = 0
			coeff = 0.0
			if (not user):
				deg = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.SEC]
				coeff = primdirs.PrimDirs.staticData[self.statsel][primdirs.PrimDirs.COEFF]
			else:
				deg = self.user[PrimDirsDlg.DEG]
				minu = self.user[PrimDirsDlg.MIN]
				sec = self.user[PrimDirsDlg.SEC]
				val = (deg+minu/60.0+sec/3600.0) 
				if (val != 0.0):
					coeff = 1.0/val
				else:
					coeff = 0.0

			self.deg.set(str(deg))
			self.min.set(str(minu))
			self.sec.set(str(sec))
			self.coeff.set(str(coeff))


	def check(self, opts):
		changed = False

		if (opts.subzodiacal != PrimDirsDlg.arsz.index(self.usesz.get())):
			opts.subzodiacal = PrimDirsDlg.arsz.index(self.usesz.get())
			changed = True

		if (opts.bianchini != self.usebian.get()):
			opts.bianchini = self.usebian.get()
			changed = True

		if (opts.zodpromsigasps[0] != self.pasps2s.get()):
			opts.zodpromsigasps[0] = self.pasps2s.get()
			changed = True

		if (opts.zodpromsigasps[1] != self.p2aspss.get()):
			opts.zodpromsigasps[1] = self.p2aspss.get()
			changed = True

		if (opts.ascmchcsasproms != self.ascmcpr.get()):
			opts.ascmchcsasproms = self.ascmcpr.get()
			changed = True


		parr = (self.psat, self.pjup, self.pmar, self.psun, self.pven, self.pmer, self.pmoo, self.pnod)
		num = len(parr)
		for i in range(num):
			if (opts.promplanets[i] != parr[i].get()):
				opts.promplanets[i] = parr[i].get()
				changed = True

		if (opts.pdsecmotion != self.psecm.get()):
			opts.pdsecmotion = self.psecm.get()
			changed = True

		if (opts.pdsecmotioniter != texts.smiterList.index(self.psecmtyp.get())):
			opts.pdsecmotioniter = texts.smiterList.index(self.psecmtyp.get())
			changed = True

		if (opts.pdbounds != self.pbounds.get()):
			opts.pdbounds = self.pbounds.get()
			changed = True

		if (opts.pduser != self.puser.get()):
			opts.pduser = self.puser.get()
			changed = True

		for i in range(len(opts.pduserlon)):
			if (opts.pduserlon[i] != self.puserlon[i]):
				opts.pduserlon[i] = self.puserlon[i]
				changed = True

		for i in range(len(opts.pduserlat)):
			if (opts.pduserlat[i] != self.puserlat[i]):
				opts.pduserlat[i] = self.puserlat[i]
				changed = True

		if (opts.pdusersouthern != self.pusersouthern):
			opts.pdusersouthern = self.pusersouthern
			changed = True

		arr = (self.conj, self.sext, self.quad, self.trig, self.oppo)
		num = len(arr)
		for i in range(num):
			if (opts.pdaspects[i] != arr[i].get()):
				opts.pdaspects[i] = arr[i].get()
				changed = True

		if (opts.sigascmc[0] != self.sasc.get()):
			opts.sigascmc[0] = self.sasc.get()
			changed = True

		if (opts.sigascmc[1] != self.smc.get()):
			opts.sigascmc[1] = self.smc.get()
			changed = True

		sarr = (self.ssat, self.sjup, self.smar, self.ssun, self.sven, self.smer, self.smoo, self.snod)
		num = len(sarr)
		for i in range(num):
			if (opts.sigplanets[i] != sarr[i].get()):
				opts.sigplanets[i] = sarr[i].get()
				changed = True

		if (opts.pduser2 != self.suser.get()):
			opts.pduser2 = self.suser.get()
			changed = True

		for i in range(len(opts.pduser2lon)):
			if (opts.pduser2lon[i] != self.suserlon[i]):
				opts.pduser2lon[i] = self.suserlon[i]
				changed = True

		for i in range(len(opts.pduser2lat)):
			if (opts.pduser2lat[i] != self.suserlat[i]):
				opts.pduser2lat[i] = self.suserlat[i]
				changed = True

		if (opts.pduser2southern != self.susersouthern):
			opts.pduser2southern = self.susersouthern
			changed = True

		dyn = False
		if (self.keydyn.get() == 'dynamic'):
			dyn = True
		if (opts.pdkeydyn != dyn):
			opts.pdkeydyn = dyn
			changed = True

		if (opts.pdkeyd != self.dynsel):
			opts.pdkeyd = self.dynsel
			changed = True

		if (opts.pdkeys != self.statsel):
			opts.pdkeys = self.statsel
			changed = True

		if (opts.pdkeydeg != self.user[PrimDirsDlg.DEG]):
			opts.pdkeydeg = self.user[PrimDirsDlg.DEG]
			changed = True

		if (opts.pdkeymin != self.user[PrimDirsDlg.MIN]):
			opts.pdkeymin = self.user[PrimDirsDlg.MIN]
			changed = True

		if (opts.pdkeysec != self.user[PrimDirsDlg.SEC]):
			opts.pdkeysec = self.user[PrimDirsDlg.SEC]
			changed = True

		return changed


	def ok(self, event=None):
		self.allright = True
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




