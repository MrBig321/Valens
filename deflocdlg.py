from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import placesdlg
import texts


#DefaultLocation
class DefLocDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	plusvalues = ('+', '-')

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsdatadlg['DefaultLocation'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Zone Panel
		zonepanel = ttk.LabelFrame(frame, text=texts.txtsdatadlg['Zone'])
		zonepanel.grid(column=1, row=0, padx=DefLocDlg.PANELDISTX, pady=DefLocDlg.PANELDISTY, sticky=(W,N,S,E)) 
			#GMTCombo
		gmtlabel = ttk.Label(zonepanel, text=texts.txtsdatadlg['GMT']+':')
		gmtlabel.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.zplus = StringVar()
		self.zpluscombo = ttk.Combobox(zonepanel, textvariable=self.zplus, width=3, state='readonly', values = DefLocDlg.plusvalues)
		self.zpluscombo.grid(column=1, row=2, padx=5, pady=5, sticky=(W))
		self.zplus.set(DefLocDlg.plusvalues[0])
		self.zpluscombo.bind('<<ComboboxSelected>>', self.zplusSelected)
			#ZoneHour
		zhourpanel = ttk.Frame(zonepanel)
		zhourpanel.grid(column=0, row=3, padx=5, pady=5, sticky=(W))
		zhourlabel = ttk.Label(zhourpanel, text=texts.txtsdatadlg['Hour']+':')
		zhourlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.zhour = StringVar()
		zhourcmd = zonepanel.register(self.validateZHour)
		zhourentry = ttk.Entry(zhourpanel, textvariable=self.zhour, width=3, validate='key', validatecommand=(zhourcmd, '%d'))
		zhourentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.zhour.set('')
			#ZoneMin
		zminpanel = ttk.Frame(zonepanel)
		zminpanel.grid(column=1, row=3, padx=5, pady=5, sticky=(W))
		zminlabel = ttk.Label(zminpanel, text=texts.txtsdatadlg['Min']+':')
		zminlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.zmin = StringVar()
		zmincmd = zonepanel.register(self.validateZMin)
		zminentry = ttk.Entry(zminpanel, textvariable=self.zmin, width=3, validate='key', validatecommand=(zmincmd, '%d'))
		zminentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.zmin.set('')
			#DST
		self.dst = BooleanVar()
		self.dst.set(False)
		dstbtn = ttk.Checkbutton(zonepanel, text=texts.txtsdatadlg['DST'], variable=self.dst, onvalue=True)
		dstbtn.grid(column=0, row=4, padx=5, pady=5, sticky=(W))

		#Place Panel
		placepanel = ttk.LabelFrame(frame, text=texts.txtsdatadlg['Place'])
		placepanel.grid(column=0, row=0, padx=DefLocDlg.PANELDISTX, pady=DefLocDlg.PANELDISTY, sticky=(W,E))
		longlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Long']+':')
		longlabel.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
			#Deg
		degpanel = ttk.Frame(placepanel)
		degpanel.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		deglabel = ttk.Label(degpanel, text=texts.txtsdatadlg['Deg']+':')
		deglabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.deg = StringVar()
		degcmd = zonepanel.register(self.validateDeg)
		degentry = ttk.Entry(degpanel, textvariable=self.deg, width=5, validate='key', validatecommand=(degcmd, '%d'))
		degentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.deg.set('')
			#Min
		arcminpanel = ttk.Frame(placepanel)
		arcminpanel.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
		arcminlabel = ttk.Label(arcminpanel, text=texts.txtsdatadlg['Min']+':')
		arcminlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.arcmin = StringVar()
		arcmincmd = zonepanel.register(self.validateArcMin)
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
		degcmd2 = zonepanel.register(self.validateDeg2)
		degentry2 = ttk.Entry(degpanel2, textvariable=self.deg2, width=5, validate='key', validatecommand=(degcmd2, '%d'))
		degentry2.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.deg2.set('')
			#Min
		arcminpanel2 = ttk.Frame(placepanel)
		arcminpanel2.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
		arcminlabel2 = ttk.Label(arcminpanel2, text=texts.txtsdatadlg['Min']+':')
		arcminlabel2.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.arcmin2 = StringVar()
		arcmincmd2 = zonepanel.register(self.validateArcMin2)
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
		placenamecmd = zonepanel.register(self.validatePlaceName)
		placenameentry = ttk.Entry(placepanel, textvariable=self.placename, width=22, validate='key', validatecommand=(placenamecmd, '%d'))
		placenameentry.grid(column=0, row=3, columnspan=3, padx=5, pady=5)
		self.placename.set('')
			#Altitude
		altlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Altitude']+':')
		altlabel.grid(column=0, row=4, padx=5, pady=5, sticky=(W))
		self.alt = StringVar()
		altcmd = zonepanel.register(self.validateAlt)
		altentry = ttk.Entry(placepanel, textvariable=self.alt, width=6, validate='key', validatecommand=(altcmd, '%d'))
		altentry.grid(column=1, row=4, padx=5, pady=5, sticky=(W))
		self.alt.set('')
		mlabel = ttk.Label(placepanel, text=texts.txtsdatadlg['Meter'])
		mlabel.grid(column=2, row=4, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=1, padx=5, pady=5, sticky=(S,E))

		placenameentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


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


	def zplusSelected(self, event=None):
		self.zpluscombo.selection_clear()


	def initialize(self, opts):
		#Zone
		if (opts.deflocplus):
			self.zplus.set(DefLocDlg.plusvalues[0])
		else:
			self.zplus.set(DefLocDlg.plusvalues[1])
		self.zhour.set(str(opts.defloczhour))
		self.zmin.set(str(opts.defloczminute))
		self.dst.set(opts.deflocdst)
		#Place
		self.deg.set(str(opts.defloclondeg))
		self.arcmin.set(str(opts.defloclonmin))
		if (opts.defloceast):
			self.longdir.set('e')
		else:
			self.longdir.set('w')

		self.deg2.set(str(opts.defloclatdeg))
		self.arcmin2.set(str(opts.defloclatmin))
		if (opts.deflocnorth):
			self.latdir.set('n')
		else:
			self.latdir.set('s')
		self.placename.set(opts.deflocname)
		self.alt.set(str(opts.deflocalt))


	def validate(self):
		zhour = self.zhour.get()
		zmin = self.zmin.get()
		deg = self.deg.get()
		arcmin = self.arcmin.get()
		deg2 = self.deg2.get()
		arcmin2 = self.arcmin2.get()
		alt = self.alt.get()

		if (zhour == '' or zmin == '' or deg == '' or arcmin == '' or deg2 == '' or arcmin2 == '' or alt == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
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

		#ZMin
		if (int(zmin) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpMin'])
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

		return True


	def copyData(self):
		#Zone
		self.var_zplus = self.zplus.get()
		if (self.var_zplus == DefLocDlg.plusvalues[0]):
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


	def check(self, opts):
		changed = False
		
		if (opts.deflocname != self.var_placename):
			opts.deflocname = self.var_placename
			changed = True

		if (opts.deflocplus != self.var_zplus):
			opts.deflocplus = self.var_zplus
			changed = True

		if (opts.defloczhour != self.var_zhour):
			opts.defloczhour = self.var_zhour
			changed = True

		if (opts.defloczminute != self.var_zmin):
			opts.defloczminute = self.var_zmin
			changed = True

		if (opts.deflocdst != self.var_dst):
			opts.deflocdst = self.var_dst
			changed = True

		#Place
		if (opts.defloclondeg != self.var_deg):
			opts.defloclondeg = self.var_deg
			changed = True

		if (opts.defloclonmin != self.var_arcmin):
			opts.defloclonmin = self.var_arcmin
			changed = True

		if (opts.defloceast != self.var_longdir):
			opts.defloceast = self.var_longdir
			changed = True

		if (opts.defloclatdeg != self.var_deg2):
			opts.defloclatdeg = self.var_deg2
			changed = True

		if (opts.defloclatmin != self.var_arcmin2):
			opts.defloclatmin = self.var_arcmin2
			changed = True

		if (opts.deflocnorth != self.var_latdir):
			opts.deflocnorth = self.var_latdir
			changed = True

		if (opts.deflocalt != self.var_alt):
			opts.deflocalt = self.var_alt
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





