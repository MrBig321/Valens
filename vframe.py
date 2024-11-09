from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from tkinter import font
from tkinter import filedialog
import math
import os
import pickle
import datetime
import astronomy
import chtime
import chplace
import chart
import hellenisticchart
import roundchart
import planet
import planets
import houses
import common
import datadlg
import deflocdlg
import boundsdlg
import speculum1dlg
import speculum2dlg
import miscdlg
import lots7dlg
import lots2dlg
import velocitydlg
import antisciadlg
import riseplanetsdlg
import dodecatemoriadlg
import risesignsdlg
import midpointsdlg
import plhoursdlg
import appearancedlg
import ayanamsadlg
import colorsdlg
import fixedstarsdlg
import ephemerisdlg
import ephemcalc
import graphwnd
import chartwnd
import revolutions
import revolutionsdlg
import timespacedlg
import secdirsdlg
import stepperdlg
import electionstepperdlg
import secdir
import transitsmdlg
import transitsmonthdlg
import transits
import findtimedlg
import sectdlg
import userdlg
import userspeculumdlg
import placspec
import aboutdlg
import primdirsdlg
import primdirsrangedlg
import primdirslistdlg
import lotsoptdlg
import zodreloptdlg
import zodrelseldlg
import zodrell1dlg
import zodrell1
import texts
import util
#import pyscreenshot as ImageGrab # For Linux


