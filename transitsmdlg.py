from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import planets
import rangechecker
import texts


class TransitsMDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtstransitsmdlg['Transits'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Date panel
		datepanel = ttk.LabelFrame(frame, text='')
		datepanel.grid(column=0, row=0, padx=TransitsMDlg.PANELDISTX, pady=TransitsMDlg.PANELDISTY, sticky=(W,N,S,E)) 
		#Year
		label = ttk.Label(datepanel, text=texts.txtstransitsmdlg['Year']+':')
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W,E))
		self.year = StringVar()
		yearcmd = datepanel.register(self.validateYear)
		yearentry = ttk.Entry(datepanel, textvariable=self.year, width=5, validate='key', validatecommand=(yearcmd, '%d'))
		yearentry.grid(column=0, row=1, padx=5, pady=5, sticky=(W,E))
		self.year.set('0')
		#Month
		label = ttk.Label(datepanel, text=texts.txtstransitsmdlg['Month']+':')
		label.grid(column=1, row=0, padx=5, pady=5, sticky=(W,E))
		self.month = StringVar()
		monthcmd = datepanel.register(self.validateMonth)
		monthentry = ttk.Entry(datepanel, textvariable=self.month, width=5, validate='key', validatecommand=(monthcmd, '%d'))
		monthentry.grid(column=1, row=1, padx=5, pady=5, sticky=(W,E))
		self.month.set('0')

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(S,E))

		yearentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


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


	def validate(self):
		y = self.year.get()
		m = self.month.get()

		if (y == '' or m == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(y)
			int(m)
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

		return True


	def initialize(self, y, m):
		self.year.set(str(y))
		self.month.set(str(m))


	def copyData(self):
		self.var_y = int(self.year.get())
		self.var_m = int(self.month.get())


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




