from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import chtime
import chart
import texts
import util


class ElectionStepperDlg:

	PANELDISTX = 2
	PANELDISTY = 2


	def __init__(self, parentdlg, parent, chrt, options):
		self.parent = parent
		self.parentdlg = parentdlg
		self.chart = chrt
		self.options = options

		self.win = Toplevel()
		self.win.title(texts.txtselectionstepperdlg['Elections'])
		self.win.parent = parent.win
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Panel
		panel = ttk.LabelFrame(frame, text='')
		panel.grid(column=0, row=0, padx=ElectionStepperDlg.PANELDISTX, pady=ElectionStepperDlg.PANELDISTY, sticky=(W,N,S,E)) 

		label = ttk.Label(panel, text=texts.txtselectionstepperdlg['Year'])
		label.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		btnIncYear = ttk.Button(panel, text='++', width=5,  command=self.onIncYear)
		btnIncYear.grid(column=1, row=0, padx=5, pady=0, sticky=(W))
		btnDecYear = ttk.Button(panel, text='--', width=5, command=self.onDecYear)
		btnDecYear.grid(column=2, row=0, padx=5, pady=0, sticky=(W))

		label = ttk.Label(panel, text=texts.txtselectionstepperdlg['Month'])
		label.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		btnIncMonth = ttk.Button(panel, text='++', width=5, command=self.onIncMonth)
		btnIncMonth.grid(column=1, row=1, padx=5, pady=0, sticky=(W))
		btnDecMonth = ttk.Button(panel, text='--', width=5, command=self.onDecMonth)
		btnDecMonth.grid(column=2, row=1, padx=5, pady=0, sticky=(W))

		label = ttk.Label(panel, text=texts.txtselectionstepperdlg['Day'])
		label.grid(column=0, row=2, padx=5, pady=0, sticky=(W))
		btnIncDay = ttk.Button(panel, text='++', width=5, command=self.onIncDay)
		btnIncDay.grid(column=1, row=2, padx=5, pady=0, sticky=(W))
		btnDecDay = ttk.Button(panel, text='--', width=5, command=self.onDecDay)
		btnDecDay.grid(column=2, row=2, padx=5, pady=0, sticky=(W))

		label = ttk.Label(panel, text=texts.txtselectionstepperdlg['Hour'])
		label.grid(column=0, row=3, padx=5, pady=0, sticky=(W))
		btnIncHour = ttk.Button(panel, text='++', width=5, command=self.onIncHour)
		btnIncHour.grid(column=1, row=3, padx=5, pady=0, sticky=(W))
		btnDecHour = ttk.Button(panel, text='--', width=5, command=self.onDecHour)
		btnDecHour.grid(column=2, row=3, padx=5, pady=0, sticky=(W))

		label = ttk.Label(panel, text=texts.txtselectionstepperdlg['Min'])
		label.grid(column=0, row=4, padx=5, pady=0, sticky=(W))
		btnIncMin = ttk.Button(panel, text='++', width=5, command=self.onIncMin)
		btnIncMin.grid(column=1, row=4, padx=5, pady=0, sticky=(W))
		btnDecMin = ttk.Button(panel, text='--', width=5, command=self.onDecMin)
		btnDecMin.grid(column=2, row=4, padx=5, pady=0, sticky=(W))

		label = ttk.Label(panel, text=texts.txtselectionstepperdlg['Sec'])
		label.grid(column=0, row=5, padx=5, pady=0, sticky=(W))
		btnIncSec = ttk.Button(panel, text='++', width=5, command=self.onIncSec)
		btnIncSec.grid(column=1, row=5, padx=5, pady=0, sticky=(W))
		btnDecSec = ttk.Button(panel, text='--', width=5, command=self.onDecSec)
		btnDecSec.grid(column=2, row=5, padx=5, pady=0, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=6, padx=5, pady=5, sticky=(S,E))

		btnIncYear.focus()

		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
		self.allright = False
		self.center()
		self.parent.setChild(self)


	def onIncYear(self):
		y = self.chart.time.origyear+1
		self.show(y, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onDecYear(self):
		y = self.chart.time.origyear-1
		self.show(y, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onIncMonth(self):
		y, m = util.incrMonth(self.chart.time.origyear, self.chart.time.origmonth)
		self.show(y, m, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onDecMonth(self):
		y, m = util.decrMonth(self.chart.time.origyear, self.chart.time.origmonth)
		self.show(y, m, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onIncDay(self):
		y, m, d = util.incrDay(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday)
		self.show(y, m, d, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onDecDay(self):
		y, m, d = util.decrDay(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday)
		self.show(y, m, d, self.chart.time.hour, self.chart.time.minute, self.chart.time.second)


	def onIncHour(self):
		y, m, d, h = util.addHour(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour)
		self.show(y, m, d, h, self.chart.time.minute, self.chart.time.second)


	def onDecHour(self):
		y, m, d, h = util.subtractHour(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour)
		self.show(y, m, d, h, self.chart.time.minute, self.chart.time.second)


	def onIncMin(self):
		y, m, d, h, mi = util.addMins(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, 1)
		self.show(y, m, d, h, mi, self.chart.time.second)


	def onDecMin(self):
		y, m, d, h, mi = util.subtractMins(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, 1)
		self.show(y, m, d, h, mi, self.chart.time.second)


	def onIncSec(self):
		y, m, d, h, mi, s = util.addSecs(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second, 1)
		self.show(y, m, d, h, mi, s)


	def onDecSec(self):
		y, m, d, h, mi, s = util.subtractSecs(self.chart.time.origyear, self.chart.time.origmonth, self.chart.time.origday, self.chart.time.hour, self.chart.time.minute, self.chart.time.second, 1)
		self.show(y, m, d, h, mi, s)


	def show(self, y, m, d, h, mi, s):
		time = chtime.Time(y, m, d, h, mi, s, self.chart.time.bc, self.chart.time.cal, self.chart.time.zt, self.chart.time.plus, self.chart.time.zh, self.chart.time.zm, self.chart.time.dst, self.chart.place)
		chrt = chart.Chart(self.chart.name, self.chart.male, chart.Chart.TRANSIT, time, self.chart.place, '', self.options, False)
		self.parentdlg.updateWnd(None, None, chrt)
		del self.chart
		self.chart = chrt


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




