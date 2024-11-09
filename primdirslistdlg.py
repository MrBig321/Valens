from tkinter import *
from tkinter import ttk
import astronomy
import chart
import planets
import primdirs
import texts
import util
import primdirsrangedlg
import primdirs
import chtime


class PrimDirsListDlg:

	def __init__(self, parent, rng, direc, pds, opts):
		self.parent = parent
		self.rng = rng
		self.direc = direc
		self.pds = pds
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsprimdirslistdlg['PrimaryDirs'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		black_rgb = util.getRGBTxt((0,0,0)) 
		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		bounds_rgb = util.getRGBTxt(self.options.clrframe)
		tree = ttk.Treeview(frame, columns=('prom', 'dir', 'sig', 'arc', 'date'), selectmode='none', height=15)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=60, anchor='center')
		tree.column('prom', width=160, anchor='center')
		tree.column('dir', width=40, anchor='center')
		tree.column('sig', width=160, anchor='center')
		tree.column('arc', width=70, anchor='center')
		tree.column('date', width=100, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('prom', text=texts.txtsprimdirslistdlg['Promissor'])
		tree.heading('dir', text=texts.txtsprimdirslistdlg['DC'])
		tree.heading('sig', text=texts.txtsprimdirslistdlg['Significator'])
		tree.heading('arc', text=texts.txtsprimdirslistdlg['Arc'])
		tree.heading('date', text=texts.txtsprimdirslistdlg['Date'])
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)

		tree.tag_configure('blacktext', background=bkg_rgb, foreground=black_rgb)
		tree.tag_configure('boundstext', background=bkg_rgb, foreground=bounds_rgb)
		tree.tag_configure('txttext', background=bkg_rgb, foreground=txt_rgb)

		tagtxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag', 'moontag', 'anodetag')
		for i in range(planets.Planets.BODIES_NUM-1):
			tree.tag_configure(tagtxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))

		tag = 'blacktext'
		cnt = 1
		num = len(self.pds)
		for i in range(num):
			#Promissor
			promtxt = ''

				#Planet		
			if (self.pds[i].prom < primdirs.PrimDir.OFFSANGLES):
				if (self.pds[i].promasp != primdirs.PrimDir.NONE and self.pds[i].promasp != chart.Chart.CONIUNCTIO):
					promtxt = texts.aspects[self.pds[i].promasp]+' '
				promtxt += texts.planets[self.pds[i].prom]
				if (not self.options.clrtextsintablesblack):
					tag = tagtxts[self.pds[i].prom]

				#Asc/MC
			elif (self.pds[i].prom >= primdirs.PrimDir.OFFSANGLES and self.pds[i].prom < primdirs.PrimDir.BOUND):
				promtxt = texts.angles[self.pds[i].prom-primdirs.PrimDir.OFFSANGLES]
				if (not self.options.clrtextsintablesblack):
					tag = 'txttext'

				#Bound
			elif (self.pds[i].prom >= primdirs.PrimDir.BOUND and self.pds[i].prom < primdirs.PrimDir.USER):
				promtxt = texts.signs[self.pds[i].prom-primdirs.PrimDir.BOUND]+' '
				promtxt += texts.planets[self.pds[i].prom2]
				if (not self.options.clrtextsintablesblack):
					tag = 'boundstext'

				#User
			elif (self.pds[i].prom == primdirs.PrimDir.USER):
				if (self.pds[i].promasp != primdirs.PrimDir.NONE and self.pds[i].promasp != chart.Chart.CONIUNCTIO):
					promtxt = texts.aspects[self.pds[i].promasp]+' '
				promtxt += texts.txtscommon['User']
				if (not self.options.clrtextsintablesblack):
					tag = 'txttext'

			dirtxt = texts.txtsprimdirslistdlg['D']
			if (not self.pds[i].direct):
				dirtxt = texts.txtsprimdirslistdlg['C']

			#Significator
			sigtxt = ''
				#Planet		
			if (self.pds[i].sig < primdirs.PrimDir.OFFSANGLES):
				if (self.pds[i].sigasp != primdirs.PrimDir.NONE and self.pds[i].sigasp != chart.Chart.CONIUNCTIO):
					sigtxt = texts.aspects[self.pds[i].sigasp]+' '
				sigtxt += texts.planets[self.pds[i].sig]

				#Asc/MC
			elif (self.pds[i].sig >= primdirs.PrimDir.OFFSANGLES and self.pds[i].sig < primdirs.PrimDir.BOUND):
				sigtxt = texts.angles[self.pds[i].sig-primdirs.PrimDir.OFFSANGLES]

				#User
			elif (self.pds[i].sig == primdirs.PrimDir.USER):
				if (self.pds[i].sigasp != primdirs.PrimDir.NONE and self.pds[i].sigasp != chart.Chart.CONIUNCTIO):
					sigtxt = texts.aspects[self.pds[i].sigasp]+' '
				sigtxt += texts.txtscommon['User']

			dirtxt = texts.txtsprimdirslistdlg['D']
			if (not self.pds[i].direct):
				dirtxt = texts.txtsprimdirslistdlg['C']

			arc = (int(self.pds[i].arc*1000))/1000.0
			arctxt = str(arc)

			year, month, day, h = astronomy.swe_revjul(self.pds[i].time, 1)
			datetxt = (str(year)).rjust(4)+'.'+(str(month)).zfill(2)+'.'+(str(day)).zfill(2)

			iid = tree.insert('', 'end', text=str(cnt)+'.', values=(promtxt, dirtxt, sigtxt, arctxt, datetxt), tags=tag)
			cnt += 1

		tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		prbtn = ttk.Button(okpanel, text=texts.txtscommon['Print'], command=self.onPrint)
		prbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(E))
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
#		self.allright = False
		self.center()
