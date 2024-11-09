from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import chtime
import chart
import secdir
import texts


class StepperDlg:

	PANELDISTX = 2
	PANELDISTY = 2


	def __init__(self, parentdlg, parent, chrt, age, direct, soltime, options):
		self.parent = parent
		self.parentdlg = parentdlg
		self.chart = chrt
		self.age = age
		if (not direct):
			self.age *= -1
#		self.direct = direct
		self.soltime = soltime
		self.options = options

		self.win = Toplevel()
		self.win.title(texts.txtsstepperdlg['SecondaryDirs'])
		self.win.parent = parent.win
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Days Panel
		dayspanel = ttk.LabelFrame(frame, text=texts.txtsstepperdlg['Days'])
		dayspanel.grid(column=0, row=0, padx=StepperDlg.PANELDISTX, pady=StepperDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.day = StringVar()
		daycmd = dayspanel.register(self.validateDay)
		dayentry = ttk.Entry(dayspanel, textvariable=self.day, width=4, validate='key', validatecommand=(daycmd, '%d'))
		dayentry.grid(column=0, row=0, padx=5, pady=5, sticky=(W,E))
		dayentry.configure(state='readonly')
		self.day.set(str(self.age))

		plusbtn = ttk.Button(dayspanel, text='++', command=self.onPlusBtn)
		plusbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		minusbtn = ttk.Button(dayspanel, text='--', command=self.onMinusBtn)
		minusbtn.grid(column=1, row=1, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(S,E))

		dayentry.focus()

		self.zt = chtime.Time.LOCALMEAN
		if (self.soltime):
			self.zt = chtime.Time.LOCALAPPARENT
		self.zh = 0
		self.zm = 0

		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
		self.allright = False
		self.center()
		self.parentdlg.setChild(self)


	def onPlusBtn(self):
		self.age += 1
		self.day.set(str(self.age))
		direct = True
		age = self.age
		if (self.age < 0):
			age *= -1
			direct = False
		sdir = secdir.SecDir(self.chart, age, direct, self.soltime)
		y, m, d, hour, minute, second = sdir.compute()

		time = chtime.Time(y, m, d, hour, minute, second, False, self.chart.time.cal, self.zt, self.chart.time.plus, self.zh, self.zm, False, self.chart.place)
		chrt = chart.Chart(self.chart.name, self.chart.male, chart.Chart.DIRECTION, time, self.chart.place, '', self.options, False)
		self.parentdlg.updateWnd(None, None, chrt)


	def onMinusBtn(self):
		self.age -= 1
		self.day.set(str(self.age))
		direct = True
		age = self.age
		if (self.age < 0):
			age *= -1
			direct = False
		sdir = secdir.SecDir(self.chart, age, direct, self.soltime)
		y, m, d, hour, minute, second = sdir.compute()

		time = chtime.Time(y, m, d, hour, minute, second, False, self.chart.time.cal, self.zt, self.chart.time.plus, self.zh, self.zm, False, self.chart.place)
		chrt = chart.Chart(self.chart.name, self.chart.male, chart.Chart.DIRECTION, time, self.chart.place, '', self.options, False)
		self.parentdlg.updateWnd(None, None, chrt)


	def validateDay(self, why):
		n = self.day.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def ok(self, event=None):
		self.destroy()


	def doModal(self):
		self.win.focus_set()
#		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def destroy(self):
		self.win.destroy()
		if (self.parentdlg != None):
			self.parentdlg.destroying(self)


	def center(self):
		self.win.withdraw()
		self.win.update_idletasks()
		sw = 512 #self.parent.win.winfo_screenwidth()
		sh = 512 #self.parent.win.winfo_screenheight()
		w = self.win.winfo_reqwidth()
		h = self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()




