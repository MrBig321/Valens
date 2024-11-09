from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import datetime
import placesdlg
import rangechecker
import texts
import util


class EphemerisDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsgraphephemdlg['Ephemeris'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Year Panel
		yearpanel = ttk.LabelFrame(frame, text=texts.txtsgraphephemdlg['Year'])
		yearpanel.grid(column=0, row=0, padx=EphemerisDlg.PANELDISTX, pady=EphemerisDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.year = StringVar()
		yearcmd = yearpanel.register(self.validateYear)
		yearentry = ttk.Entry(yearpanel, textvariable=self.year, width=6, validate='key', validatecommand=(yearcmd, '%d'))
		yearentry.grid(column=0, row=0, padx=70, pady=10)#, sticky=(W, E))
		now = datetime.datetime.now()
		self.year.set(str(now.year))

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


	def validate(self):
		year = self.year.get()

		if (year == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(year)
		except ValueError:
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumericFieldsDigits'])
			return False

		checker = rangechecker.RangeChecker()
		if (int(year) > checker.epherange): #>= !?
			if (checker.isExtended()):
				messagebox.showerror(parent=self.win, message=texts.txtsvalidators['SwissEphem'])
			else:
				messagebox.showerror(parent=self.win, message=texts.txtsvalidators['MoshierEphem'])
			return False

		return True


	def copyData(self):
		self.var_year = int(self.year.get())


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
#		self.win.grab_set()							# events go only to this wnd
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





