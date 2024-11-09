from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import rangechecker
import placesdlg
import texts
import util


class DataDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	plusvalues = ('+', '-')

	def __init__(self, parent, opts):

		self.parent = parent
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsdatadlg['Data'])
		self.win.resizable(FALSE, FALSE)

		nb = ttk.Notebook(self.win)

#DataFrame
		frame1 = ttk.Frame(nb)
		frame1.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame1.columnconfigure(1, weight=1) #column 1 will expand

		#Name Panel
		namepanel = ttk.LabelFrame(frame1, text=texts.txtsdatadlg['General'])
		namepanel.grid(column=0, row=0, padx=DataDlg.PANELDISTX, pady=DataDlg.PANELDISTY, sticky=(W, N, S))
		namelabel = ttk.Label(namepanel, text=texts.txtsdatadlg['Name']+':')
		namelabel.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.name = StringVar()
		namecmd = namepanel.register(self.validateName)
		nameentry = ttk.Entry(namepanel, textvariable=self.name, width=22, validate='key', validatecommand=(namecmd, '%d'))	#the width of the widget in chars
		nameentry.grid(column=1, row=0, padx=5, pady=5)
		self.name.set('')
		genderlabel = ttk.Label(namepanel, text=texts.txtsdatadlg['Gender']+':')
		genderlabel.grid(column=0, row=1, padx=5, pady=5)
		self.gender = BooleanVar()
		self.gender.set(True)
		genderbtn = ttk.Checkbutton(namepanel, text=texts.txtsdatadlg['Male'], variable=self.gender, onvalue=True)
		genderbtn.grid(column=1, row=1, padx=5, pady=5, sticky=(W))

		#DateTime Panel
		datepanel = ttk.LabelFrame(frame1, text=texts.txtsdatadlg['DateAndTime'])
		datepanel.grid(column=1, row=0, padx=DataDlg.PANELDISTX, pady=DataDlg.PANELDISTY, sticky=(W,N,E,S))
		self.bc = BooleanVar()
		self.bc.set(False)
		bcbtn = ttk.Checkbutton(datepanel, text=texts.txtsdatadlg['BC'], variable=self.bc, onvalue=True)
		bcbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
			#Year
		yearpanel = ttk.Frame(datepanel)
		yearpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(W))		#This adds to datepanel-grid
		yearlabel = ttk.Label(yearpanel, text=texts.txtsdatadlg['Year']+':')
		yearlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.year = StringVar()
		yearcmd = namepanel.register(self.validateYear)
		yearentry = ttk.Entry(yearpanel, textvariable=self.year, width=5, validate='key', validatecommand=(yearcmd, '%d'))
		yearentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.year.set('')
			#Month
		monthpanel = ttk.Frame(datepanel)
		monthpanel.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		monthlabel = ttk.Label(monthpanel, text=texts.txtsdatadlg['Month']+':')
		monthlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.month = StringVar()
		monthcmd = namepanel.register(self.validateMonth)
		monthentry = ttk.Entry(monthpanel, textvariable=self.month, width=3, validate='key', validatecommand=(monthcmd, '%d'))
		monthentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.month.set('')
			#Day
		daypanel = ttk.Frame(datepanel)
		daypanel.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
		daylabel = ttk.Label(daypanel, text=texts.txtsdatadlg['Day']+':')
		daylabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.day = StringVar()
		daycmd = namepanel.register(self.validateDay)
		dayentry = ttk.Entry(daypanel, textvariable=self.day, width=3, validate='key', validatecommand=(daycmd, '%d'))
		dayentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.day.set('')
			#Hour
		hourpanel = ttk.Frame(datepanel)
		hourpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		hourlabel = ttk.Label(hourpanel, text=texts.txtsdatadlg['Hour']+':')
		hourlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.hour = StringVar()
		hourcmd = namepanel.register(self.validateHour)
		hourentry = ttk.Entry(hourpanel, textvariable=self.hour, width=3, validate='key', validatecommand=(hourcmd, '%d'))
		hourentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.hour.set('')
			#Minute
		minutepanel = ttk.Frame(datepanel)
		minutepanel.grid(column=1, row=2, padx=5, pady=5, sticky=(W))
		minutelabel = ttk.Label(minutepanel, text=texts.txtsdatadlg['Min']+':')
		minutelabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.minute = StringVar()
		minutecmd = namepanel.register(self.validateMinute)
		minuteentry = ttk.Entry(minutepanel, textvariable=self.minute, width=3, validate='key', validatecommand=(minutecmd, '%d'))
		minuteentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.minute.set('')
			#Second
		secondpanel = ttk.Frame(datepanel)
		secondpanel.grid(column=2, row=2, padx=5, pady=5, sticky=(W))
		secondlabel = ttk.Label(secondpanel, text=texts.txtsdatadlg['Sec']+':')
		secondlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.second = StringVar()
		secondcmd = namepanel.register(self.validateSecond)
		secondentry = ttk.Entry(secondpanel, textvariable=self.second, width=3, validate='key', validatecommand=(secondcmd, '%d'))
		secondentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.second.set('')

		#Calendar Panel
		calpanel = ttk.LabelFrame(frame1, text=texts.txtsdatadlg['CalendarAndZone'])
		calpanel.grid(column=1, row=1, padx=DataDlg.PANELDISTX, pady=DataDlg.PANELDISTY, sticky=(W,N,S,E)) 
			#CalCombo
		self.cal = StringVar()
		self.calcombo = ttk.Combobox(calpanel, textvariable=self.cal, width=12, state='readonly', values=texts.calList)
		self.calcombo.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky=(W))
		self.cal.set(texts.calList[0])
		self.calcombo.bind('<<ComboboxSelected>>', self.calSelected)
			#ZoneCombo
		self.zone = StringVar()
		self.zonecombo = ttk.Combobox(calpanel, textvariable=self.zone, width=12, state='readonly', values=texts.zoneList)
		self.zonecombo.grid(column=0, row=1, columnspan=3, padx=5, pady=5, sticky=(W))
		self.zone.set(texts.zoneList[0])
		self.zonecombo.bind('<<ComboboxSelected>>', self.zoneSelected)
			#GMTCombo
		gmtlabel = ttk.Label(calpanel, text=texts.txtsdatadlg['GMT']+':')
		gmtlabel.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.zplus = StringVar()
		self.zpluscombo = ttk.Combobox(calpanel, textvariable=self.zplus, width=3, state='readonly', values=DataDlg.plusvalues)
		self.zpluscombo.grid(column=1, row=2, padx=5, pady=5, sticky=(W))
		self.zplus.set(DataDlg.plusvalues[0])
		self.zpluscombo.bind('<<ComboboxSelected>>', self.zplusSelected)
			#ZoneHour
		zhourpanel = ttk.Frame(calpanel)
		zhourpanel.grid(column=0, row=3, padx=5, pady=5, sticky=(W))
		zhourlabel = ttk.Label(zhourpanel, text=texts.txtsdatadlg['Hour']+':')
		zhourlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.zhour = StringVar()
		zhourcmd = namepanel.register(self.validateZHour)
		zhourentry = ttk.Entry(zhourpanel, textvariable=self.zhour, width=3, validate='key', validatecommand=(zhourcmd, '%d'))
		zhourentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.zhour.set('')
			#ZoneMin
		zminpanel = ttk.Frame(calpanel)
		zminpanel.grid(column=1, row=3, padx=5, pady=5, sticky=(W))
		zminlabel = ttk.Label(zminpanel, text=texts.txtsdatadlg['Min']+':')
		zminlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.zmin = StringVar()
		zmincmd = namepanel.register(self.validateZMin)
		zminentry = ttk.Entry(zminpanel, textvariable=self.zmin, width=3, validate='key', validatecommand=(zmincmd, '%d'))
		zminentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.zmin.set('')
			#DST
		self.dst = BooleanVar()
		self.dst.set(False)
		dstbtn = ttk.Checkbutton(calpanel, text=texts.txtsdatadlg['DST'], variable=self.dst, onvalue=True)
		dstbtn.grid(column=0, row=4, padx=5, pady=5, sticky=(W))

		#Place Panel
		placepanel = ttk.LabelFrame(frame1, text=texts.txtsdatadlg['Place'])
		placepanel.grid(column=0, row=1, padx=DataDlg.PANELDISTX, pady=DataDlg.PANELDISTY, sticky=(W,E))
		longlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Long']+':')
		longlabel.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
			#Deg
		degpanel = ttk.Frame(placepanel)
		degpanel.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		deglabel = ttk.Label(degpanel, text=texts.txtsdatadlg['Deg']+':')
		deglabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.deg = StringVar()
		degcmd = namepanel.register(self.validateDeg)
		degentry = ttk.Entry(degpanel, textvariable=self.deg, width=5, validate='key', validatecommand=(degcmd, '%d'))
		degentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.deg.set('')
			#Min
		arcminpanel = ttk.Frame(placepanel)
		arcminpanel.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
		arcminlabel = ttk.Label(arcminpanel, text=texts.txtsdatadlg['Min']+':')
		arcminlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.arcmin = StringVar()
		arcmincmd = namepanel.register(self.validateArcMin)
		arcminentry = ttk.Entry(arcminpanel, textvariable=self.arcmin, width=5, validate='key', validatecommand=(arcmincmd, '%d'))
		arcminentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.arcmin.set('')
			#LonDir
		longdirpanel = ttk.Frame(placepanel)
		longdirpanel.grid(column=3, row=0, padx=5, pady=5, sticky=(W,N,S))
		self.longdir = StringVar()
		ebtn = ttk.Radiobutton(longdirpanel, text=texts.txtsdatadlg['E'], variable=self.longdir, value='e')
		ebtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		wbtn = ttk.Radiobutton(longdirpanel, text=texts.txtsdatadlg['W'], variable=self.longdir, value='w')
		wbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		self.longdir.set('e')

		latlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Lat']+':')
		latlabel.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
			#Deg
		degpanel2 = ttk.Frame(placepanel)
		degpanel2.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		deglabel2 = ttk.Label(degpanel2, text=texts.txtsdatadlg['Deg']+':')
		deglabel2.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.deg2 = StringVar()
		degcmd2 = namepanel.register(self.validateDeg2)
		degentry2 = ttk.Entry(degpanel2, textvariable=self.deg2, width=5, validate='key', validatecommand=(degcmd2, '%d'))
		degentry2.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.deg2.set('')
			#Min
		arcminpanel2 = ttk.Frame(placepanel)
		arcminpanel2.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
		arcminlabel2 = ttk.Label(arcminpanel2, text=texts.txtsdatadlg['Min']+':')
		arcminlabel2.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.arcmin2 = StringVar()
		arcmincmd2 = namepanel.register(self.validateArcMin2)
		arcminentry2 = ttk.Entry(arcminpanel2, textvariable=self.arcmin2, width=5, validate='key', validatecommand=(arcmincmd2, '%d'))
		arcminentry2.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.arcmin2.set('')
			#LatDir
		latdirpanel = ttk.Frame(placepanel)
		latdirpanel.grid(column=3, row=1, padx=5, pady=5, sticky=(W,N,S))
		self.latdir = StringVar()
		nbtn = ttk.Radiobutton(latdirpanel, text=texts.txtsdatadlg['N'], variable=self.latdir, value='n')
		nbtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		sbtn = ttk.Radiobutton(latdirpanel, text=texts.txtsdatadlg['S'], variable=self.latdir, value='s')
		sbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		self.latdir.set('n')
			#PlaceBtn
		placebtn = ttk.Button(placepanel, text=texts.txtsdatadlg['Place'], command=self.placeBtn)
		placebtn.grid(column=0, row=2, columnspan=3, padx=5, pady=5)
		self.placename = StringVar()
		placenamecmd = namepanel.register(self.validatePlaceName)
		placenameentry = ttk.Entry(placepanel, textvariable=self.placename, width=22, validate='key', validatecommand=(placenamecmd, '%d'))
		placenameentry.grid(column=0, row=3, columnspan=3, padx=5, pady=5)
		self.placename.set('')
			#Altitude
		altlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Altitude']+':')
		altlabel.grid(column=0, row=4, padx=5, pady=5, sticky=(W))
		self.alt = StringVar()
		altcmd = namepanel.register(self.validateAlt)
		altentry = ttk.Entry(placepanel, textvariable=self.alt, width=6, validate='key', validatecommand=(altcmd, '%d'))
		altentry.grid(column=1, row=4, padx=5, pady=5, sticky=(W))
		self.alt.set('')
		mlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Meter'])
		mlabel.grid(column=2, row=4, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame1)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=2, padx=5, pady=5, sticky=(S,E))

