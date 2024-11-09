#import sys #sys.maxint
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import placeslistdlg
import geonames
import placedb
import texts
import util


#Derived from ttk and it doesn't seem to find tk in colum method!
#use e.g. tk.StrigVar()
# Shouldn't be derived from Treeview but create Treeview inside!?
class PlacesList:
	PLACE = 0
	LON = 1
	LAT = 2
	ZONE = 3
	ALT = 4
	COLNUM = ALT+1

	def __init__(self, parent):
		self.parent = parent
		self.tree = ttk.Treeview(parent, columns=('lon', 'lat', 'zone', 'alt'), selectmode='browse', height=16)

		self.tree.column('#0', width=140, anchor='center')
		self.tree.column('lon', width=80, anchor='center')
		self.tree.column('lat', width=70, anchor='center')
		self.tree.column('zone', width=60, anchor='center')
		self.tree.column('alt', width=60, anchor='center')

		ysb = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(parent, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

		self.tree.heading('#0', text=texts.txtsplacesdlg['Places'])
		self.tree.heading('lon', text=texts.txtsplacesdlg['Long'])
		self.tree.heading('lat', text=texts.txtsplacesdlg['Lat'])
		self.tree.heading('zone', text=texts.txtsplacesdlg['Zone'])
		self.tree.heading('alt', text=texts.txtsplacesdlg['Alt'])

		self.load()
		self.tree.bind('<<TreeviewSelect>>', self.onSelect)
		self.changed = False
		self.selitem = None


	def onSelect(self, event):
		self.selitem = self.tree.selection()[0]
#		vals = self.tree.item(self.selitem)
#		print (vals)
#		print(self.tree.item(item, 'text'))
#		print(self.tree.item(item, 'values'))
#		print(self.tree.item(item, 'tags'))


	def load(self):
		pdb = placedb.PlaceDB()
		pdb.read()

		self.iids = []
		for p in pdb.placedb:
			iid = self.tree.insert('', 'end', text=p.name, values=(p.lon, p.lat, p.tz, p.alt))
			self.iids.append(iid)


	def save(self):
		if (self.changed):
			pdb = placedb.PlaceDB()
	
			num = len(self.iids)
			for i in range(num):
				vals = self.tree.item(self.iids[i])
#				print(vals['text'], vals['values'][0], vals['values'][1], vals['values'][2], vals['values'][3])
#				print (self.tree.set(self.iids[i]))
				pdb.add(vals['text'], vals['values'][0], vals['values'][1], vals['values'][2], str(vals['values'][3]))  #alt is int if retrieved (see onSelect above)

			pdb.sort()
			pdb.write()

			self.changed = False


	def onAdd(self, item):
		iid = self.tree.insert('', 'end', text=item[0], values=(item[1], item[2], item[3], item[4]))
		self.iids.append(iid)
		self.tree.see(iid)
		self.tree.selection_set(iid)

		self.changed = True


	def onRemove(self):
		if (self.selitem != None):
			ret = messagebox.askyesno(parent=self.parent, message=texts.txtscommon['AreYouSure'], icon='question')
			if (ret):
				self.tree.delete(self.selitem)
				self.iids.remove(self.selitem)
				self.selitem = None
				self.changed = True

		else: messagebox.showinfo(parent=self.parent, message=texts.txtsplacesdlg['NoSelection'])


	def onRemoveAll(self):
		if (len(self.iids) > 0):
			ret = messagebox.askyesno(parent=self.parent, message=texts.txtscommon['AreYouSure'], icon='question')
			if (ret):
				num = len(self.iids)
				for i in range(num):
					self.tree.delete(self.iids[i])
				del self.iids[:]
				self.selitem = None
				self.changed = True



class PlacesDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	plusvalues = ('+', '-')

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsplacesdlg['Places'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Place Panel
		placepanel = ttk.LabelFrame(frame, text=texts.txtsplacesdlg['Place'])
		placepanel.grid(column=0, row=0, columnspan=2, padx=PlacesDlg.PANELDISTX, pady=PlacesDlg.PANELDISTY, sticky=(W,E,N,S))
		longlabel = ttk.Label(placepanel, text=texts.txtsplacesdlg['Long']+':')
		longlabel.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
			#Deg
		degpanel = ttk.Frame(placepanel)
		degpanel.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		deglabel = ttk.Label(degpanel, text=texts.txtsplacesdlg['Deg']+':')
		deglabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.deg = StringVar()
		degcmd = placepanel.register(self.validateDeg)
		degentry = ttk.Entry(degpanel, textvariable=self.deg, width=5, validate='key', validatecommand=(degcmd, '%d'))
		degentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.deg.set('')
			#Min
		arcminpanel = ttk.Frame(placepanel)
		arcminpanel.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
		arcminlabel = ttk.Label(arcminpanel, text=texts.txtsplacesdlg['Min']+':')
		arcminlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.arcmin = StringVar()
		arcmincmd = placepanel.register(self.validateArcMin)
		arcminentry = ttk.Entry(arcminpanel, textvariable=self.arcmin, width=5, validate='key', validatecommand=(arcmincmd, '%d'))
		arcminentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.arcmin.set('')
			#LonDir
		longdirpanel = ttk.Frame(placepanel)
		longdirpanel.grid(column=3, row=0, padx=5, pady=5, sticky=(W,N,S))
		self.longdir = StringVar()
		ebtn = ttk.Radiobutton(longdirpanel, text=texts.txtsplacesdlg['E'], variable=self.longdir, value='e')
		ebtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		wbtn = ttk.Radiobutton(longdirpanel, text=texts.txtsplacesdlg['W'], variable=self.longdir, value='w')
		wbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		self.longdir.set('e')

		latlabel = ttk.Label(placepanel, text=texts.txtsplacesdlg['Lat']+':')
		latlabel.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
			#Deg
		degpanel2 = ttk.Frame(placepanel)
		degpanel2.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		deglabel2 = ttk.Label(degpanel2, text=texts.txtsplacesdlg['Deg']+':')
		deglabel2.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.deg2 = StringVar()
		degcmd2 = placepanel.register(self.validateDeg2)
		degentry2 = ttk.Entry(degpanel2, textvariable=self.deg2, width=5, validate='key', validatecommand=(degcmd2, '%d'))
		degentry2.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.deg2.set('')
			#Min
		arcminpanel2 = ttk.Frame(placepanel)
		arcminpanel2.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
		arcminlabel2 = ttk.Label(arcminpanel2, text=texts.txtsplacesdlg['Min']+':')
		arcminlabel2.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.arcmin2 = StringVar()
		arcmincmd2 = placepanel.register(self.validateArcMin2)
		arcminentry2 = ttk.Entry(arcminpanel2, textvariable=self.arcmin2, width=5, validate='key', validatecommand=(arcmincmd2, '%d'))
		arcminentry2.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.arcmin2.set('')
			#LatDir
		latdirpanel = ttk.Frame(placepanel)
		latdirpanel.grid(column=3, row=1, padx=5, pady=5, sticky=(W,N,S))
		self.latdir = StringVar()
		nbtn = ttk.Radiobutton(latdirpanel, text=texts.txtsplacesdlg['N'], variable=self.latdir, value='n')
		nbtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		sbtn = ttk.Radiobutton(latdirpanel, text=texts.txtsplacesdlg['S'], variable=self.latdir, value='s')
		sbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		self.latdir.set('n')
			#PlaceName
		plname = ttk.Label(placepanel, text=texts.txtsplacesdlg['Name']+':')
		plname.grid(column=0, row=3, padx=5, pady=5)
		self.placename = StringVar()
		placenamecmd = placepanel.register(self.validatePlaceName)
		placenameentry = ttk.Entry(placepanel, textvariable=self.placename, width=22, validate='key', validatecommand=(placenamecmd, '%d'))
		placenameentry.grid(column=1, row=3, columnspan=2, padx=5, pady=5)
		self.placename.set('')
		searchbtn = ttk.Button(placepanel, text=texts.txtsplacesdlg['Search'], command=self.onSearch)
		searchbtn.grid(column=3, row=3, padx=5, pady=5)
		self.txtvar = StringVar()
		self.txtvar.set(texts.txtsplacesdlg['MaxNumberOnlineSearch']+': '+'2'.zfill(3))
		scalelabel = ttk.Label(placepanel, textvariable=self.txtvar)
		scalelabel.grid(column=0, row=4, columnspan=2, padx=5, pady=5)
		self.scalevar = IntVar()
		self.scalevar.set(2)
		scale = ttk.Scale(placepanel, orient=HORIZONTAL, from_=2, to=100, variable=self.scalevar, command=self.onScale)
		scale.grid(column=0, row=5, columnspan=4, padx=5, pady=5, sticky=(E, W))
			#Altitude
		altlabel = ttk.Label(placepanel, text=texts.txtsplacesdlg['Alt']+':')
		altlabel.grid(column=0, row=6, padx=5, pady=5, sticky=(W))
		self.alt = StringVar()
		altcmd = placepanel.register(self.validateAlt)
		altentry = ttk.Entry(placepanel, textvariable=self.alt, width=6, validate='key', validatecommand=(altcmd, '%d'))
		altentry.grid(column=1, row=6, padx=5, pady=5, sticky=(W))
		self.alt.set('')
		mlabel = ttk.Label(placepanel, text=texts.txtsplacesdlg['M'])
		mlabel.grid(column=2, row=6, padx=5, pady=5, sticky=(W))

		#Zone Panel
		zonepanel = ttk.LabelFrame(frame, text=texts.txtsplacesdlg['Zone'])
		zonepanel.grid(column=0, row=1, padx=PlacesDlg.PANELDISTX, pady=PlacesDlg.PANELDISTY, sticky=(W,N,S,E)) 
			#GMTCombo
		gmtlabel = ttk.Label(zonepanel, text=texts.txtsplacesdlg['GMT']+':')
		gmtlabel.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.zplus = StringVar()
		self.zpluscombo = ttk.Combobox(zonepanel, textvariable=self.zplus, width=3, state='readonly', values = PlacesDlg.plusvalues)
		self.zpluscombo.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		self.zplus.set(PlacesDlg.plusvalues[0])
		self.zpluscombo.bind('<<ComboboxSelected>>', self.zplusSelected)
			#ZoneHour
		zhourpanel = ttk.Frame(zonepanel)
		zhourpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		zhourlabel = ttk.Label(zhourpanel, text=texts.txtsplacesdlg['Hour']+':')
		zhourlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.zhour = StringVar()
		zhourcmd = zonepanel.register(self.validateZHour)
		zhourentry = ttk.Entry(zhourpanel, textvariable=self.zhour, width=3, validate='key', validatecommand=(zhourcmd, '%d'))
		zhourentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.zhour.set('')
			#ZoneMin
		zminpanel = ttk.Frame(zonepanel)
		zminpanel.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		zminlabel = ttk.Label(zminpanel, text=texts.txtsplacesdlg['Min']+':')
		zminlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.zmin = StringVar()
		zmincmd = zonepanel.register(self.validateZMin)
		zminentry = ttk.Entry(zminpanel, textvariable=self.zmin, width=3, validate='key', validatecommand=(zmincmd, '%d'))
		zminentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.zmin.set('')

		#Buttons
		btnspanel = ttk.LabelFrame(frame, text='')
		btnspanel.grid(column=1, row=1, padx=PlacesDlg.PANELDISTX, pady=PlacesDlg.PANELDISTY, sticky=(W,N,S,E)) 
		addbtn = ttk.Button(btnspanel, text=texts.txtsplacesdlg['Add'], command=self.addBtn, width=20)	#!?
		addbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W,E))
		removebtn = ttk.Button(btnspanel, text=texts.txtsplacesdlg['Remove'], command=self.removeBtn)
		removebtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W,E))
		removeallbtn = ttk.Button(btnspanel, text=texts.txtsplacesdlg['RemoveAll'], command=self.removeAllBtn)
		removeallbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W,E))

		#PlacesList
		listpanel = ttk.LabelFrame(frame, text='')
		listpanel.grid(column=2, row=0, rowspan=2, padx=PlacesDlg.PANELDISTX, pady=PlacesDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.treeobj = PlacesList(listpanel)
		self.treeobj.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=3, padx=5, pady=5, sticky=(S,E))

		placenameentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onScale(self, event=None):
		self.txtvar.set(texts.txtsplacesdlg['MaxNumberOnlineSearch']+': '+(str(self.scalevar.get())).zfill(3))


	def onSearch(self, event=None):
		txt = self.placename.get()
		if (txt == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsplacesdlg['PlaceEmpty'])
			return

		if (len(txt) < 3):
			messagebox.showerror(parent=self.win, message=texts.txtsplacesdlg['TooFewChars'])
			return

