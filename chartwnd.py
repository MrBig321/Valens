from tkinter import *
import hellenisticchart
import roundchart
import speculum1dlg
import speculum2dlg
import lots7dlg
import lots2dlg
import velocitydlg
import stepperdlg
import electionstepperdlg
import texts
#import pyscreenshot as ImageGrab # For Linux


class ChartWnd:
	XSIZE = 512
	YSIZE = 512


	def __init__(self, parent, titletxt, chrt, chrt2, opts, compare=False, invert=False, theother=False, wndparent=True):

		self.parent = parent
		self.chart = chrt
		self.options = opts
		self.chart2 = chrt2

		self.theother = theother
		self.wndparent = wndparent

		self.win = Toplevel()
		self.win.title(titletxt)
#		self.win.resizable(FALSE, FALSE)
		self.win.bind('<Destroy>', self.ok)
		self.win.minsize(300,300)

		self.firsttime = True
		self.prevw = ChartWnd.XSIZE
		self.prevh = ChartWnd.YSIZE

		#Popup-menu
		self.menu = Menu(self.win, tearoff=0)
		self.sel = StringVar()
		if (compare):
			self.sel.set('comparison')
		else:
			self.sel.set('chart')
		self.menusub = Menu(self.menu, tearoff=0)
		self.menusub.add_radiobutton(label=texts.txtspopupmenu['Chart'], variable=self.sel, value='chart', command=self.onChart)
		self.menusub.add_radiobutton(label=texts.txtspopupmenu['Comparison'], variable=self.sel, value='comparison', command=self.onComparison)
		self.menu.add_cascade(label=texts.txtspopupmenu['Windows'], menu=self.menusub)
		self.bw = BooleanVar()
		self.menu.add_checkbutton(label=texts.txtscommon['BW'], variable=self.bw, command=self.onBW, onvalue=True)
		if (not theother):
			self.menu.add_command(label=texts.menutxts['TMSpeculum1'], command=self.onSpeculum1)
			self.menu.add_command(label=texts.menutxts['TMSpeculum2'], command=self.onSpeculum2)
			self.menu.add_command(label=texts.menutxts['TMLots7'], command=self.onLots7)
			self.menu.add_command(label=texts.menutxts['TMLots2'], command=self.onLots2)
			self.menu.add_command(label=texts.menutxts['TMVelocity'], command=self.onVelocity)
			self.menu.add_command(label=texts.menutxts['CMTheOther'], command=self.onTheOther)
		self.menu.add_command(label=texts.txtscommon['Print'], command=self.onPrint, accelerator="Ctrl+P") 
		self.win.bind('<Button-3>', self.onMenu)

		self.win.bind('<Button-1>', self.onLeftClick)
		self.win.bind_all("<Control-p>", self.onPrint)

		if (not invert):
			if (self.options.hellenistic):
				self.hchart = hellenisticchart.HellenisticChart(self.win, self.chart2, self.options, (ChartWnd.XSIZE, ChartWnd.YSIZE))
			else:
				self.hchart = roundchart.RoundChart(self.win, self.chart2, self.options, (ChartWnd.XSIZE, ChartWnd.YSIZE))
		else:
			if (not self.options.hellenistic):
				self.hchart = hellenisticchart.HellenisticChart(self.win, self.chart2, self.options, (ChartWnd.XSIZE, ChartWnd.YSIZE))
			else:
				self.hchart = roundchart.RoundChart(self.win, self.chart2, self.options, (ChartWnd.XSIZE, ChartWnd.YSIZE))

		self.hchart.can.pack(fill=BOTH, expand=1)

		self.win.bind('<Configure>', self.onResize)
		self.center() ##

		self.chldren = []
		self.closing = False


	def onLeftClick(self, event=None):
		self.menu.unpost()


	def onBW(self, event=None):
		self.hchart.bw = self.bw.get()
		if (self.sel.get() == 'chart'):
			self.hchart.drawCanvas(self.chart2, self.options, (self.prevw, self.prevh))
		else:
			self.hchart.drawCanvas(self.chart, self.options, (self.prevw, self.prevh), self.chart2)


	def onSpeculum1(self, event=None):
		dlg = self.getChild(speculum1dlg.Speculum1Dlg)
		if (dlg == None):
			dlg = speculum1dlg.Speculum1Dlg(self, self.win, self.chart2, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onSpeculum2(self, event=None):
		dlg = self.getChild(speculum2dlg.Speculum2Dlg)
		if (dlg == None):
			dlg = speculum2dlg.Speculum2Dlg(self, self.win, self.chart2, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onLots7(self, event=None):
		dlg = self.getChild(lots7dlg.Lots7Dlg)
		if (dlg == None):
			dlg = lots7dlg.Lots7Dlg(self, self.win, self.chart2, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onLots2(self, event=None):
		dlg = self.getChild(lots2dlg.Lots2Dlg)
		if (dlg == None):
			dlg = lots2dlg.Lots2Dlg(self, self.win, self.chart2, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onVelocity(self, event=None):
		dlg = self.getChild(velocitydlg.VelocityDlg)
		if (dlg == None):
			dlg = velocitydlg.VelocityDlg(self, self.win, self.chart2, self.options)
			self.chldren.append(dlg)
			dlg.doModal()
		else: dlg.win.lift()


	def onTheOther(self, event=None):
		wnd = self.getChild(ChartWnd)
		if (wnd == None):
			otherwnd = ChartWnd(self, '', self.chart, self.chart2, self.options, False, True, True, False)
			self.chldren.append(otherwnd)
			otherwnd.show()
		else: wnd.win.lift()


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


	def onChart(self, event=None):
		self.hchart.bw = self.bw.get()
		self.hchart.drawCanvas(self.chart2, self.options, (self.prevw, self.prevh))


	def onComparison(self, event=None):
		self.hchart.bw = self.bw.get()
		self.hchart.drawCanvas(self.chart, self.options, (self.prevw, self.prevh), self.chart2)


	def onMenu(self, event=None):
		self.menu.post(event.x_root, event.y_root)


	def onResize(self, event):
		self.win.update_idletasks()
		w = self.win.winfo_width()
		h = self.win.winfo_height()
		if (self.firsttime or w != self.prevw or h != self.prevh):
			self.firsttime = False
			if (self.sel.get() == 'chart'):
				self.hchart.drawCanvas(self.chart2, self.options, (w, h))
			else:
				self.hchart.drawCanvas(self.chart, self.options, (w, h), self.chart2)
			self.prevw = w
			self.prevh = h


	def getChild(self, cl):
		num = len(self.chldren)
		for i in range(num):
			if (isinstance(self.chldren[i], cl)):
				return self.chldren[i]

		return None


	def updateWnd(self, chrt, opts, chrt2=None):
		if (chrt != None):
			self.chart = chrt
		if (chrt2 != None):
			self.chart2 = chrt2
		if (opts != None):
			self.options = opts
		#redraw this wnd
		if (self.sel.get() == 'chart'):
			self.hchart.drawCanvas(self.chart2, self.options, (self.prevw, self.prevh))
		else:
			self.hchart.drawCanvas(self.chart, self.options, (self.prevw, self.prevh), self.chart2)

		if (not self.theother):
			#redraw chldren
			num = len(self.chldren)
			for i in range(num):
				if (not isinstance(self.chldren[i], (stepperdlg.StepperDlg, electionstepperdlg.ElectionStepperDlg))):
					self.chldren[i].updateWnd(chrt, opts, chrt2)


	def destroying(self, obj):
		if (not self.closing):
			num = len(self.chldren)
			for i in range(num):
				if (self.chldren[i] == obj):
					del self.chldren[i]
					break


	#From stepper dialogs
	def setChild(self, ptr):
		self.chldren.append(ptr)


	def ok(self, event=None):
		self.closing = True
		num = len(self.chldren)
		for i in range(num):
			self.chldren[i].destroy()

		self.destroy()


	def show(self):
		self.win.focus_set()
		self.win.transient()						# stay on top
#		self.win.wait_window(self.win)				# display and wait
		self.win.wait_visibility()				# display and wait (in ChartStepperWnd)


	def destroy(self):
		self.win.destroy()
		if (self.parent != None):
			self.parent.destroying(self)


	def center(self):
		self.win.withdraw()
		self.win.update_idletasks()
		sw = sh = 0
		if (self.wndparent):
			sw = self.parent.winfo_screenwidth()
			sh = self.parent.winfo_screenheight()
		else:
			sw = self.parent.win.winfo_screenwidth()
			sh = self.parent.win.winfo_screenheight()

		w = ChartWnd.XSIZE #self.win.winfo_reqwidth()
		h = ChartWnd.YSIZE #self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()