class VFrame(Tk):

	XSIZE = 512
	YSIZE = 512

	APPERANCEID = 0
	AYANAMSAID = 1
	COLORSID = 2
	SECTID = 3
	NODESID = 4
	HOUSESID = 5
	BOUNDID = 6
	PRIMDIRS = 7
	LOTS = 8
	ZODREL = 9
	DEFAULTID = 10
	SEPARATORID = 11
	AUTOSAVEID = 12
	SAVEID = 13
	RELOADID = 14

	HOUSESARR = ('none', 'porphyry', 'alcabitus', 'regiomontanus', 'placidus')

	def __init__(self, opts, titletxt):
		Tk.__init__(self)

		self.fpathhors = 'Hors'
		self.fpathimgs = 'Images'
		
		self.options = opts

		self.title(titletxt)

		#Main menubar creation
		menubar = Menu(self)

		#Horoscope-menu
		self.mhoros = Menu(menubar, tearoff=0)
		self.mhoros.add_command(label=texts.menutxts['HMData'], command=self.onData, underline=0, accelerator="Ctrl+D")
		self.mhoros.add_command(label=texts.menutxts['HMLoad'], command=self.onLoad, underline=0, accelerator="Ctrl+L")
		self.mhoros.add_command(label=texts.menutxts['HMSave'], command=self.onSave, underline=0, accelerator="Ctrl+S")
		self.mhoros.add_command(label=texts.menutxts['HMSynastry'], command=self.onSynastry, underline=1, accelerator="Ctrl+Y")
		self.mhoros.add_command(label=texts.menutxts['HMEphemeris'], command=self.onEphemeris, underline=0, accelerator="Ctrl+E")
		self.mhoros.add_command(label=texts.menutxts['HMFindTime'], command=self.onFindTime, underline=0, accelerator="Ctrl+F")
		self.mhoros.add_separator()
		self.mhoros.add_command(label=texts.menutxts['HMExit'], command=self.Quit, underline=1, accelerator="Alt+X")

		#bind accelerator-keys
		self.bind('<Control-d>', self.onData)
		self.bind('<Control-l>', self.onLoad)
		self.bind('<Control-s>', self.onSave)
		self.bind('<Control-y>', self.onSynastry)
		self.bind('<Control-e>', self.onEphemeris)
		self.bind('<Control-f>', self.onFindTime)
		self.bind('<Alt-x>', self.Quit)

		#Tables-menu
		self.mtables = Menu(menubar, tearoff=0)
		self.mtables.add_command(label=texts.menutxts['TMSpeculum1'], command=self.onSpeculum1, accelerator="F1")
		self.mtables.add_command(label=texts.menutxts['TMSpeculum2'], command=self.onSpeculum2, accelerator="F2")
		self.mtables.add_command(label=texts.menutxts['TMMisc'], command=self.onMisc, accelerator="F3")
		self.mtables.add_command(label=texts.menutxts['TMLots7'], command=self.onLots7, accelerator="F4")
		self.mtables.add_command(label=texts.menutxts['TMLots2'], command=self.onLots2, accelerator="Ctrl+F4")
		self.mtables.add_command(label=texts.menutxts['TMVelocity'], command=self.onVelocity, accelerator="F5")
		self.mtables.add_command(label=texts.menutxts['TMAntiscia'], command=self.onAntiscia, accelerator="Ctrl+F5")
		self.mtables.add_command(label=texts.menutxts['TMRiseSet'], command=self.onRiseset, accelerator="F6")
		self.mtables.add_command(label=texts.menutxts['TMDodecatemoria'], command=self.onDodecatemoria, accelerator="Ctrl+F6")
		self.mtables.add_command(label=texts.menutxts['TMRiseSigns'], command=self.onRiseSigns, accelerator="F7")
		self.mtables.add_command(label=texts.menutxts['TMExactTransits'], command=self.onExactTransits, accelerator="Ctrl+F7")
		self.mtables.add_command(label=texts.menutxts['TMMidpoints'], command=self.onMidpoints, accelerator="F8")
		self.mtables.add_command(label=texts.menutxts['TMUserSpeculum'], command=self.onUserSpeculum, accelerator="Ctrl+F8")
		self.mtables.add_command(label=texts.menutxts['TMPlanetaryHours'], command=self.onPlHours, accelerator="F9")
		self.mtables.add_command(label=texts.menutxts['TMFixedStars'], command=self.onFixedStars, accelerator="F10")
		self.mtables.add_command(label=texts.menutxts['TMZodRel'], command=self.onZodRel, accelerator="F11")
		self.mtables.add_command(label=texts.menutxts['TMPrimaryDirs'], command=self.onPrimaryDirs, accelerator="F12")

		self.bind('<F1>', self.onSpeculum2)
		self.bind('<F2>', self.onSpeculum2)
		self.bind('<F3>', self.onMisc)
		self.bind('<F4>', self.onLots7)
		self.bind('<Control-F4>', self.onLots2)
		self.bind('<F5>', self.onVelocity)
		self.bind('<Control-F5>', self.onAntiscia)
		self.bind('<F6>', self.onRiseset)
		self.bind('<Control-F6>', self.onDodecatemoria)
		self.bind('<F7>', self.onRiseSigns)
		self.bind('<Control-F7>', self.onExactTransits)
		self.bind('<F8>', self.onMidpoints)
		self.bind('<Control-F8>', self.onUserSpeculum)
		self.bind('<F9>', self.onPlHours)
		self.bind('<F10>', self.onFixedStars)
		self.bind('<F11>', self.onZodRel)
		self.bind('<F12>', self.onPrimaryDirs)

		#Chart-menu
		self.mcharts = Menu(menubar, tearoff=0)
		self.mcharts.add_command(label=texts.menutxts['CMSecondaryDirs'], command=self.onSecDirsChart, accelerator="Shift+Ctrl+F1")
		self.mcharts.add_command(label=texts.menutxts['CMRevolutions'], command=self.onRevolutionsChart, accelerator="Shift+Ctrl+F2")
		self.mcharts.add_command(label=texts.menutxts['CMTransits'], command=self.onTransitsChart, accelerator="Shift+Ctrl+F3")
		self.mcharts.add_command(label=texts.menutxts['CMElections'], command=self.onElectionsChart, accelerator="Shift+Ctrl+F4")
		self.mcharts.add_command(label=texts.menutxts['CMSyzygy'], command=self.onSyzygyChart, accelerator="Shift+Ctrl+F5")
		self.mcharts.add_command(label=texts.menutxts['CMTheOther'], command=self.onTheOtherChart, accelerator="Shift+Ctrl+F6")

		self.bind('<Shift-Control-F1>', self.onSecDirsChart)
		self.bind('<Shift-Control-F2>', self.onRevolutionsChart)
		self.bind('<Shift-Control-F3>', self.onTransitsChart)
		self.bind('<Shift-Control-F4>', self.onElectionsChart)
		self.bind('<Shift-Control-F5>', self.onSyzygyChart)
		self.bind('<Shift-Control-F6>', self.onTheOtherChart)

		#Options-menu
		self.moptions = Menu(menubar, tearoff=0)
		self.moptions.add_command(label=texts.menutxts['OMAppearance'], command=self.onAppearanceOpt, underline=0, accelerator="Shift+A")
		self.moptions.add_command(label=texts.menutxts['OMAyanamsha'], command=self.onAyanamsaOpt, underline=1, accelerator="Shift+Y")
		self.moptions.add_command(label=texts.menutxts['OMColors'], command=self.onColorsOpt, underline=0, accelerator="Shift+C")
		self.moptions.add_command(label=texts.menutxts['OMSect'], command=self.onSectOpt, underline=3, accelerator="Shift+T")

		self.onode = StringVar()
		self.moptionsnodesub = Menu(self.moptions, tearoff=0)
		self.moptionsnodesub.add_radiobutton(label=texts.menutxts['OMNMean'], variable=self.onode, value='mean', command=self.onNodeAccelMean, accelerator="Shift+M")
		self.moptionsnodesub.add_radiobutton(label=texts.menutxts['OMNTrue'], variable=self.onode, value='true', command=self.onNodeAccelTrue, accelerator="Shift+W")
		self.setNode()

		self.moptions.add_cascade(label=texts.menutxts['OMNodes'], menu=self.moptionsnodesub)

		self.ohouses = StringVar()
		self.moptionshousessub = Menu(self.moptions, tearoff=0)
		self.moptionshousessub.add_radiobutton(label=texts.menutxts['OMHSNone'], variable=self.ohouses, value=VFrame.HOUSESARR[0], command=self.onHousesNone, accelerator="Shift+F1")
		self.moptionshousessub.add_radiobutton(label=texts.menutxts['OMHSPorphyrius'], variable=self.ohouses, value=VFrame.HOUSESARR[1], command=self.onHousesPorphyry, accelerator="Shift+F2")
		self.moptionshousessub.add_radiobutton(label=texts.menutxts['OMHSAlcabitus'], variable=self.ohouses, value=VFrame.HOUSESARR[2], command=self.onHousesAlcabitus, accelerator="Shift+F3")
		self.moptionshousessub.add_radiobutton(label=texts.menutxts['OMHSRegiomontanus'], variable=self.ohouses, value=VFrame.HOUSESARR[3], command=self.onHousesRegiomontanus, accelerator="Shift+F4")
		self.moptionshousessub.add_radiobutton(label=texts.menutxts['OMHSPlacidus'], variable=self.ohouses, value=VFrame.HOUSESARR[4], command=self.onHousesPlacidus, accelerator="Shift+F5")
		self.setHouses()

		self.moptions.add_cascade(label=texts.menutxts['OMHouses'], menu=self.moptionshousessub)

		self.moptions.add_command(label=texts.menutxts['OMBounds'], command=self.onBoundsOpt, underline=0, accelerator="Shift+B")
		self.moptions.add_command(label=texts.menutxts['OMPrimaryDirs'], command=self.onPrimDirsOpt, underline=0, accelerator="Shift+P")
		self.moptions.add_command(label=texts.menutxts['OMLots'], command=self.onLotsOpt, underline=0, accelerator="Shift+L")
		self.moptions.add_command(label=texts.menutxts['OMZodRel'], command=self.onZodRelOpt, underline=0, accelerator="Shift+Z")
		self.moptions.add_command(label=texts.menutxts['OMDefLocationOpt'], command=self.onDefLocOpt, underline=0, accelerator="Shift+D")
		self.oauto = BooleanVar()
		self.moptions.add_separator()
		self.moptions.add_checkbutton(label=texts.menutxts['OMAutoSave'], variable=self.oauto, onvalue=True, offvalue=False, command=self.onAutosaveOpts, underline=1, accelerator="Shift+U")
		self.oauto.set(False)
		self.moptions.add_command(label=texts.menutxts['OMSave'], command=self.onSaveOpts, underline=0, accelerator="Shift+S")
		self.moptions.add_command(label=texts.menutxts['OMReload'], command=self.onReloadOpts, underline=0, accelerator="Shift+R")

		self.bind('<Shift-A>', self.onAppearanceOpt)
		self.bind('<Shift-Y>', self.onAyanamsaOpt)
		self.bind('<Shift-C>', self.onColorsOpt)
		self.bind('<Shift-T>', self.onSectOpt)
		self.bind('<Shift-W>', self.onNodeAccelTrue)
		self.bind('<Shift-M>', self.onNodeAccelMean)
		self.bind('<Shift-F1>', self.onHousesNone)
		self.bind('<Shift-F2>', self.onHousesPorphyry)
		self.bind('<Shift-F3>', self.onHousesAlcabitus)
		self.bind('<Shift-F4>', self.onHousesRegiomontanus)
		self.bind('<Shift-F5>', self.onHousesPlacidus)
		self.bind('<Shift-B>', self.onBoundsOpt)
		self.bind('<Shift-P>', self.onPrimDirsOpt)
		self.bind('<Shift-L>', self.onLotsOpt)
		self.bind('<Shift-Z>', self.onZodRelOpt)
		self.bind('<Shift-D>', self.onDefLocOpt)
		self.bind('<Shift-U>', self.onAutosaveOpts)
		self.bind('<Shift-S>', self.onSaveOpts)
		self.bind('<Shift-R>', self.onReloadOpts)

		#Help-menu
		self.mhelp = Menu(menubar, tearoff=0)
		self.mhelp.add_command(label=texts.menutxts['HEMAbout'], command=self.onAbout, underline=0, accelerator="Alt+A")

		self.bind('<Alt-A>', self.onAbout)

		#main menu
		menubar.add_cascade(label=texts.menutxts['MHoroscope'], menu=self.mhoros, underline=0)
		menubar.add_cascade(label=texts.menutxts['MTables'], menu=self.mtables, underline=0)
		menubar.add_cascade(label=texts.menutxts['MCharts'], menu=self.mcharts, underline=0)
		menubar.add_cascade(label=texts.menutxts['MOptions'], menu=self.moptions, underline=0)
		menubar.add_cascade(label=texts.menutxts['MHelp'], menu=self.mhelp, underline=1)
		
		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		self.config(bg=bkg_rgb, height=VFrame.YSIZE, width=VFrame.XSIZE, menu=menubar)

		self.minsize(300,300)
		self.center()

		os.environ['SE_EPHE_PATH'] = ''
		common.common = common.Common()
		astronomy.swe_set_ephe_path(common.common.ephepath)

		self.moptions.entryconfig(VFrame.SAVEID, state=DISABLED)
		if (self.options.checkOptsFile()):
			self.moptions.entryconfig(VFrame.RELOADID, state=NORMAL)
		else:
			self.moptions.entryconfig(VFrame.RELOADID, state=DISABLED)

		#Popup-menu
		self.bw = BooleanVar()
		self.pmenu = Menu(self, tearoff=0)
		self.pmenu.add_checkbutton(label=texts.txtscommon['BW'], variable=self.bw, command=self.onBW, onvalue=True)
		self.pmenu.add_command(label=texts.txtscommon['Print'], command=self.onPrint, accelerator="Ctrl+P")
		self.bind('<Button-3>', self.onPMenu)

		self.bind('<Button-1>', self.onLeftClick)
		self.bind_all("<Control-p>", self.onPrint)

		self.HereAndNow()
		self.firsttime = True
		self.prevw = VFrame.XSIZE
		self.prevh = VFrame.YSIZE

		self.initVars()

		if (self.options.hellenistic):
			self.hchart = hellenisticchart.HellenisticChart(self, self.chart, self.options, (VFrame.XSIZE, VFrame.YSIZE))
		else:
			self.hchart = roundchart.RoundChart(self, self.chart, self.options, (VFrame.XSIZE, VFrame.YSIZE))
		self.hchart.can.pack(fill=BOTH, expand=1)

		self.bind('<Configure>', self.onResize)

		self.chldren = []
		self.closing = False


	def onLeftClick(self, event=None):
		self.pmenu.unpost()


	def onBW(self, event=None):
		self.hchart.bw = self.bw.get()
		w = self.winfo_width()
		h = self.winfo_height()
		self.hchart.drawCanvas(self.chart, self.options, (w, h))


	def onPrint(self, event=None):