#		cc = self.win.cget('cursor')
		origcursor = self.win.config(cursor='watch')
		self.win.update_idletasks()
		maxnum = self.scalevar.get()
		geo = geonames.Geonames(self.placename.get(), maxnum) #.encode("utf-8"), maxnum)
		if (geo.get_location_info()):
			if (len(geo.li) == 1):
				self.fillFields(geo.li[0])
				self.win.config(cursor='left_ptr')
			else:
				#popup list
				pldlg = placeslistdlg.PlacesListDlg(self, geo.li)
				self.win.config(cursor='left_ptr')
				pldlg.doModal()
				if (pldlg.allright):
					idx = pldlg.getIdx()
					if (idx != None):
						self.fillFields(geo.li[idx])

		else:
			self.win.config(cursor='left_ptr')
			messagebox.showerror(parent=self.win, message=texts.txtsplacesdlg['NotFound'])


	def fillFields(self, it):
		self.placename.set(it[geonames.Geonames.NAME])

		#lon
		east = True
		lon = it[geonames.Geonames.LON]
		if (lon < 0.0):
			east = False
			lon *= -1
			
		d, m, s = util.decToDeg(lon)
		self.deg.set(str(d))
		self.arcmin.set(str(m))
		if (east):
			self.longdir.set('e')
		else:
			self.longdir.set('w')

		#lat
		north = True
		lat = it[geonames.Geonames.LAT]
		if (lat < 0.0):
			north = False
			lat *= -1
			
		d, m, s = util.decToDeg(lat)
		self.deg2.set(str(d))
		self.arcmin2.set(str(m))
		if (north):
			self.latdir.set('n')
		else:
			self.latdir.set('s')

		#zone
		plus = True
		gmtoffs = it[geonames.Geonames.GMTOFFS]
		if (gmtoffs < 0.0):
			plus = False
			gmtoffs *= -1

		gmtoffshour = int(gmtoffs)
		gmtoffsmin = int((gmtoffs-gmtoffshour)*60.0)

		self.zhour.set(str(gmtoffshour))
		self.zmin.set(str(gmtoffsmin))
		
		val = 0
		if (not plus):
			val = 1

		self.zplus.set(PlacesDlg.plusvalues[val])

		#altitude
		alt = int(it[geonames.Geonames.ALTITUDE])
		if (alt < 0):
			alt = 0

		self.alt.set(str(alt))


