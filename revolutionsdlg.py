from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import planets
import rangechecker
import util
import texts


class RevolutionsDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsrevolutionsdlg['Revolutions'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Planets Panel
		plspanel = ttk.LabelFrame(frame, text='')#texts.txtsrevolutionsdlg['Planets'])
		plspanel.grid(column=0, row=0, padx=RevolutionsDlg.PANELDISTX, pady=RevolutionsDlg.PANELDISTY, sticky=(W,N,S,E)) 
			#Combo
		self.pl = StringVar()
		self.plcombo = ttk.Combobox(plspanel, textvariable=self.pl, width=10, state='readonly', values = texts.planets2)
		self.plcombo.grid(column=1, row=2, padx=5, pady=5, sticky=(W))
		self.pl.set(texts.planets2[planets.Planets.SUN])
		self.plcombo.bind('<<ComboboxSelected>>', self.plSelected)
		#Date panel
		datepanel = ttk.LabelFrame(frame, text='')#texts.txtsrevolutionsdlg['Revolutions'])
		datepanel.grid(column=1, row=0, padx=RevolutionsDlg.PANELDISTX, pady=RevolutionsDlg.PANELDISTY, sticky=(W,N,S,E)) 
			#StartingDate
		label = ttk.Label(datepanel, text=texts.txtsrevolutionsdlg['StartingDate']+':')
		label.grid(column=0, row=0, columnspan=3, padx=5, pady=0, sticky=(W))
			#Year
		yearpanel = ttk.Frame(datepanel)
		yearpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(W))		#This adds to datepanel-grid
		yearlabel = ttk.Label(yearpanel, text=texts.txtsrevolutionsdlg['Year']+':')
		yearlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.year = StringVar()
		yearcmd = plspanel.register(self.validateYear)
		yearentry = ttk.Entry(yearpanel, textvariable=self.year, width=5, validate='key', validatecommand=(yearcmd, '%d'))
		yearentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.year.set('')
			#Month
		monthpanel = ttk.Frame(datepanel)
		monthpanel.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		monthlabel = ttk.Label(monthpanel, text=texts.txtsrevolutionsdlg['Month']+':')
		monthlabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.month = StringVar()
		monthcmd = plspanel.register(self.validateMonth)
		monthentry = ttk.Entry(monthpanel, textvariable=self.month, width=3, validate='key', validatecommand=(monthcmd, '%d'))
		monthentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.month.set('')
			#Day
		daypanel = ttk.Frame(datepanel)
		daypanel.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
		daylabel = ttk.Label(daypanel, text=texts.txtsrevolutionsdlg['Day']+':')
		daylabel.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.day = StringVar()
		daycmd = plspanel.register(self.validateDay)
		dayentry = ttk.Entry(daypanel, textvariable=self.day, width=3, validate='key', validatecommand=(daycmd, '%d'))
		dayentry.grid(column=0, row=1, padx=5, pady=0, sticky=(W))
		self.day.set('')

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=1, padx=5, pady=5, sticky=(S,E))

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


	def validateDay(self, why):
		n = self.day.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def plSelected(self, event=None):
		self.plcombo.selection_clear()


	def validate(self):
		y = self.year.get()
		m = self.month.get()
		d = self.day.get()

		if (y == '' or m == '' or d == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(y)
			int(m)
			int(d)
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

		if (not util.checkDate(int(y), int(m), int(d))):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['InvalidDate'])
			return False

		return True


	def initialize(self, pl, y, m, d):
		self.pl.set(texts.planets2[pl])

		self.year.set(str(y))
		self.month.set(str(m))
		self.day.set(str(d))


	def copyData(self):
		self.var_pl = self.pl.get()
		self.var_pl = texts.planets2.index(self.var_pl)

		self.var_y = int(self.year.get())
		self.var_m = int(self.month.get())
		self.var_d = int(self.day.get())


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