#		self.grabcanvas = ImageGrab.grab(bbox=self.getBBox())
#		self.grabcanvas.save("out.jpg")
		print('Commented out')


	def getBBox(self):
		x=self.hchart.can.winfo_rootx()+self.hchart.can.winfo_x()
		y=self.hchart.can.winfo_rooty()+self.hchart.can.winfo_y()
		x1=x+self.hchart.can.winfo_width()
		y1=y+self.hchart.can.winfo_height()
		box=(x,y,x1,y1)
		return box


	def onPMenu(self, event=None):
		self.pmenu.post(event.x_root, event.y_root)


	def HereAndNow(self):
		plac = chplace.Place(self.options.deflocname, self.options.defloclondeg, self.options.defloclonmin, 0, self.options.defloceast, self.options.defloclatdeg, self.options.defloclatmin, 0, self.options.deflocnorth, self.options.deflocalt)

		now = datetime.datetime.now()
		tim = chtime.Time(now.year, now.month, now.day, now.hour, now.minute, now.second, False, chtime.Time.GREGORIAN, chtime.Time.ZONE, self.options.deflocplus, self.options.defloczhour, self.options.defloczminute, self.options.deflocdst, plac)

		self.chart = chart.Chart(texts.txtsdatadlg['HereAndNow'], True, chart.Chart.RADIX, tim, plac, '', self.options)


	def onResize(self, event):
		self.update_idletasks()
		w = self.winfo_width()
		h = self.winfo_height()
		if (self.firsttime or w != self.prevw or h != self.prevh):
			self.firsttime = False
			self.hchart.drawCanvas(self.chart, self.options, (w, h))
			self.prevw = w
			self.prevh = h