#		self.win.geometry('%dx%d+%d+%d' % (400, 300, 0, 0))
#		self.win.update_idletasks()

		self.deg_symbol = '\u00b0'


	def onPrint(self, event=None):
		zodtxts = (texts.txtsprimdirsdlg['SZNeither'], texts.txtsprimdirsdlg['SZPromissor'], texts.txtsprimdirsdlg['SZSignificator'], texts.txtsprimdirsdlg['SZBoth'])
		arr = ['0-25', '25-50', '50-75', '75-100', 'all']

		#Personal data
		chrt = self.parent.chart
		juliantxt = ''
		bctxt = ''
		if (chrt.time.cal == chtime.Time.JULIAN):
			juliantxt = texts.txtscommon['J']
		if (chrt.time.bc):
			bctxt = texts.txtscommon['BC']
		datetxt = texts.months[chrt.time.omonth-1]+' '+str(chrt.time.oday)+', '+str(chrt.time.oyear)+' '+juliantxt+' '+bctxt
		timetxt = str(chrt.time.hour).zfill(2)+':'+str(chrt.time.minute).zfill(2)+':'+str(chrt.time.second).zfill(2)+' '+texts.zoneList[chrt.time.zt]
		placetxt = chrt.place.placename
		dirlontxt = texts.txtscommon['E']
		if (not chrt.place.east):
			dirlontxt = texts.txtscommon['W']
		dirlattxt = texts.txtscommon['N']
		if (not chrt.place.north):
			dirlattxt = texts.txtscommon['S']
		coordtxt = (str(chrt.place.deglon)).zfill(2)+self.deg_symbol+(str(chrt.place.minlon)).zfill(2)+"'"+dirlontxt+'  '+(str(chrt.place.deglat)).zfill(2)+self.deg_symbol+(str(chrt.place.minlat)).zfill(2)+"'"+dirlattxt
		nametxt = chrt.name
		#end of Personal data

		li = []
		li.append(nametxt)
		li.append(datetxt)
		li.append(timetxt)
		li.append(placetxt)
		li.append(coordtxt)
		li.append('********************')

		li.append('Age: '+arr[self.rng])
		li.append('Direction: '+primdirsrangedlg.PrimDirsRangeDlg.dirarr[self.direc])
		li.append(texts.txtscommon['PDType'])
		li.append(texts.txtsprimdirsdlg['UseSZ']+': '+zodtxts[self.options.subzodiacal])
		if (self.options.subzodiacal == primdirs.PrimDirs.SZBOTH):
			if (self.options.bianchini):
				li.append(texts.txtsprimdirsdlg['Bianchini'])

		txtKey = 'Key: '
		if (self.options.pdkeydyn):
			txtKey += texts.txtsprimdirsdlg['Dynamic']
			txtKey += ', '+texts.typeListDyn[self.options.pdkeyd]
		else: 
			txtKey += texts.txtsprimdirsdlg['Static']
			txtKey += ', '+texts.typeListStat[self.options.pdkeys]
			if (self.options.pdkeys != primdirs.PrimDirs.USER):
				deg = primdirs.PrimDirs.staticData[self.options.pdkeys][primdirs.PrimDirs.DEG]
				minu = primdirs.PrimDirs.staticData[self.options.pdkeys][primdirs.PrimDirs.MIN]
				sec = primdirs.PrimDirs.staticData[self.options.pdkeys][primdirs.PrimDirs.SEC]
				txtKey	+= ' ('+str(deg)+'d '+str(minu)+'m '+str(sec)+'s)'
			else:
				txtKey	+= ' ('+str(self.options.pdkeydeg)+'d '+str(self.options.pdkeymin)+'m '+str(self.options.pdkeysec)+'s)'

		li.append(txtKey)

		if (self.options.zodpromsigasps[primdirs.PrimDirs.ASPSPROMSTOSIGS]):
			li.append(texts.txtsprimdirsdlg['ZodAspsPromsToSigs1']+' '+texts.txtsprimdirsdlg['ZodAspsPromsToSigs2'])
		if (self.options.zodpromsigasps[primdirs.PrimDirs.PROMSTOSIGASPS]):
			li.append(texts.txtsprimdirsdlg['ZodPromsToSigAsps1']+' '+texts.txtsprimdirsdlg['ZodPromsToSigAsps2'])
		if (self.options.ascmchcsasproms):
			li.append(texts.txtsprimdirsdlg['ZodAscMCHCsAsProms'])
		
		li.append(texts.txtsprimdirsdlg['Promissors']+':')
		plsli = []
		for i in range(len(self.options.promplanets)):
			if (self.options.promplanets[i]):
				plsli.append(texts.planets[i])

		if (len(plsli) > 0):
			li.append(','.join(plsli))

		if (self.options.pdsecmotion):
			li.append(texts.txtsprimdirsdlg['SecondaryMotion'])

		if (self.options.pdbounds):
			li.append(texts.txtsprimdirsdlg['Bounds'])

		if (self.options.pduser):
			txtS = 'North'
			if (self.options.pdusersouthern):
				txtS = 'South'
			li.append(texts.txtsprimdirsdlg['User']+' Lon.: ('+str(self.options.pduserlon[0])+'d '+str(self.options.pduserlon[1])+'m '+str(self.options.pduserlon[2])+'s) '+'Lat.: ('+str(self.options.pduserlat[0])+'d '+str(self.options.pduserlat[1])+'m '+str(self.options.pduserlat[2])+'s '+txtS+')')

		li.append(texts.txtscommon['Aspects']+':')
		aspsli = []
		for i in range(chart.Chart.ASPECT_NUM):
			if (self.options.pdaspects[i]):
				aspsli.append(texts.aspects[i])

		if (len(aspsli) > 0):
			li.append(','.join(aspsli))

		li.append(texts.txtsprimdirsdlg['Significators']+':')
		if (self.options.sigascmc[0] and self.options.sigascmc[1]):
			li.append(texts.ascmc[0]+', '+texts.ascmc[1])
		else:
			if (self.options.sigascmc[0]):
				li.append(texts.ascmc[0])
			if (self.options.sigascmc[1]):
				li.append(texts.ascmc[1])

		plsli2 = []
		for i in range(len(self.options.sigplanets)):
			if (self.options.sigplanets[i]):
				plsli2.append(texts.planets[i])

		if (len(plsli2) > 0):
			li.append(','.join(plsli2))

		if (self.options.pduser2):
			txtS2 = 'North'
			if (self.options.pduser2southern):
				txtS2 = 'South'
			li.append(texts.txtsprimdirsdlg['User']+' Lon.: ('+str(self.options.pduser2lon[0])+'d '+str(self.options.pduser2lon[1])+'m '+str(self.options.pduser2lon[2])+'s) '+'Lat.: ('+str(self.options.pduser2lat[0])+'d '+str(self.options.pduser2lat[1])+'m '+str(self.options.pduser2lat[2])+'s '+txtS2+')')

		li.append('********************')

		cnt = 1
		num = len(self.pds)
		for i in range(num):
			#Promissor
			promtxt = ''

				#Planet		
			if (self.pds[i].prom < primdirs.PrimDir.OFFSANGLES):
				if (self.pds[i].promasp != primdirs.PrimDir.NONE and self.pds[i].promasp != chart.Chart.CONIUNCTIO):
					promtxt = texts.aspects[self.pds[i].promasp]+' '
				promtxt += texts.planets[self.pds[i].prom]

				#Asc/MC
			elif (self.pds[i].prom >= primdirs.PrimDir.OFFSANGLES and self.pds[i].prom < primdirs.PrimDir.BOUND):
				promtxt = texts.angles[self.pds[i].prom-primdirs.PrimDir.OFFSANGLES]

				#Bound
			elif (self.pds[i].prom >= primdirs.PrimDir.BOUND and self.pds[i].prom < primdirs.PrimDir.USER):
				promtxt = texts.signs[self.pds[i].prom-primdirs.PrimDir.BOUND]+' '
				promtxt += texts.planets[self.pds[i].prom2]

				#User
			elif (self.pds[i].prom == primdirs.PrimDir.USER):
				if (self.pds[i].promasp != primdirs.PrimDir.NONE and self.pds[i].promasp != chart.Chart.CONIUNCTIO):
					promtxt = texts.aspects[self.pds[i].promasp]+' '
				promtxt += texts.txtscommon['User']

			dirtxt = texts.txtsprimdirslistdlg['D']
			if (not self.pds[i].direct):
				dirtxt = texts.txtsprimdirslistdlg['C']

			#Significator
			sigtxt = ''
				#Planet		
			if (self.pds[i].sig < primdirs.PrimDir.OFFSANGLES):
				if (self.pds[i].sigasp != primdirs.PrimDir.NONE and self.pds[i].sigasp != chart.Chart.CONIUNCTIO):
					sigtxt = texts.aspects[self.pds[i].sigasp]+' '
				sigtxt += texts.planets[self.pds[i].sig]

				#Asc/MC
			elif (self.pds[i].sig >= primdirs.PrimDir.OFFSANGLES and self.pds[i].sig < primdirs.PrimDir.BOUND):
				sigtxt = texts.angles[self.pds[i].sig-primdirs.PrimDir.OFFSANGLES]

				#User
			elif (self.pds[i].sig == primdirs.PrimDir.USER):
				if (self.pds[i].sigasp != primdirs.PrimDir.NONE and self.pds[i].sigasp != chart.Chart.CONIUNCTIO):
					sigtxt = texts.aspects[self.pds[i].sigasp]+' '
				sigtxt += texts.txtscommon['User']

			dirtxt = texts.txtsprimdirslistdlg['D']
			if (not self.pds[i].direct):
				dirtxt = texts.txtsprimdirslistdlg['C']

			arc = (int(self.pds[i].arc*1000))/1000.0
			arctxt = str(arc)

			year, month, day, h = astronomy.swe_revjul(self.pds[i].time, 1)
			datetxt = (str(year)).rjust(4)+'.'+(str(month)).zfill(2)+'.'+(str(day)).zfill(2)

			txt = str(cnt)+'. '+promtxt+' '+dirtxt+' --> '+sigtxt+' '+arctxt+' '+datetxt
			li.append(txt)
			cnt += 1

		with open('pds.txt', 'wt') as out:
			out.write('\n'.join(li))


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