#		spinvar = StringVar()
#		spin = Spinbox(frame1, from_=1, to=10, textvariable=spinvar)
#		spin.grid(column=0, row=2, padx=5, pady=5, sticky=(W))

#NotesFrame
		frame2 = ttk.Frame(nb)
		frame2.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		self.txt = Text(frame2, width=62)#, height=20)
		self.txt.grid(column=0, row=0, padx=5, pady=5, sticky=(W,E,N,S))

		okpanel2 = ttk.Frame(frame2)
		okbtn2 = ttk.Button(okpanel2, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn2 = ttk.Button(okpanel2, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn2.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn2.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel2.grid(column=0, row=1, padx=5, pady=5, sticky=(S,E))

#Notebook
		nb.add(frame1, text=texts.txtsdatadlg['Data'])
		nb.add(frame2, text=texts.txtsdatadlg['Notes'])
		nb.enable_traversal()
		nb.pack()

		nameentry.focus()
		self.allright = False
		self.center()


	def validateName(self, why):
		n = self.name.get()
		if ((len(n) >= 20) and (int(why) == 1)):
			return False

		return True


	def validateYear(self, why):
		n = self.year.get()
		if ((len(n) >= 4) and (int(why) == 1)):
			return False

		return True


	def validateMonth(self, why):
		n = self.month.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateDay(self, why):
		n = self.day.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateHour(self, why):
		n = self.hour.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMinute(self, why):
		n = self.minute.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSecond(self, why):
		n = self.second.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateDeg(self, why):
		n = self.deg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateArcMin(self, why):
		n = self.arcmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateDeg2(self, why):
		n = self.deg2.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateArcMin2(self, why):
		n = self.arcmin2.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateAlt(self, why):
		n = self.alt.get()
		if ((len(n) >= 5) and (int(why) == 1)):
			return False

		return True


	def validateZHour(self, why):
		n = self.zhour.get()
		if ((len(n) >= 1) and (int(why) == 1)):
			return False

		return True

	def validateZMin(self, why):
		n = self.zmin.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def placeBtn(self):
		dlg = placesdlg.PlacesDlg(self.win)
		dlg.initialize()
		dlg.doModal()
		if (dlg.allright):
			#copy selected place to fields
			place = dlg.var_placename
			lon = dlg.var_lon
			lat = dlg.var_lat
			zone = dlg.var_zone
			alt = dlg.var_alt

			self.placename.set(place.strip())

			#long
			idx = lon.find('E')#
			if (idx == -1):
				idx = lon.find('W')#
				self.longdir.set('w')
			else:
				self.longdir.set('e')
				
			fr = 0
			if (lon[0] == '0'):
				fr = 1
			self.deg.set(lon[fr:idx])
			idx += 1
			if (lon[idx] == '0'):
				idx += 1
			self.arcmin.set(lon[idx:])
	
			#lat
			idx = lat.find('N')#
			if (idx == -1):
				idx = lat.find('S')#
				self.latdir.set('s')
			else:
				self.latdir.set('n')
				
			fr = 0
			if (lat[0] == '0'):
				fr = 1
			self.deg2.set(lat[fr:idx])
			idx += 1
			if (lat[idx] == '0'):
				idx += 1
			self.arcmin2.set(lat[idx:])

			#zone
			self.zplus.set(zone[0])

			zone = zone[1:]
			idx = zone.find(':')
			self.zhour.set(zone[0:idx])

			idx += 1
			if (zone[idx] == '0'):
				idx += 1
			self.zmin.set(zone[idx:])

			#alt
			self.alt.set(alt)

#		dlg.destroy()



	def validatePlaceName(self, why):
		n = self.placename.get()
		if ((len(n) >= 20) and (int(why) == 1)):
			return False

		return True


	def calSelected(self, event=None):
		self.calcombo.selection_clear()


	def zoneSelected(self, event=None):
		self.zonecombo.selection_clear()


	def zplusSelected(self, event=None):
		self.zpluscombo.selection_clear()


	def validate(self):
		y = self.year.get()
		m = self.month.get()
		d = self.day.get()
		h = self.hour.get()
		mi = self.minute.get()
		s = self.second.get()
		zhour = self.zhour.get()
		zmin = self.zmin.get()
		deg = self.deg.get()
		arcmin = self.arcmin.get()
		deg2 = self.deg2.get()
		arcmin2 = self.arcmin2.get()
		alt = self.alt.get()

		if (y == '' or m == '' or d == '' or h == '' or mi == '' or s == '' or zhour == '' or zmin == '' or deg == '' or arcmin == '' or deg2 == '' or arcmin2 == '' or alt == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(y)
			int(m)
			int(d)
			int(h)
			int(mi)
			int(s)
			int(zhour)
			int(zmin)
			int(deg)
			int(arcmin)
			int(deg2)
			int(arcmin2)		
			int(alt)
		except ValueError:
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumericFieldsDigits'])
			return False

		#Year
		checker = rangechecker.RangeChecker()
		if (int(y) > checker.epherange): #>= !?
			if (checker.isExtended()):
				messagebox.showerror(parent=self.win, message=texts.txtsvalidators['SwissEphem'])
			else:
				messagebox.showerror(parent=self.win, message=texts.txtsvalidators['MoshierEphem'])
			return False

		#Month
		if (int(m) < 1 or int(m) > 12):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpMonth'])
			return False

		#Day
		if (int(d) < 1 or int(d) > 31):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpDay'])
			return False

		#Hour
		if (int(h) > 23):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpHour'])
			return False


		#Min, ZMin
		if (int(mi) > 59 or int(zmin) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpMin'])
			return False

		#Sec
		if (int(s) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpSec'])
			return False

		#ZHour
		if (int(zhour) > 12):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpZoneHour'])
			return False

		#Long, Lat
		#Deg
		if (int(deg) > 180 or int(deg2) > 180):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpLonDeg'])
			return False
		#ArcMin
		if (int(arcmin) > 59 or int(arcmin2) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpArcMin'])
			return False

		#Altitude
		if (int(alt) > 10000):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpAltitude'])
			return False

		#Check Date
		if (not util.checkDate(int(y), int(m), int(d))):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['InvalidDate'])
			return False

		return True


	def initialize(self, chrt):
		#General
		self.name.set(str(chrt.name))
		self.gender.set(chrt.male)
		#DateAndTime
		self.year.set(str(chrt.time.origyear))
		self.month.set(str(chrt.time.origmonth))
		self.day.set(str(chrt.time.origday))
		self.hour.set(str(chrt.time.hour))
		self.minute.set(str(chrt.time.minute))
		self.second.set(str(chrt.time.second))
		self.bc.set(chrt.time.bc)
		#CalendarAndZone
		self.cal.set(texts.calList[chrt.time.cal])
		self.zone.set(texts.zoneList[chrt.time.zt])
		if (chrt.time.plus):
			self.zplus.set(DataDlg.plusvalues[0])
		else:
			self.zplus.set(DataDlg.plusvalues[1])
		self.zhour.set(str(chrt.time.zh))
		self.zmin.set(str(chrt.time.zm))
		self.dst.set(chrt.time.dst)
		#Place
		self.deg.set(str(chrt.place.deglon))
		self.arcmin.set(str(chrt.place.minlon))
		if (chrt.place.east):
			self.longdir.set('e')
		else:
			self.longdir.set('w')
		self.deg2.set(str(chrt.place.deglat))
		self.arcmin2.set(str(chrt.place.minlat))
		if (chrt.place.north):
			self.latdir.set('n')
		else:
			self.latdir.set('s')
		self.placename.set(chrt.place.placename)
		self.alt.set(str(chrt.place.altitude))
		#Notes
		if (chrt.notes != ''):
			self.txt.insert(END, chrt.notes)


	def copyData(self):
		self.var_name = self.name.get()
		self.var_male = self.gender.get()
		#DateAndTime
		self.var_bc = self.bc.get()
		self.var_y = int(self.year.get())
		self.var_m = int(self.month.get())
		self.var_d = int(self.day.get())
		self.var_h = int(self.hour.get())
		self.var_mi = int(self.minute.get())
		self.var_s = int(self.second.get())
		#CalendarAndZone
		self.var_cal = self.cal.get()
		self.var_cal = texts.calList.index(self.var_cal)
		self.var_zone = self.zone.get()
		self.var_zone = texts.zoneList.index(self.var_zone)

		self.var_zplus = self.zplus.get()
		if (self.var_zplus == DataDlg.plusvalues[0]):
			self.var_zplus = True
		else:
			self.var_zplus = False
		self.var_zhour = int(self.zhour.get())
		self.var_zmin = int(self.zmin.get())
		self.var_dst = self.dst.get()
		#Place
		self.var_deg = int(self.deg.get())
		self.var_arcmin = int(self.arcmin.get())
		self.var_longdir = self.longdir.get()
		if (self.var_longdir == 'e'):
			self.var_longdir = True
		else:
			self.var_longdir = False
		self.var_deg2 = int(self.deg2.get())
		self.var_arcmin2 = int(self.arcmin2.get())
		self.var_latdir = self.latdir.get()
		if (self.var_latdir == 'n'):
			self.var_latdir = True
		else:
			self.var_latdir = False
		self.var_placename = self.placename.get()
		self.var_alt = int(self.alt.get())
		#Notes
		self.var_notes = self.txt.get(1.0, END)


	def check(self, chrt):
		changed = False
		if (chrt.name != self.var_name):
			changed = True
		if (chrt.male != self.var_male):
			changed = True
		#DateAndTime
		if (chrt.time.bc != self.var_bc):
			changed = True
		if (chrt.time.year != self.var_y):
			changed = True
		if (chrt.time.month != self.var_m):
			changed = True
		if (chrt.time.day != self.var_d):
			changed = True
		if (chrt.time.hour != self.var_h):
			changed = True
		if (chrt.time.minute != self.var_mi):
			changed = True
		if (chrt.time.second != self.var_s):
			changed = True
		#CalendarAndZone
		if (chrt.time.cal != self.var_cal):
			changed = True
		if (chrt.time.zt != self.var_zone):
			changed = True
		if (chrt.time.plus != self.var_zplus):
			changed = True
		if (chrt.time.zh != self.var_zhour):
			changed = True
		if (chrt.time.zm != self.var_zmin):
			changed = True
		if (chrt.time.dst != self.var_dst):
			changed = True
		#Place
		if (chrt.place.deglon != self.var_deg):
			changed = True
		if (chrt.place.minlon != self.var_arcmin):
			changed = True
		if (chrt.place.east != self.var_longdir):
			changed = True
		if (chrt.place.deglat != self.var_deg2):
			changed = True
		if (chrt.place.minlat != self.var_arcmin2):
			changed = True
		if (chrt.place.north != self.var_latdir):
			changed = True
		if (chrt.place.placename != self.var_placename):
			changed = True
		if (chrt.place.altitude != self.var_alt):
			changed = True
		#Notes
		if (chrt.notes != self.var_notes):
			changed = True

		return changed


	def ok(self, event=None):
		val = self.validate()
		if (not val):
			self.allright = False
			return False
		else:
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