#		self.can.configure(width=event.width, height=event.height)


	def onLoad(self, event=None):
		dpath = '.'
		if (os.path.isdir(self.fpathhors)):
			dpath = self.fpathhors
		filename = filedialog.askopenfilename(parent=self, title=texts.txtsfiles['OpenHor'], initialdir=dpath, defaultextension=texts.txtsfiles['HorExtension'])

		if (len(filename) != 0): #according to the docs in case of cancel should return with an empty string
			chrt = self.subLoad(filename)
			self.fpathhors, fname = os.path.split(filename)

			if (chrt != None):
				self.chart = chrt
				self.initVars()

				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				self.destroyChildren()


#In order to be compatible with pickle of python2 (because of Morinus) fix_imports and protocol is used in Load and Save. Remove them to get rid of backward compatibility
	def subLoad(self, fpath, full=True):
		chrt = None

		try:
			f = open(fpath, 'rb')		
			name = pickle.load(f, fix_imports=True)
			male = pickle.load(f, fix_imports=True)
			htype = pickle.load(f, fix_imports=True)
			htype = chart.Chart.RADIX
			bc = pickle.load(f, fix_imports=True)
			year = pickle.load(f, fix_imports=True)
			month = pickle.load(f, fix_imports=True)
			day = pickle.load(f, fix_imports=True)
			hour = pickle.load(f, fix_imports=True)
			minute = pickle.load(f, fix_imports=True)
			second = pickle.load(f, fix_imports=True)
			cal = pickle.load(f, fix_imports=True)
			zt = pickle.load(f, fix_imports=True)
			plus = pickle.load(f, fix_imports=True)
			zh = pickle.load(f, fix_imports=True)
			zm = pickle.load(f, fix_imports=True)
			dst = pickle.load(f, fix_imports=True)
			placename = pickle.load(f, fix_imports=True)
			deglon = pickle.load(f, fix_imports=True)
			minlon = pickle.load(f, fix_imports=True)
			seclon = pickle.load(f, fix_imports=True)
			east = pickle.load(f, fix_imports=True)
			deglat = pickle.load(f, fix_imports=True)
			minlat = pickle.load(f, fix_imports=True)
			seclat = pickle.load(f, fix_imports=True)
			north = pickle.load(f, fix_imports=True)
			altitude = pickle.load(f, fix_imports=True)
			notes = pickle.load(f, fix_imports=True)
			f.close()

			place = chplace.Place(placename, deglon, minlon, 0, east, deglat, minlat, seclat, north, altitude)
			time = chtime.Time(year, month, day, hour, minute, second, bc, cal, zt, plus, zh, zm, dst, place)
			chrt = chart.Chart(name, male, chart.Chart.RADIX, time, place, notes, self.options, full)
		except IOError:
			messagebox.showerror(message=texts.txtsfiles['FileError'])

		return chrt 


	def onSave(self, event=None):
		dpath = '.'
		if (os.path.isdir(self.fpathhors)):
			dpath = self.fpathhors
			name = self.chart.name
			if (name == ''):
				name = texts.txtsfiles['Untitled']
		filename = filedialog.asksaveasfilename(parent=self, title=texts.txtsfiles['SaveHor'], initialdir=dpath, initialfile=name, defaultextension=texts.txtsfiles['HorExtension'])

		if (len(filename) != 0): #according to the docs in case of cancel should return with an empty string
			try:
				f = open(filename, 'wb')		
				pickle.dump(self.chart.name, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.male, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.htype, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.bc, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.origyear, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.origmonth, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.origday, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.hour, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.minute, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.second, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.cal, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.zt, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.plus, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.zh, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.zm, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.time.dst, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.placename, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.deglon, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.minlon, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.seclon, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.east, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.deglat, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.minlat, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.seclat, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.north, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.place.altitude, f, fix_imports=True, protocol=2)
				pickle.dump(self.chart.notes, f, fix_imports=True, protocol=2)
				self.fpathhors, fname = os.path.split(filename)
				f.close()
			except IOError:
				messagebox.showerror(message=texts.txtsfiles['FileError'])


	def onData(self, event=None):
		dlg = datadlg.DataDlg(self, self.options)
		dlg.initialize(self.chart)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.chart)
			if (changed):
				plac = chplace.Place(dlg.var_placename, dlg.var_deg, dlg.var_arcmin, 0, dlg.var_longdir, dlg.var_deg2, dlg.var_arcmin2, 0, dlg.var_latdir, dlg.var_alt)
				tim = chtime.Time(dlg.var_y, dlg.var_m, dlg.var_d, dlg.var_h, dlg.var_mi, dlg.var_s, dlg.var_bc, dlg.var_cal, dlg.var_zone, dlg.var_zplus, dlg.var_zhour, dlg.var_zmin, dlg.var_dst, plac)
				self.chart = chart.Chart(dlg.var_name, dlg.var_male, chart.Chart.RADIX, tim, plac, dlg.var_notes, self.options)

				self.chart.recalc()
				self.initVars()
				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				self.destroyChildren()


	def onSynastry(self, event=None):
		dpath = '.'
		if (os.path.isdir(self.fpathhors)):
			dpath = self.fpathhors
		filename = filedialog.askopenfilename(parent=self, title=texts.txtsfiles['OpenHor'], initialdir=dpath, defaultextension='.hor')

		if (len(filename) != 0): #according to the docs in case of cancel should return with an empty string
			chrt = self.subLoad(filename, False)
			self.fpathhors, fname = os.path.split(filename)

			if (chrt != None):
				synwnd = chartwnd.ChartWnd(self, texts.txtscommon['Synastry'], self.chart, chrt, self.options, True)
				self.chldren.append(synwnd)
				synwnd.show()


	def onEphemeris(self, event=None):
		dlg = ephemerisdlg.EphemerisDlg(self)
		dlg.doModal()
		if (dlg.allright):
			year  = dlg.var_year
			origcursor = self.config(cursor='watch')
			self.update_idletasks()
			eph = ephemcalc.EphemCalc(year, self.options)
			self.config(cursor='left_ptr')
			ephemwnd = graphwnd.GraphWnd(self, year, eph.posArr, self.options)
			self.chldren.append(ephemwnd)
			ephemwnd.show()


	def onFindTime(self, event=None):
		dlg = findtimedlg.FindTimeDlg(self, self.options)
		dlg.doModal()


	#TABLES
	def onSpeculum1(self, event=None):
		dlg = self.getChild(speculum1dlg.Speculum1Dlg)
		if (dlg == None):
			dlg = speculum1dlg.Speculum1Dlg(self, self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onSpeculum2(self, event=None):
		dlg = self.getChild(speculum2dlg.Speculum2Dlg)
		if (dlg == None):
			dlg = speculum2dlg.Speculum2Dlg(self, self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onMisc(self, event=None):
		dlg = self.getChild(miscdlg.MiscDlg)
		if (dlg == None):
			dlg = miscdlg.MiscDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onLots7(self, event=None):
		dlg = self.getChild(lots7dlg.Lots7Dlg)
		if (dlg == None):
			dlg = lots7dlg.Lots7Dlg(self, self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onLots2(self, event=None):
		dlg = self.getChild(lots2dlg.Lots2Dlg)
		if (dlg == None):
			dlg = lots2dlg.Lots2Dlg(self, self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onVelocity(self, event=None):
		dlg = self.getChild(velocitydlg.VelocityDlg)
		if (dlg == None):
			dlg = velocitydlg.VelocityDlg(self, self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onAntiscia(self, event=None):
		dlg = self.getChild(antisciadlg.AntisciaDlg)
		if (dlg == None):
			dlg = antisciadlg.AntisciaDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onRiseset(self, event=None):
		dlg = self.getChild(riseplanetsdlg.RisePlanetsDlg)
		if (dlg == None):
			dlg = riseplanetsdlg.RisePlanetsDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onDodecatemoria(self, event=None):
		dlg = self.getChild(dodecatemoriadlg.DodecatemoriaDlg)
		if (dlg == None):
			dlg = dodecatemoriadlg.DodecatemoriaDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onExactTransits(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		trdlg = transitsmdlg.TransitsMDlg(self)
		trdlg.initialize(self.mtrdlg_year, self.mtrdlg_month)	
		trdlg.doModal()
		if (trdlg.allright):
			year = self.mtrdlg_year = trdlg.var_y
			month = self.mtrdlg_month = trdlg.var_m

			origcursor = self.config(cursor='watch')
			self.update_idletasks()
			trans = transits.Transits()
			trans.month(year, month, self.chart)

			dlg = transitsmonthdlg.TransitsMonthDlg(self, trans.transits, year, month, self.options)
			self.config(cursor='left_ptr')
			self.chldren.append(dlg)
			dlg.doModal()


	def onRiseSigns(self, event=None):
		dlg = self.getChild(risesignsdlg.RiseSignsDlg)
		if (dlg == None):
			dlg = risesignsdlg.RiseSignsDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onMidpoints(self, event=None):
		dlg = self.getChild(midpointsdlg.MidpointsDlg)
		if (dlg == None):
			dlg = midpointsdlg.MidpointsDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onUserSpeculum(self, event=None):
		dlg = userdlg.UserDlg(self)
		dlg.doModal()		#No need to call initialize()
		if (dlg.allright):
			d = dlg.var_deg
			m = dlg.var_min
			s = dlg.var_sec
			d2 = dlg.var_deg2
			m2 = dlg.var_min2
			s2 = dlg.var_sec2
			southern = dlg.var_southern

			lon = d+m/60.0+s/3600.0
			lat = d2+m2/60.0+s2/3600.0
			if (southern):
				lat *= -1

			ra, decl, dist = astronomy.swe_cotrans(lon, lat, 1.0, -self.chart.obl[0])
			spec = placspec.PlacidianSpeculum(self.chart.place.lat, self.chart.houses.ascmc[houses.Houses.MC][houses.Houses.RA], lon, lat, ra, decl)

			dlg = userspeculumdlg.UserSpeculumDlg(self, spec, self.chart.ayanamsa, self.options)
			self.chldren.append(dlg)
			dlg.doModal()


	def onPlHours(self, event=None):
		dlg = self.getChild(plhoursdlg.PlHoursDlg)
		if (dlg == None):
			dlg = plhoursdlg.PlHoursDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onFixedStars(self, event=None):
		dlg = self.getChild(fixedstarsdlg.FixedStarsDlg)
		if (dlg == None):
			dlg = fixedstarsdlg.FixedStarsDlg(self, self.chart, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onZodRel(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		seldlg = zodrelseldlg.ZodRelSelDlg(self)
		seldlg.doModal()
		if (seldlg.allright):
			zdl1 = zodrell1.ZodRelL1(self.chart.time, seldlg.var_sel, seldlg.var_sca, self.options)
			zdl1.calc()
			dlg = zodrell1dlg.ZodRelL1Dlg(self, zdl1.zrs, self.options)
			self.chldren.append(dlg)
			dlg.doModal()


	def onPrimaryDirs(self, event=None):
		dlg = primdirsrangedlg.PrimDirsRangeDlg(self, self.chart, self.options)
		dlg.doModal()
		pds = dlg.pds
		rng = primdirsrangedlg.PrimDirsRangeDlg.arr.index(dlg.age.get())
		direc = primdirsrangedlg.PrimDirsRangeDlg.dirarr.index(dlg.direct.get())

		if (dlg.abort.isReady()):
			dlg = primdirslistdlg.PrimDirsListDlg(self, rng, direc, pds, self.options)
			self.chldren.append(dlg)
			dlg.doModal()


	#Charts
	def onSecDirsChart(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		sdsdlg = secdirsdlg.SecDirsDlg(self)
		sdsdlg.initialize(self.secdirsdlg_age, self.secdirsdlg_direct, self.secdirsdlg_soltime)
		sdsdlg.doModal()
		if (sdsdlg.allright):
			age = self.secdirsdlg_age = sdsdlg.var_age
			direct = self.secdirsdlg_direct = sdsdlg.var_direct
			soltime = self.secdirsdlg_soltime = sdsdlg.var_soltime

			zt = chtime.Time.LOCALMEAN
			if (soltime):
				zt = chtime.Time.LOCALAPPARENT
			zh = 0
			zm = 0

			sdir = secdir.SecDir(self.chart, age, direct, soltime)
			y, m, d, hour, minute, second = sdir.compute()

			dlg = timespacedlg.TimeSpaceDlg(self, texts.txtssecdirdlg['SecondaryDirs'], self.options)
			ti = (y, m, d, hour, minute, second, self.chart.time.cal, zt, zh, zm)
			dlg.initialize(self.chart, ti)	
			dlg.doModal()
			if (dlg.allright):
				place = chplace.Place(dlg.var_placename, dlg.var_deg, dlg.var_arcmin, 0, dlg.var_longdir, dlg.var_deg2, dlg.var_arcmin2, 0, dlg.var_latdir, dlg.var_alt)
				time = chtime.Time(y, m, d, hour, minute, second, False, self.chart.time.cal, zt, dlg.var_zplus, zh, zm, False, place)

				secdirchart = chart.Chart(self.chart.name, self.chart.male, chart.Chart.DIRECTION, time, place, '', self.options, False)

				secdirwnd = chartwnd.ChartWnd(self, texts.txtscommon['SecondaryDirs'], self.chart, secdirchart, self.options)
				self.chldren.append(secdirwnd)
				secdirwnd.show()

				stepdlg = stepperdlg.StepperDlg(secdirwnd, secdirwnd, self.chart, age, direct, soltime, self.options)
				stepdlg.doModal()


	def onRevolutionsChart(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		revdlg = revolutionsdlg.RevolutionsDlg(self)
		revdlg.initialize(self.revdlg_pl, self.revdlg_year, self.revdlg_month, self.revdlg_day)
		revdlg.doModal()
		if (revdlg.allright):
			self.revdlg_pl = revdlg.var_pl
			self.revdlg_year = revdlg.var_y
			self.revdlg_month = revdlg.var_m
			self.revdlg_day = revdlg.var_d

			origcursor = self.config(cursor='watch')
			self.update_idletasks()
			revs = revolutions.Revolutions()
			result = revs.compute(revdlg.var_pl, revdlg.var_y, revdlg.var_m, revdlg.var_d, self.chart)
			self.config(cursor='left_ptr')

			if (result):
				t1, t2, t3, t4, t5, t6 = revs.t[0], revs.t[1], revs.t[2], revs.t[3], revs.t[4], revs.t[5] 
				if (self.options.ayanamsa != 0 and revdlg.var_pl == planets.Planets.SUN):
					t1, t2, t3, t4, t5, t6 = self.calcPrecNutCorrectedSolar(revs) #y, m, d, hour, min, sec
	
				dlg = timespacedlg.TimeSpaceDlg(self, texts.txtsrevolutionsdlg['Revolutions'], self.options)
				ti = (t1, t2, t3, t4, t5, t6, chtime.Time.GREGORIAN, chtime.Time.GREENWICH, 0, 0)
				dlg.initialize(self.chart, ti)	

				dlg.doModal()
				if (dlg.allright):
					place = chplace.Place(dlg.var_placename, dlg.var_deg, dlg.var_arcmin, 0, dlg.var_longdir, dlg.var_deg2, dlg.var_arcmin2, 0, dlg.var_latdir, dlg.var_alt)#Same as for the transits
					time = chtime.Time(t1, t2, t3, t4, t5, t6, False, dlg.var_cal, chtime.Time.GREENWICH, dlg.var_zplus, 0, 0, False, place)
	
					revchart = chart.Chart(self.chart.name, self.chart.male, chart.Chart.REVOLUTION, time, place, '', self.options, False)
	
					revwnd = chartwnd.ChartWnd(self, texts.txtscommon['Revolution'], self.chart, revchart, self.options)
					self.chldren.append(revwnd)
					revwnd.show()
			else:
				messagebox.showerror(message=texts.txtscommon['CouldnotComputeRevolution'])


	def calcPrecNutCorrectedSolar(self, revs):
		time = chtime.Time(revs.t[0], revs.t[1], revs.t[2], revs.t[3], revs.t[4], revs.t[5], False, self.chart.time.cal, chtime.Time.GREENWICH, False, 0, 0, False, self.chart.place, False)
		#The algorithm of the Janus astrological program
		jdSol = time.jd
		JD1900 = 2415020.5
		FBAyanamsa1900 = astronomy.swe_get_ayanamsa_ut(JD1900)

		rflag, dat, serr = astronomy.swe_calc_ut(JD1900, astronomy.SE_ECL_NUT, 0)
		NutLon1900 = dat[2]
		SVP1900 = 360.0-FBAyanamsa1900-NutLon1900

		#calc natalprecfrom1900
		rflag, dat, serr = astronomy.swe_calc_ut(self.chart.time.jd, astronomy.SE_ECL_NUT, 0)
		NutLonNatal = dat[2]
		SVPNatal = 360.0-self.chart.ayanamsa-NutLonNatal
		NatalChartPrecessionFrom1900 = SVPNatal-SVP1900

		#Calc SVP for return date
		NatalSunLon = self.chart.planets.planets[planets.Planets.SUN].data[planet.Planet.LON]
		DiffAngle = 50.0 # this is my idea
		pflag = astronomy.SEFLG_SWIEPH+astronomy.SEFLG_SPEED

		#Keep recalculating transiting Sun position using new jdSol until
		#DiffAngle is small enough.
		while (DiffAngle > 0.00001):
			rflag, dat, serr = astronomy.swe_calc_ut(jdSol, astronomy.SE_SUN, pflag)
			TranSunLon = dat[0]
			TranSunVel = dat[3]

			rflag, dat, serr = astronomy.swe_calc_ut(jdSol, astronomy.SE_ECL_NUT, 0)
			FBAyanamsaReturn = astronomy.swe_get_ayanamsa_ut(jdSol)
			NutLonReturn = dat[2]
			SVPReturn = 360.0-FBAyanamsaReturn-NutLonReturn

			SolPrecessionFrom1900 = SVPReturn-SVP1900
			Precession = SolPrecessionFrom1900-NatalChartPrecessionFrom1900 #

			TranSunLon = TranSunLon+Precession

			DiffAngle = NatalSunLon-TranSunLon

			if (math.fabs(DiffAngle) > 180.0):
				DiffAngle = DiffAngle-util.sgn(DiffAngle)*360.0

			CorrectionJD = DiffAngle/TranSunVel

			jdSol = jdSol+CorrectionJD

			fromjdtime = astronomy.swe_revjul(jdSol, astronomy.SE_GREG_CAL)

		h, mi, s = util.decToDeg(fromjdtime[3])
		return fromjdtime[0], fromjdtime[1], fromjdtime[2], h, mi, s


	def onTransitsChart(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		dlg = timespacedlg.TimeSpaceDlg(self, texts.txtscommon['Transits'], self.options)
		dlg.initialize(self.chart)

		dlg.doModal()
		if (dlg.allright):
			place = chplace.Place(dlg.var_placename, dlg.var_deg, dlg.var_arcmin, 0, dlg.var_longdir, dlg.var_deg2, dlg.var_arcmin2, 0, dlg.var_latdir, dlg.var_alt)#Same as for the transits
			time = chtime.Time(dlg.var_y, dlg.var_m, dlg.var_d, dlg.var_h, dlg.var_mi, dlg.var_s, dlg.var_bc, dlg.var_cal, dlg.var_zone, dlg.var_zplus, dlg.var_zhour, dlg.var_zmin, dlg.var_dst, place)

			trchart = chart.Chart(self.chart.name, self.chart.male, chart.Chart.TRANSIT, time, place, '', self.options, False)

			trwnd = chartwnd.ChartWnd(self, texts.txtscommon['Transit'], self.chart, trchart, self.options)
			self.chldren.append(trwnd)
			trwnd.show()


	def onElectionsChart(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		time = chtime.Time(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second, self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.dst, self.chart.place)

		electionchart = chart.Chart(self.chart.name, self.chart.male, chart.Chart.TRANSIT, time, self.chart.place, '', self.options, False)

		electionwnd = chartwnd.ChartWnd(self, texts.txtscommon['Elections'], self.chart, electionchart, self.options)
		self.chldren.append(electionwnd)
		electionwnd.show()

		estepdlg = electionstepperdlg.ElectionStepperDlg(electionwnd, electionwnd, self.chart, self.options)
		estepdlg.doModal()


	def onSyzygyChart(self, event=None):
		if (self.chart.time.bc):
			messagebox.showinfo(parent=self, message=texts.txtscommon['NotAvailable'])
			return

		syzygychart = chart.Chart(self.chart.name, self.chart.male, chart.Chart.RADIX, self.chart.syzygy.time, self.chart.place, '', self.options, False)
		syzwnd = chartwnd.ChartWnd(self, texts.txtscommon['Syzygy'], self.chart, syzygychart, self.options)
		self.chldren.append(syzwnd)
		syzwnd.show()


	def onTheOtherChart(self, event=None):
		otherwnd = chartwnd.ChartWnd(self, '', self.chart, self.chart, self.options, False, True, True)
		self.chldren.append(otherwnd)
		otherwnd.show()


	#OPTIONS
	def onAppearanceOpt(self, event=None):
		topo = self.options.topocentric
		hell = self.options.hellenistic
		dlg = appearancedlg.AppearanceDlg(self)
		dlg.initialize(self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				if (topo != self.options.topocentric):
					self.chart.recalc()

				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()

				if (hell != self.options.hellenistic):
					self.hchart.can.pack_forget()
					if (self.options.hellenistic):
						self.hchart = hellenisticchart.HellenisticChart(self, self.chart, self.options, (w, h))
					else:
						self.hchart = roundchart.RoundChart(self, self.chart, self.options, (w, h))
					self.hchart.can.pack(fill=BOTH, expand=1)
				else:
					self.hchart.drawCanvas(self.chart, self.options, (w, h))

				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onBoundsOpt(self, event=None):
		dlg = boundsdlg.BoundsDlg(self, self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onPrimDirsOpt(self, event=None):
		dlg = primdirsdlg.PrimDirsDlg(self)
		dlg.initialize(self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onLotsOpt(self, event=None):
		dlg = lotsoptdlg.LotsOptDlg(self)
		dlg.initialize(self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				self.chart.recalc()
				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onZodRelOpt(self, event=None):
		dlg = zodreloptdlg.ZodRelOptDlg(self)
		dlg.initialize(self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onDefLocOpt(self, event=None):
		dlg = deflocdlg.DefLocDlg(self)
		dlg.initialize(self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()


	def onColorsOpt(self, event=None):
		dlg = colorsdlg.ColorsDlg(self, self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				for i in range(planets.Planets.PLANETS_NUM+1):
					self.options.clrplanets[i] = dlg.clrarr[i]

				self.options.clrframe = dlg.clrarr[planets.Planets.ANODE+1]
				self.options.clrsigns = dlg.clrarr[planets.Planets.ANODE+2]
				self.options.clrAscMC = dlg.clrarr[planets.Planets.ANODE+3]
				self.options.clrbackground = dlg.clrarr[planets.Planets.ANODE+4]
				self.options.clrtexts = dlg.clrarr[planets.Planets.ANODE+5]
				self.options.clrtextsintablesblack = dlg.textsblack.get()

				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onSectOpt(self, event=None):
		dlg = sectdlg.SectDlg(self)
		dlg.initialize(self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				self.chart.recalc()
				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onAyanamsaOpt(self, event=None):
		dlg = ayanamsadlg.AyanamsaDlg(self, self.options)
		dlg.doModal()
		if (dlg.allright):
			changed = dlg.check(self.options)
			if (changed):
				self.chart.recalc()	
				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()
				self.hchart.drawCanvas(self.chart, self.options, (w, h))

				#Update options-menuitems and save
				self.enableOptMenus(True, True)
				if (self.options.autosave):
					self.options.save()

				self.destroyChildren()


	def onAutosaveOpts(self, event=None):
		#Is this check necessary? It will toggle!
		changed = self.options.autosave != self.oauto.get()
		if (changed):
			self.options.autosave = self.oauto.get()
			if (self.options.autosave):
				self.options.save()
				self.enableOptMenus(False, True)


	def onSaveOpts(self, event=None):
		if (self.moptions.entrycget(VFrame.SAVEID, 'state') != 'disabled'):
			self.options.save()
			self.enableOptMenus(False, True)


	def onReloadOpts(self, event=None):
		if (self.moptions.entrycget(VFrame.RELOADID, 'state') != 'disabled'):
			ret = messagebox.askyesno(message=texts.txtscommon['AreYouSure'], icon='question')
			if (ret):
				self.options.reload()
				self.options.removeOptsFile()
				self.setNode()
				self.setHouses()
				self.enableOptMenus(False, False)

				self.chart.recalc()

				#Change Canvas
				self.update_idletasks()
				w = self.winfo_width()
				h = self.winfo_height()

				self.hchart.can.pack_forget()
				if (self.options.hellenistic):
					self.hchart = hellenisticchart.HellenisticChart(self, self.chart, self.options, (w, h))
				else:
					self.hchart = roundchart.RoundChart(self, self.chart, self.options, (w, h))
				self.hchart.can.pack(fill=BOTH, expand=1)
	
				self.destroyChildren()


	def enableOptMenus(self, enableSave, enableReload):
		#if (self.moptions.entrycget(0, "state") == "normal"):
		if (not enableSave):
			self.moptions.entryconfig(VFrame.SAVEID, state=DISABLED)
		else:
			self.moptions.entryconfig(VFrame.SAVEID, state=NORMAL)

		if (not enableReload):
			self.moptions.entryconfig(VFrame.RELOADID, state=DISABLED)
		else:
			self.moptions.entryconfig(VFrame.RELOADID, state=NORMAL)


	def onNode(self, event=None):
		mn = True
		if (self.onode.get() != 'mean'):
			mn = False
		changed = self.options.meannode != mn
		if (changed):
			self.enableOptMenus(True, True)
			self.options.meannode = mn
			if (self.options.autosave):
				self.options.save()
			self.chart.setNodes()

			#Change Canvas
			self.update_idletasks()
			w = self.winfo_width()
			h = self.winfo_height()
			self.hchart.drawCanvas(self.chart, self.options, (w, h))

			self.destroyChildren()


	def onNodeAccelMean(self, event=None):
		self.onode.set('mean')
		self.onNode()


	def onNodeAccelTrue(self, event=None):
		self.onode.set('true')
		self.onNode()


	def setNode(self):
		if (self.options.meannode):
			self.onode.set('mean')
		else:
			self.onode.set('true')


	def onHouses(self, event=None):
		num = len(VFrame.HOUSESARR)
		for i in range(num):
			if (VFrame.HOUSESARR[i] == self.ohouses.get()):
				break

		changed = self.options.hsys != i
		if (changed):
			self.enableOptMenus(True, True)
			self.options.hsys = i
			if (self.options.autosave):
				self.options.save()
			self.chart.setHouses()

			#Change Canvas
			self.update_idletasks()
			w = self.winfo_width()
			h = self.winfo_height()
			self.hchart.drawCanvas(self.chart, self.options, (w, h))

			self.destroyChildren()


	def onHousesNone(self, event=None):
		self.ohouses.set(VFrame.HOUSESARR[0])
		self.onHouses()


	def onHousesPorphyry(self, event=None):
		self.ohouses.set(VFrame.HOUSESARR[1])
		self.onHouses()


	def onHousesAlcabitus(self, event=None):
		self.ohouses.set(VFrame.HOUSESARR[2])
		self.onHouses()


	def onHousesRegiomontanus(self, event=None):
		self.ohouses.set(VFrame.HOUSESARR[3])
		self.onHouses()


	def onHousesPlacidus(self, event=None):
		self.ohouses.set(VFrame.HOUSESARR[4])
		self.onHouses()


	def setHouses(self, event=None):
		self.ohouses.set(VFrame.HOUSESARR[self.options.hsys])


	#HELP
	def onAbout(self, event=None):
		dlg = aboutdlg.AboutDlg(self)
		dlg.doModal()


	def initVars(self):
		#SecDirs
		self.secdirsdlg_age = 0
		self.secdirsdlg_direct = True
		self.secdirsdlg_soltime = True

		#Revolutions
		self.revdlg_pl = planets.Planets.SUN
		year = self.chart.time.year
		month = self.chart.time.month
		day = self.chart.time.day
		self.revdlg_year, self.revdlg_month, self.revdlg_day = util.incrDay(year, month, day)

		#Exact Transits
		year = self.chart.time.year
		month = self.chart.time.month
		self.mtrdlg_year, self.mtrdlg_month = util.incrMonth(year, month)


	def getChild(self, cl):
		num = len(self.chldren)
		for i in range(num):
			if (isinstance(self.chldren[i], cl)):
				return self.chldren[i]

		return None


	def destroying(self, obj):
		if (not self.closing):
			num = len(self.chldren)
			for i in range(num):
				if (self.chldren[i] == obj):
					del self.chldren[i]
					break


	def destroyChildren(self):
		self.closing = True
		num = len(self.chldren)
		for i in range(num):
			self.chldren[i].destroy()
		del self.chldren[:]
		self.closing = False


	def Quit(self):#, event=None):
		self.destroyChildren()
		self.quit()


	def center(self):
#		self.update_idletasks()
		sw = self.winfo_screenwidth()
		sh = self.winfo_screenheight()
#		w = self.winfo_width()
#		h = self.winfo_height()
		w = VFrame.XSIZE
		h = VFrame.YSIZE
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.geometry('%dx%d+%d+%d' % (w, h, x, y))








