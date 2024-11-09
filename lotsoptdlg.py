from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import copy
import chart
import planets
import rangechecker
import util
import texts


class LotsOptDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	#Component of a Lot #Maybe to Options!?
	ASC, IC, DSC, MC, HC1, HC2, HC3, HC4, HC5, HC6, HC7, HC8, HC9, HC10, HC11, HC12 = range(16)
	SAT, JUP, MAR, SUN, VEN, MER, MOO = range(16, 23)
	PLS = SAT
	ASCLORD, ICLORD, DSCLORD, MCLORD, HC1LORD, HC2LORD, HC3LORD, HC4LORD, HC5LORD, HC6LORD, HC7LORD, HC8LORD, HC9LORD, HC10LORD, HC11LORD, HC12LORD = range(23, 39)
	HCLORD = ASCLORD
	SATLORD, JUPLORD, MARLORD, SUNLORD, VENLORD, MERLORD, MOOLORD = range(39, 46)
	PLSLORD = SATLORD
	SYZ = MOOLORD+1
	SYZLORD = SYZ+1
	LT = SYZLORD+1
	LTLORD = LT+1
	LD = LTLORD+1
	LDLORD = LD+1
	LH = LDLORD+1
	LHLORD = LH+1
	DE = LHLORD+1
	RE = DE+1
	RELORD = RE+1

	###
	NAME = 0
	FORMULA = 1
	DIURNAL = 2

	DIURNALTXT = '*'
	LORDTXT = '!'

	MAX_LOTS_NUM = 40


	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtslotsdlg['Lots'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		self.refs = []

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Editor panel
		edpanel = ttk.LabelFrame(frame, text='')
		edpanel.grid(column=0, row=0, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		label = ttk.Label(edpanel, text=texts.txtslotsdlg['Name']+':')
		label.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.name = StringVar()
		namecmd = edpanel.register(self.validateName)
		nameentry = ttk.Entry(edpanel, textvariable=self.name, width=17, validate='key', validatecommand=(namecmd, '%d'))
		nameentry.grid(column=0, row=0, padx=80, pady=5, sticky=(W))
		self.name.set('')
		#Formula
		forpanel = ttk.LabelFrame(edpanel, text=texts.txtslotsdlg['Formula'])
		forpanel.grid(column=0, row=1, columnspan=2, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.comp1 = StringVar()
		self.compcb1 = ttk.Combobox(forpanel, textvariable=self.comp1, width=4, state='readonly', values=texts.lotComponentList)
		self.compcb1.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.comp1.set(texts.lotComponentList[0])
		self.compcb1.bind('<<ComboboxSelected>>', self.onCompCB1)
		label = ttk.Label(forpanel, text='+(')
		label.grid(column=1, row=0, padx=5, pady=0, sticky=(W))
		self.comp2 = StringVar()
		self.compcb2 = ttk.Combobox(forpanel, textvariable=self.comp2, width=4, state='readonly', values=texts.lotComponentList)
		self.compcb2.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
		self.comp2.set(texts.lotComponentList[0])
		self.compcb2.bind('<<ComboboxSelected>>', self.onCompCB2)
		label = ttk.Label(forpanel, text=' - ')
		label.grid(column=3, row=0, padx=5, pady=0, sticky=(W))
		self.comp3 = StringVar()
		self.compcb3 = ttk.Combobox(forpanel, textvariable=self.comp3, width=4, state='readonly', values=texts.lotComponentList)
		self.compcb3.grid(column=4, row=0, padx=5, pady=5, sticky=(W))
		self.comp3.set(texts.lotComponentList[0])
		self.compcb3.bind('<<ComboboxSelected>>', self.onCompCB3)
		label = ttk.Label(forpanel, text=')')
		label.grid(column=5, row=0, padx=5, pady=0, sticky=(W))
		#Diurnal
		self.diurnal = BooleanVar()
		self.diurnal.set(True)
		diurnalbtn = ttk.Checkbutton(edpanel, text=texts.txtslotsdlg['Diurnal'], variable=self.diurnal, onvalue=True)
		diurnalbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		#Reference
		refpanel = ttk.LabelFrame(edpanel, text=texts.txtslotsdlg['Reference'])
		refpanel.grid(column=0, row=3, columnspan=2, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.refcomp1 = StringVar()
		self.refcompcb1 = ttk.Combobox(refpanel, textvariable=self.refcomp1, width=4, state='readonly', values=self.refs)
		self.refcompcb1.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
#		self.refcomp1.set('')
		self.refcompcb1.configure(state='disabled')
		self.refcompcb1.bind('<<ComboboxSelected>>', self.onRefCompCB1)
		self.refcomp2 = StringVar()
		self.refcompcb2 = ttk.Combobox(refpanel, textvariable=self.refcomp2, width=4, state='readonly', values=self.refs)
		self.refcompcb2.grid(column=1, row=0, padx=25, pady=5, sticky=(W))
#		self.refcomp2.set('')
		self.refcompcb2.configure(state='disabled')
		self.refcompcb2.bind('<<ComboboxSelected>>', self.onRefCompCB2)
		self.refcomp3 = StringVar()
		self.refcompcb3 = ttk.Combobox(refpanel, textvariable=self.refcomp3, width=4, state='readonly', values=self.refs)
		self.refcompcb3.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
#		self.refcomp3.set('')
		self.refcompcb3.configure(state='disabled')
		self.refcompcb3.bind('<<ComboboxSelected>>', self.onRefCompCB3)
		#Degrees
		degpanel = ttk.LabelFrame(edpanel, text=texts.txtslotsdlg['Degree'])
		degpanel.grid(column=0, row=4, columnspan=2, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.degsigncomp1 = StringVar()
		self.degsigncompcb1 = ttk.Combobox(degpanel, textvariable=self.degsigncomp1, width=6, state='readonly', values=texts.signs)
		self.degsigncompcb1.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.degsigncomp1.set(texts.signs[0])
		self.degsigncompcb1.configure(state='disabled')
		self.degsigncompcb1.bind('<<ComboboxSelected>>', self.onDegSignCompCB1)
		self.degsigncomp2 = StringVar()
		self.degsigncompcb2 = ttk.Combobox(degpanel, textvariable=self.degsigncomp2, width=6, state='readonly', values=texts.signs)
		self.degsigncompcb2.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		self.degsigncomp2.set(texts.signs[0])
		self.degsigncompcb2.configure(state='disabled')
		self.degsigncompcb2.bind('<<ComboboxSelected>>', self.onDegSignCompCB2)
		self.degsigncomp3 = StringVar()
		self.degsigncompcb3 = ttk.Combobox(degpanel, textvariable=self.degsigncomp3, width=6, state='readonly', values=texts.signs)
		self.degsigncompcb3.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
		self.degsigncomp3.set(texts.signs[0])
		self.degsigncompcb3.configure(state='disabled')
		self.degsigncompcb3.bind('<<ComboboxSelected>>', self.onDegSignCompCB3)
		self.degcomp1 = StringVar()
		degcomp1cmd = edpanel.register(self.validateDegComp1)
		self.degcomp1entry = ttk.Entry(degpanel, textvariable=self.degcomp1, width=3, validate='key', validatecommand=(degcomp1cmd, '%d'))
		self.degcomp1entry.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.degcomp1entry.configure(state='disabled')
		self.degcomp1.set('0')
		self.degcomp2 = StringVar()
		degcomp2cmd = edpanel.register(self.validateDegComp2)
		self.degcomp2entry = ttk.Entry(degpanel, textvariable=self.degcomp2, width=3, validate='key', validatecommand=(degcomp2cmd, '%d'))
		self.degcomp2entry.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		self.degcomp2entry.configure(state='disabled')
		self.degcomp2.set('0')
		self.degcomp3 = StringVar()
		degcomp3cmd = edpanel.register(self.validateDegComp3)
		self.degcomp3entry = ttk.Entry(degpanel, textvariable=self.degcomp3, width=3, validate='key', validatecommand=(degcomp3cmd, '%d'))
		self.degcomp3entry.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
		self.degcomp3entry.configure(state='disabled')
		self.degcomp3.set('0')
		#Checkboxes
		chkpanel = ttk.LabelFrame(edpanel, text='')
		chkpanel.grid(column=0, row=5, columnspan=2, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.hcsigns = BooleanVar()
		self.hcsigns.set(False)
		hcsignsbtn = ttk.Checkbutton(chkpanel, text=texts.txtslotsdlg['HCSigns'], variable=self.hcsigns, command=self.onHCSigns, onvalue=True)
		hcsignsbtn.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.hcsignsasc = BooleanVar()
		self.hcsignsasc.set(False)
		self.hcsignsascbtn = ttk.Checkbutton(chkpanel, text=texts.txtslotsdlg['HCSignsAsc'], variable=self.hcsignsasc, onvalue=True)
		self.hcsignsascbtn.grid(column=0, row=2, padx=25, pady=5, sticky=(W))
		#Buttons
		btnpanel = ttk.LabelFrame(frame, text='')
		btnpanel.grid(column=0, row=2, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		addbtn = ttk.Button(btnpanel, text=texts.txtslotsdlg['Add'], width=25, command=self.onAddBtn)
		addbtn.grid(column=0, row=0, padx=5, pady=0)
		modifybtn = ttk.Button(btnpanel, text=texts.txtslotsdlg['Modify'], width=25, command=self.onModifyBtn)
		modifybtn.grid(column=0, row=1, padx=5, pady=5)
		removebtn = ttk.Button(btnpanel, text=texts.txtslotsdlg['Remove'], width=25, command=self.onRemoveBtn)
		removebtn.grid(column=0, row=2, padx=5, pady=0)
		removeallbtn = ttk.Button(btnpanel, text=texts.txtslotsdlg['RemoveAll'], width=25, command=self.onRemoveAllBtn)
		removeallbtn.grid(column=0, row=3, padx=5, pady=5)
		#List
		listpanel = ttk.LabelFrame(frame, text='')
		listpanel.grid(column=1, row=0, rowspan=3, padx=LotsOptDlg.PANELDISTX, pady=LotsOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.tree = ttk.Treeview(listpanel, columns=('name', 'formula', 'diurnal'), selectmode='browse', height=20)

		bkg_rgb = util.getRGBTxt((255, 255, 255))
#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		self.tree.column('#0', width=50, anchor='center')
		self.tree.column('name', width=120, anchor='center')
		self.tree.column('formula', width=200, anchor='center')
		self.tree.column('diurnal', width=60, anchor='center')

		ysb = ttk.Scrollbar(listpanel, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(listpanel, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)
		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)

	#	self.tree.heading('#0', text='')
		self.tree.heading('name', text=texts.txtslotsdlg['Name'])
		self.tree.heading('formula', text=texts.txtslotsdlg['Formula'])
		self.tree.heading('diurnal', text=texts.txtslotsdlg['Diurnal'])

		self.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=5, pady=5)
		self.tree.bind('<Button-1>', self.onListClicked)

		self.iids = []
		#ref-array

		self.cnt = 0

		self.changed = False

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=3, padx=5, pady=5, sticky=(S,E))

		nameentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onHCSigns(self, event=None):
		if (self.hcsigns.get()):
			self.hcsignsascbtn.configure(state='normal')
		else:
			self.hcsignsascbtn.configure(state='disabled')


	def onListClicked(self, event=None):
		item = self.tree.identify('item', event.x, event.y)
		if (item != ''):
			idx = self.iids.index(item)
#			print ("you clicked on", self.tree.item(item,"text"))
			self.fillWidgets(idx)


	def fillWidgets(self, i):
		val = self.tree.item(self.iids[i])
		name = val['values'][LotsOptDlg.NAME]
		form = val['values'][LotsOptDlg.FORMULA]
		f1 = self.getFormula(form, 1)
		f2 = self.getFormula(form, 2)
		f3 = self.getFormula(form, 3)
		fs = [f1, f2, f3]

		cbs	= (self.comp1, self.comp2, self.comp3)
		degsigncbs = (self.degsigncompcb1, self.degsigncompcb2, self.degsigncompcb3)
		degsigns = (self.degsigncomp1, self.degsigncomp2, self.degsigncomp3)
		degentries = (self.degcomp1entry, self.degcomp2entry, self.degcomp3entry)
		degs = (self.degcomp1, self.degcomp2, self.degcomp3)
		refcbs = (self.refcompcb1, self.refcompcb2, self.refcompcb3)
		refers = (self.refcomp1, self.refcomp2, self.refcomp3)

		self.name.set(name)
		lensigntxt = len(texts.signs2[0])

		for j in range(len(fs)):
			if (fs[j][0].isdigit()):#Degrees
				txt = fs[j][:]
				signtxt = txt[-lensigntxt:]
				sign = texts.signs2.index(signtxt) #index raises ValueError if string not found
				deg = int(txt[:-lensigntxt])
				cbs[j].set(texts.lotComponentList[LotsOptDlg.DE])
				degs[j].set(deg)
				degsigns[j].set(texts.signs[sign])
				degsigncbs[j].configure(state='readonly')
				degentries[j].configure(state='normal')
				refcbs[j].configure(state='disabled')
			elif (fs[j][0] == texts.txtslotsdlg['R']):#Reference
				lord = fs[j][-1] == LotsOptDlg.LORDTXT
				if (lord):
					cbs[j].set(texts.lotComponentList[LotsOptDlg.RELORD])
					refers[j].set(fs[j][1:-1])
				else:
					cbs[j].set(texts.lotComponentList[LotsOptDlg.RE])
					refers[j].set(fs[j][1:])

				degsigncbs[j].configure(state='disabled')
				degentries[j].configure(state='disabled')
				refcbs[j].configure(state='readonly')
			else:
				cbs[j].set(fs[j])
				degsigncbs[j].configure(state='disabled')
				degentries[j].configure(state='disabled')
				refcbs[j].configure(state='disabled')

		diurnal = val['values'][LotsOptDlg.DIURNAL]
		diur = False
		if (diurnal == LotsOptDlg.DIURNALTXT):
			diur = True
		self.diurnal.set(diur)


	def onCompCB1(self, event=None):
		self.compcb1.selection_clear()

		if (texts.lotComponentList.index(self.comp1.get()) == LotsOptDlg.DE):
			self.enableDeg1(True)
			self.enableDegSignCB1(True)
			self.enableRefCB1(False)
		elif (texts.lotComponentList.index(self.comp1.get()) == LotsOptDlg.RE or texts.lotComponentList.index(self.comp1.get()) == LotsOptDlg.RELORD):
			self.enableDeg1(False)
			self.enableDegSignCB1(False)
			if (len(self.refs) != 0):
				self.enableRefCB1(True)
			else:
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['NoRefs'])
				self.comp1.set(texts.lotComponentList[0])
		else:
			self.enableDeg1(False)
			self.enableDegSignCB1(False)
			self.enableRefCB1(False)


	def onCompCB2(self, event=None):
		self.compcb2.selection_clear()

		if (texts.lotComponentList.index(self.comp2.get()) == LotsOptDlg.DE):
			self.enableDeg2(True)
			self.enableDegSignCB2(True)
			self.enableRefCB2(False)
		elif (texts.lotComponentList.index(self.comp2.get()) == LotsOptDlg.RE or texts.lotComponentList.index(self.comp2.get()) == LotsOptDlg.RELORD):
			self.enableDeg2(False)
			self.enableDegSignCB2(False)
			if (len(self.refs) != 0):
				self.enableRefCB2(True)
			else:
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['NoRefs'])
				self.comp2.set(texts.lotComponentList[0])
		else:
			self.enableDeg2(False)
			self.enableDegSignCB2(False)
			self.enableRefCB2(False)


	def onCompCB3(self, event=None):
		self.compcb3.selection_clear()

		if (texts.lotComponentList.index(self.comp3.get()) == LotsOptDlg.DE):
			self.enableDeg3(True)
			self.enableDegSignCB3(True)
			self.enableRefCB3(False)
		elif (texts.lotComponentList.index(self.comp3.get()) == LotsOptDlg.RE or texts.lotComponentList.index(self.comp3.get()) == LotsOptDlg.RELORD):
			self.enableDeg3(False)
			self.enableDegSignCB3(False)
			if (len(self.refs) != 0):
				self.enableRefCB3(True)
			else:
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['NoRefs'])
				self.comp3.set(texts.lotComponentList[0])
		else:
			self.enableDeg3(False)
			self.enableDegSignCB3(False)
			self.enableRefCB3(False)


	def onRefCompCB1(self, event=None):
		self.refcompcb1.selection_clear()


	def onRefCompCB2(self, event=None):
		self.refcompcb2.selection_clear()


	def onRefCompCB3(self, event=None):
		self.refcompcb3.selection_clear()


	def onDegSignCompCB1(self, event=None):
		self.degsigncompcb1.selection_clear()


	def onDegSignCompCB2(self, event=None):
		self.degsigncompcb2.selection_clear()


	def onDegSignCompCB3(self, event=None):
		self.degsigncompcb3.selection_clear()


	def enableRefCB1(self, ena):
		txt = 'readonly'
		if (not ena):
			txt = 'disabled'
		self.refcompcb1.configure(state=txt)


	def enableRefCB2(self, ena):
		txt = 'readonly'
		if (not ena):
			txt = 'disabled'
		self.refcompcb2.configure(state=txt)


	def enableRefCB3(self, ena):
		txt = 'readonly'
		if (not ena):
			txt = 'disabled'
		self.refcompcb3.configure(state=txt)


	def enableDegSignCB1(self, ena):
		txt = 'readonly'
		if (not ena):
			txt = 'disabled'
		self.degsigncompcb1.configure(state=txt)


	def enableDegSignCB2(self, ena):
		txt = 'readonly'
		if (not ena):
			txt = 'disabled'
		self.degsigncompcb2.configure(state=txt)


	def enableDegSignCB3(self, ena):
		txt = 'readonly'
		if (not ena):
			txt = 'disabled'
		self.degsigncompcb3.configure(state=txt)


	def enableDeg1(self, ena):
		txt = 'normal'
		if (not ena):
			txt = 'disabled'
		self.degcomp1entry.configure(state=txt)


	def enableDeg2(self, ena):
		txt = 'normal'
		if (not ena):
			txt = 'disabled'
		self.degcomp2entry.configure(state=txt)


	def enableDeg3(self, ena):
		txt = 'normal'
		if (not ena):
			txt = 'disabled'
		self.degcomp3entry.configure(state=txt)


	def validateName(self, why):
		n = self.name.get()
		if ((len(n) >= 15) and (int(why) == 1)):
			return False

		return True


	def validateDegComp1(self, why):
		n = self.degcomp1.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateDegComp2(self, why):
		n = self.degcomp2.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateDegComp3(self, why):
		n = self.degcomp3.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def checkRefs(self):
		#is referred Lot refers to another one? (1-deep only)
		comp1txt = self.comp1.get()
		comp2txt = self.comp2.get()
		comp3txt = self.comp3.get()
		if (texts.lotComponentList.index(comp1txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp1txt) == LotsOptDlg.RELORD):
			ref1 = int(self.refcomp1.get())
			if (self.isReferring(ref1-1)):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['AlreadyReferring'])
				return False
		if (texts.lotComponentList.index(comp2txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp2txt) == LotsOptDlg.RELORD):
			ref2 = int(self.refcomp2.get())
			if (self.isReferring(ref2-1)):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['AlreadyReferring'])
				return False
		if (texts.lotComponentList.index(comp3txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp3txt) == LotsOptDlg.RELORD):
			ref3 = int(self.refcomp3.get())
			if (self.isReferring(ref3-1)):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['AlreadyReferring'])
				return False

		return True


	def onAddBtn(self):
		if (self.cnt >= LotsOptDlg.MAX_LOTS_NUM):
			messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['MaxLotsNum']+str(LotsOptDlg.MAX_LOTS_NUM))
			return

		if (not self.checkRefs()):
			return

		ok, nametxt, formulatxt, diurtxt = self.widgetsToTexts()
		if (not ok):
			return

		self.cnt += 1
		self.iids.append(self.tree.insert('', 'end', text=str(self.cnt)+'.', values=(nametxt, formulatxt, diurtxt)))
		self.refs.append(str(self.cnt))
		self.refcompcb1['values'] = self.refs
		self.refcomp1.set(self.refs[0])
		self.refcompcb2['values'] = self.refs
		self.refcomp2.set(self.refs[0])
		self.refcompcb3['values'] = self.refs
		self.refcomp3.set(self.refs[0])
		self.tree.selection_set(self.iids[len(self.iids)-1])
		self.tree.see(self.iids[len(self.iids)-1])	#ensure that the new item is visible

		self.changed = True


	def onModifyBtn(self):
		if (len(self.iids) == 0):
			return

		if (not self.checkRefs()):
			return

		ok, nametxt, formulatxt, diurtxt = self.widgetsToTexts()
		if (not ok):
			return

		sel = self.tree.selection()
		if (sel != ''):
			num = len(self.iids)
			for i in range(num):
				val = self.tree.item(self.iids[i])
				numtxt = val['text']
				numtxt = numtxt[0:-1]
				rownum = self.iids.index(sel[0])
				if (numtxt == str(rownum+1)):
					#is this lot referred to by another one?
					#check first the combos: is there Ref or RefLord?
					comp1txt = self.comp1.get()
					comp2txt = self.comp2.get()
					comp3txt = self.comp3.get()
					if (texts.lotComponentList.index(comp1txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp1txt) == LotsOptDlg.RELORD or texts.lotComponentList.index(comp2txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp2txt) == LotsOptDlg.RELORD or texts.lotComponentList.index(comp3txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp3txt) == LotsOptDlg.RELORD): 
						if (self.isReferred(i)):
							messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['AlreadyReferred'])
							return False

					self.tree.item(self.iids[i], values=(nametxt, formulatxt, diurtxt))
					self.changed = True
					break
		else:
			messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['NoSelection'])


	def widgetsToTexts(self):
		ok = True
		nametxt = self.name.get()
		if (nametxt == ''):
			messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['LotNameEmpty'])
			return False, '', '', ''

		num = len(self.iids)
		for i in range(num):
			val = self.tree.item(self.iids[i])
			if (val['values'][LotsOptDlg.NAME] == nametxt):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['LotAlreadyExists'])
				return False, '', '', ''

		comp1txt = self.comp1.get()
		comp2txt = self.comp2.get()
		comp3txt = self.comp3.get()

		if (texts.lotComponentList.index(comp1txt) == LotsOptDlg.DE):
			deg = int(self.degcomp1.get())
			if (deg > chart.Chart.SIGN_DEG-1):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['DegreeProblem']+' '+str(chart.Chart.SIGN_DEG))
				ok = False
			comp1txt = self.degcomp1.get()+texts.signs2[texts.signs.index(self.degsigncomp1.get())]
		elif (texts.lotComponentList.index(comp1txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp1txt) == LotsOptDlg.RELORD):
			t1 = texts.txtslotsdlg['R']+self.refcomp1.get()
			if (texts.lotComponentList.index(comp1txt) == LotsOptDlg.RELORD):
				t1 += LotsOptDlg.LORDTXT
			comp1txt = t1

		if (texts.lotComponentList.index(comp2txt) == LotsOptDlg.DE):
			deg = int(self.degcomp2.get())
			if (deg > chart.Chart.SIGN_DEG-1):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['DegreeProblem']+' '+str(chart.Chart.SIGN_DEG))
				ok = False
			comp2txt = self.degcomp2.get()+texts.signs2[texts.signs.index(self.degsigncomp2.get())]
		elif (texts.lotComponentList.index(comp2txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp2txt) == LotsOptDlg.RELORD):
			t2 = texts.txtslotsdlg['R']+self.refcomp2.get()
			if (texts.lotComponentList.index(comp2txt) == LotsOptDlg.RELORD):
				t2 += LotsOptDlg.LORDTXT
			comp2txt = t2

		if (texts.lotComponentList.index(comp3txt) == LotsOptDlg.DE):
			deg = int(self.degcomp3.get())
			if (deg > chart.Chart.SIGN_DEG-1):
				messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['DegreeProblem']+' '+str(chart.Chart.SIGN_DEG))
				ok = False
			comp3txt = self.degcomp3.get()+texts.signs2[texts.signs.index(self.degsigncomp3.get())]
		elif (texts.lotComponentList.index(comp3txt) == LotsOptDlg.RE or texts.lotComponentList.index(comp3txt) == LotsOptDlg.RELORD):
			t3 = texts.txtslotsdlg['R']+self.refcomp3.get()
			if (texts.lotComponentList.index(comp3txt) == LotsOptDlg.RELORD):
				t3 += LotsOptDlg.LORDTXT
			comp3txt = t3

		formulatxt = comp1txt+'+'+comp2txt+'-'+comp3txt

		diurtxt = ''
		if (self.diurnal.get()):
			diurtxt = LotsOptDlg.DIURNALTXT

		return ok, nametxt, formulatxt, diurtxt


	def onRemoveBtn(self):
		if (len(self.iids) == 0):
			return

		sel = self.tree.selection()
		if (sel != ''):
			ret = messagebox.askyesno(parent=self.win, message=texts.txtscommon['AreYouSure'], icon='question')
			if (ret):
				sel = self.tree.selection()
				if (sel != ''):
					linestodelete = []
					num = len(self.iids) 
					for w in range(num):
						val = self.tree.item(self.iids[w])
						numtxt = val['text']
						numtxt = numtxt[0:-1]
						rownum = self.iids.index(sel[0])
						if (numtxt == str(rownum+1)):
							linestodelete.append(w)
							linestodelete = self.isReferred(w, linestodelete)
							endnum = len(self.iids)
							#Update references
							for i in range(w+1, endnum):
								val = self.tree.item(self.iids[i])
								form = val['values'][LotsOptDlg.FORMULA]
								f1 = self.getFormula(form, 1)
								f2 = self.getFormula(form, 2)
								f3 = self.getFormula(form, 3)
								fs = [f1, f2, f3]
								ref = 0
	
								for j in range(len(fs)):
									if (fs[j][0] == texts.txtslotsdlg['R']):#Reference
										lord = fs[j][-1] == LotsOptDlg.LORDTXT
										if (lord):
											ref = int(fs[j][1:-1])
										else:
											ref = int(fs[j][1:])
	
										for k in range(len(linestodelete)):
											if (ref > linestodelete[k]+1):
												ref -= 1
			
												#Set updated reference
												fs[j] = texts.txtslotsdlg['R']+str(ref)
												if (lord):
													fs[j] += LotsOptDlg.LORDTXT

									formulatxt = fs[0]+'+'+fs[1]+'-'+fs[2]
									val = self.tree.item(self.iids[i])
									nametxt = val['values'][LotsOptDlg.NAME]
									diurtxt = val['values'][LotsOptDlg.DIURNAL]
									self.tree.item(self.iids[i], values=(nametxt, formulatxt, diurtxt))

							for l in range(len(linestodelete)):
								self.tree.delete(self.iids[linestodelete[l]])

							offs = 0
							for l in range(len(linestodelete)):
								del self.iids[linestodelete[l]-offs]
								offs += 1
	
							self.removeRefs(len(linestodelete))
	
							self.cnt = 0
							n = len(self.iids)
							for m in range(n):
								self.cnt += 1
								val = self.tree.item(self.iids[m])
								nametxt = val['values'][LotsOptDlg.NAME]
								formulatxt = val['values'][LotsOptDlg.FORMULA]
								diurtxt = val['values'][LotsOptDlg.DIURNAL]
								self.tree.item(self.iids[m], text=str(self.cnt)+'.', values=(nametxt, formulatxt, diurtxt))

							self.changed = True

							break
		else:
			messagebox.showinfo(parent=self.win, message=texts.txtslotsdlg['NoSelection'])


	def removeRefs(self, num):
		del self.refs[-num:]
		self.refcompcb1['values'] = self.refs
		if (len(self.refs) > 0):
			self.refcomp1.set(self.refs[0])


	def onRemoveAllBtn(self):
		if (len(self.iids) > 0):
			ret = messagebox.askyesno(parent=self.win, message=texts.txtscommon['AreYouSure'], icon='question')
			if (ret):
				num = len(self.iids) 
				for i in range(num):
					self.tree.delete(self.iids[i])
				del self.iids[:]

				self.cnt = 0
				self.changed = True


	def getFormula(self, txt, num):
		if (num == 1):
			idx = txt.find('+')
			f = txt[0:idx]
		elif (num == 2):
			idx = txt.find('+')
			idx2 = txt.find('-')
			f = txt[idx+1:idx2]
		else:
			idx = txt.find('-')
			f = txt[idx+1:]

		#remove whitespaces
		f = f.strip()
		return f


	def isReferred(self, num, lines=None):
		#Is num-th lot referred to by other lots?
		endnum = len(self.iids)
		for i in range(num+1, endnum):
			val = self.tree.item(self.iids[i])
			form = val['values'][LotsOptDlg.FORMULA]
			f1 = self.getFormula(form, 1)
			f2 = self.getFormula(form, 2)
			f3 = self.getFormula(form, 3)
			fs = [f1, f2, f3]
			ref = 0

			for j in range(len(fs)):
				if (fs[j][0] == texts.txtslotsdlg['R']):#Reference
					lord = fs[j][-1] == LotsOptDlg.LORDTXT
					if (lord):
						ref = int(fs[j][1:-1])
					else:
						ref = int(fs[j][1:])

					if (ref == num+1):
						if (lines == None):
							return True
						else:
							lines.append(i)
							break
		if (lines == None):
			return False

		return lines


	def isReferring(self, idx):
		val = self.tree.item(self.iids[idx])
		form = val['values'][LotsOptDlg.FORMULA]
		f1 = self.getFormula(form, 1)
		f2 = self.getFormula(form, 2)
		f3 = self.getFormula(form, 3)

		fs = [f1, f2, f3]
		for i in range(len(fs)):
			if (fs[i][0] == texts.txtslotsdlg['R']):#Reference
				return True

		return False


	def initialize(self, opts):
		NAMEOPT = 0
		FORMULAOPT = 1
		REFORDEGSOPT = 2
		DIURNALOPT = 3
		self.cnt = 0
		num = len(opts.lotsopts)
		for i in range(num):
			nametxt = opts.lotsopts[i][NAMEOPT]
			f1txt = f2txt = f3txt = ''
			if (opts.lotsopts[i][FORMULAOPT][0] == LotsOptDlg.DE):
				sign = int(opts.lotsopts[i][REFORDEGSOPT][0]/chart.Chart.SIGN_DEG)
				deg = int(opts.lotsopts[i][REFORDEGSOPT][0]%chart.Chart.SIGN_DEG)
				f1txt = str(deg)+texts.signs2[sign]
			elif (opts.lotsopts[i][FORMULAOPT][0] == LotsOptDlg.RE or opts.lotsopts[i][FORMULAOPT][0] == LotsOptDlg.RELORD):
				f1txt = texts.txtslotsdlg['R']+str(opts.lotsopts[i][REFORDEGSOPT][0])
				if (opts.lotsopts[i][FORMULAOPT][0] == LotsOptDlg.RELORD):
					f1txt += LotsOptDlg.LORDTXT
			else:
				f1txt = texts.lotComponentList[opts.lotsopts[i][FORMULAOPT][0]]

			if (opts.lotsopts[i][FORMULAOPT][1] == LotsOptDlg.DE):
				sign = int(opts.lotsopts[i][REFORDEGSOPT][1]/chart.Chart.SIGN_DEG)
				deg = int(opts.lotsopts[i][REFORDEGSOPT][1]%chart.Chart.SIGN_DEG)
				f2txt = str(deg)+texts.signs2[sign]
			elif (opts.lotsopts[i][FORMULAOPT][1] == LotsOptDlg.RE or opts.lotsopts[i][FORMULAOPT][1] == LotsOptDlg.RELORD):
				f2txt = texts.txtslotsdlg['R']+str(opts.lotsopts[i][REFORDEGSOPT][1])
				if (opts.lotsopts[i][FORMULAOPT][1] == LotsOptDlg.RELORD):
					f2txt += LotsOptDlg.LORDTXT
			else:
				f2txt = texts.lotComponentList[opts.lotsopts[i][FORMULAOPT][1]]

			if (opts.lotsopts[i][FORMULAOPT][2] == LotsOptDlg.DE):
				sign = int(opts.lotsopts[i][REFORDEGSOPT][2]/chart.Chart.SIGN_DEG)
				deg = int(opts.lotsopts[i][REFORDEGSOPT][2]%chart.Chart.SIGN_DEG)
				f3txt = str(deg)+texts.signs2[sign]
			elif (opts.lotsopts[i][FORMULAOPT][2] == LotsOptDlg.RE or opts.lotsopts[i][FORMULAOPT][2] == LotsOptDlg.RELORD):
				f3txt = texts.txtslotsdlg['R']+str(opts.lotsopts[i][REFORDEGSOPT][2])
				if (opts.lotsopts[i][FORMULAOPT][2] == LotsOptDlg.RELORD):
					f3txt += LotsOptDlg.LORDTXT
			else:
				f3txt = texts.lotComponentList[opts.lotsopts[i][FORMULAOPT][2]]

			formulatxt = f1txt+'+'+f2txt+'-'+f3txt

			diurnaltxt = ''
			if (opts.lotsopts[i][DIURNALOPT]):
				diurnaltxt = LotsOptDlg.DIURNALTXT
			self.cnt += 1
			self.iids.append(self.tree.insert('', 'end', text=str(self.cnt)+'.', values=(nametxt, formulatxt, diurnaltxt)))
			self.refs.append(str(self.cnt))

		if (num > 0):
			self.refcompcb1['values'] = self.refs
			self.refcomp1.set(self.refs[0])
			self.refcompcb2['values'] = self.refs
			self.refcomp2.set(self.refs[0])
			self.refcompcb3['values'] = self.refs
			self.refcomp3.set(self.refs[0])
			self.tree.selection_set(self.iids[0])
			self.fillWidgets(0)

		self.hcsigns.set(opts.hcmeanssigncusp)
		self.hcsignsasc.set(opts.ascissigncusp)
		if (not self.hcsigns.get()):
			self.hcsignsascbtn.configure(state='disabled')


	def copyData(self):
		if (self.changed):
			lensigntxt = len(texts.signs2[0])
			self.var_lots = []
			for i in range(len(self.iids)):
				val = self.tree.item(self.iids[i])
				name = val['values'][LotsOptDlg.NAME]
				form = val['values'][LotsOptDlg.FORMULA]
				f1 = self.getFormula(form, 1)
				f2 = self.getFormula(form, 2)
				f3 = self.getFormula(form, 3)
				fs = [f1, f2, f3]
				refordegs = [0, 0, 0]

				for j in range(len(fs)):
					if (fs[j][0].isdigit()):#Degrees
						txt = fs[j][:]
						signtxt = txt[-lensigntxt:]
						sign = texts.signs2.index(signtxt) #index raises ValueError if string not found

						deg = int(txt[:-lensigntxt])
						refordegs[j] = sign*chart.Chart.SIGN_DEG+deg
						fs[j] = LotsOptDlg.DE
					elif (fs[j][0] == texts.txtslotsdlg['R']):#Reference
						lord = fs[j][-1] == LotsOptDlg.LORDTXT
						if (lord):
							refordegs[j] = int(fs[j][1:-1])
						else:
							refordegs[j] = int(fs[j][1:])
						if (lord): 
							fs[j] = LotsOptDlg.RELORD
						else:
							fs[j] = LotsOptDlg.RE
					else:
						fs[j] = texts.lotComponentList.index(fs[j])

				diurnal = val['values'][LotsOptDlg.DIURNAL]
				diur = False
				if (diurnal == LotsOptDlg.DIURNALTXT):
					diur = True
				
				self.var_lots.append((name, (fs[0], fs[1], fs[2]), (refordegs[0], refordegs[1], refordegs[2]), diur))

		self.var_hcsigns = self.hcsigns.get()
		self.var_hcsignsasc = self.hcsignsasc.get()


	def check(self, opts):
		chnged = False

		#opts.lotsopts
		if (self.changed):
			del opts.lotsopts #[:]
			opts.lotsopts = copy.deepcopy(self.var_lots)
			chnged = True

		if (opts.hcmeanssigncusp != self.var_hcsigns):
			opts.hcmeanssigncusp = self.var_hcsigns
			chnged = True

		if (opts.ascissigncusp != self.var_hcsignsasc):
			opts.ascissigncusp = self.var_hcsignsasc
			chnged = True

		return chnged


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