#	def isInternetOn(self):
#		try:
#			response=urllib2.urlopen('http://www.geonames.org', timeout=1)
#			return True
#		except urllib2.URLError:
#			pass
#		return False


	def addBtn(self):
		if (self.validate()):
			item = []
			item.append(self.placename.get())

			dirtxt = 'E'
			if (self.longdir.get() != 'e'):
				dirtxt = 'W'
			lon = self.deg.get().zfill(2)+dirtxt+self.arcmin.get().zfill(2)
			item.append(lon)

			dirtxt = 'N'
			if (self.latdir.get() != 'n'):
				dirtxt = 'S'
			lat = self.deg2.get().zfill(2)+dirtxt+self.arcmin2.get().zfill(2)
			item.append(lat)

			sign = '+'
			if (self.zplus.get() == PlacesDlg.plusvalues[1]):
				sign = '-'
			zone = sign+self.zhour.get()+':'+(self.zmin.get()).zfill(2)
			item.append(zone)

			alt = self.alt.get()
			item.append(alt)

			self.treeobj.onAdd(item)


	def removeBtn(self):
		self.treeobj.onRemove()


	def removeAllBtn(self):
		self.treeobj.onRemoveAll()


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


	def validatePlaceName(self, why):
		n = self.placename.get()
		if ((len(n) >= 20) and (int(why) == 1)):
			return False

		return True


	def zplusSelected(self, event=None):
		self.zpluscombo.selection_clear()


	def initialize(self):
		#Zone
		self.zplus.set(PlacesDlg.plusvalues[0])
		self.zhour.set('0')
		self.zmin.set('0')
		#Place
		self.deg.set('0')
		self.arcmin.set('0')
		self.longdir.set('e')
		self.deg2.set('0')
		self.arcmin2.set('0')
		self.latdir.set('n')
		self.placename.set('')
		self.alt.set('0')


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
		vals = self.treeobj.tree.item(self.treeobj.selitem)
		self.var_placename = vals['text']
		self.var_lon = vals['values'][0]
		self.var_lat = vals['values'][1]
		self.var_zone = vals['values'][2]
		self.var_alt = vals['values'][3]


	def ok(self, event=None):
		self.treeobj.save()
		if (self.treeobj.selitem != None):
			self.copyData()
			self.allright = True
			self.destroy()
		else: 
			messagebox.showinfo(parent=self.win, message=texts.txtsplacesdlg['NoSelection'])
			self.allright = False


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









