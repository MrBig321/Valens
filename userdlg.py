from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import texts


class UserDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsuserdlg['User'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#panel
		mpanel = ttk.LabelFrame(frame, text='')
		mpanel.grid(column=0, row=0, padx=UserDlg.PANELDISTX, pady=UserDlg.PANELDISTY, sticky=(W,N,S,E)) 
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['Longitude']+':')
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		#Longitude
			#Degree
		self.deg = StringVar()
		degcmd = mpanel.register(self.validateDeg)
		degentry = ttk.Entry(mpanel, textvariable=self.deg, width=4, validate='key', validatecommand=(degcmd, '%d'))
		degentry.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		self.deg.set('0')
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['D'])
		label.grid(column=2, row=0, padx=5, pady=5, sticky=(W))
			#Min
		self.min = StringVar()
		mincmd = mpanel.register(self.validateMin)
		minentry = ttk.Entry(mpanel, textvariable=self.min, width=3, validate='key', validatecommand=(mincmd, '%d'))
		minentry.grid(column=3, row=0, padx=5, pady=5, sticky=(W))
		self.min.set('0')
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['M'])
		label.grid(column=4, row=0, padx=5, pady=5, sticky=(W))
			#Sec
		self.sec = StringVar()
		seccmd = mpanel.register(self.validateSec)
		secentry = ttk.Entry(mpanel, textvariable=self.sec, width=3, validate='key', validatecommand=(seccmd, '%d'))
		secentry.grid(column=5, row=0, padx=5, pady=5, sticky=(W))
		self.sec.set('0')
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['S'])
		label.grid(column=6, row=0, padx=5, pady=5, sticky=(W))
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['Latitude']+':')
		label.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		#Latitude
			#Degree2
		self.deg2 = StringVar()
		deg2cmd = mpanel.register(self.validateDeg2)
		deg2entry = ttk.Entry(mpanel, textvariable=self.deg2, width=4, validate='key', validatecommand=(deg2cmd, '%d'))
		deg2entry.grid(column=1, row=1, padx=5, pady=5, sticky=(W))
		self.deg2.set('0')
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['D'])
		label.grid(column=2, row=1, padx=5, pady=5, sticky=(W))
			#Min2
		self.min2 = StringVar()
		min2cmd = mpanel.register(self.validateMin2)
		min2entry = ttk.Entry(mpanel, textvariable=self.min2, width=3, validate='key', validatecommand=(min2cmd, '%d'))
		min2entry.grid(column=3, row=1, padx=5, pady=5, sticky=(W))
		self.min2.set('0')
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['M'])
		label.grid(column=4, row=1, padx=5, pady=5, sticky=(W))
			#Sec2
		self.sec2 = StringVar()
		sec2cmd = mpanel.register(self.validateSec2)
		sec2entry = ttk.Entry(mpanel, textvariable=self.sec2, width=3, validate='key', validatecommand=(sec2cmd, '%d'))
		sec2entry.grid(column=5, row=1, padx=5, pady=5, sticky=(W))
		self.sec2.set('0')
		label = ttk.Label(mpanel, text=texts.txtsuserdlg['S'])
		label.grid(column=6, row=1, padx=5, pady=5, sticky=(W))
		#Southern
		self.southern = BooleanVar()
		self.southern.set(False)
		sbtn = ttk.Checkbutton(mpanel, text=texts.txtsuserdlg['Southern'], variable=self.southern, onvalue=True)
		sbtn.grid(column=1, row=2, columnspan=3, padx=5, pady=5, sticky=(W))


		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=3, padx=5, pady=5, sticky=(S,E))

		degentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def validateDeg(self, why):
		n = self.deg.get()
		if ((len(n) >= 3) and (int(why) == 1)):
			return False

		return True


	def validateMin(self, why):
		n = self.min.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSec(self, why):
		n = self.sec.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateDeg2(self, why):
		n = self.deg2.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateMin2(self, why):
		n = self.min2.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validateSec2(self, why):
		n = self.sec2.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validate(self):
		d = self.deg.get()
		m = self.min.get()
		s = self.sec.get()
		d2 = self.deg2.get()
		m2 = self.min2.get()
		s2 = self.sec2.get()

		if (d == '' or m == '' or s == '' or d2 == '' or m2 == '' or s2 == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(d)
			int(m)
			int(s)
			int(d2)
			int(m2)
			int(s2)
		except ValueError:
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumericFieldsDigits'])
			return False

		if (int(d) < 0 or int(d) > 359):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpEclLonDeg'])
			return False

		if (int(m) < 0 or int(m) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpArcMin'])
			return False

		if (int(s) < 0 or int(s) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpArcSec'])
			return False

		if (int(d2) < 0 or int(d2) > 89):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpLatDeg'])
			return False

		if (int(m2) < 0 or int(m2) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpArcMin'])
			return False

		if (int(s2) < 0 or int(s2) > 59):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['HelpArcSec'])
			return False

		return True


	def copyData(self):
		self.var_deg = int(self.deg.get())
		self.var_min = int(self.min.get())
		self.var_sec = int(self.sec.get())
		self.var_deg2 = int(self.deg2.get())
		self.var_min2 = int(self.min2.get())
		self.var_sec2 = int(self.sec2.get())
		self.var_southern = self.southern.get()


	def initialize(self, lon, lat, south):
		self.deg.set(str(lon[0]))
		self.min.set(str(lon[1]))
		self.sec.set(str(lon[2]))
		self.deg2.set(str(lat[0]))
		self.min2.set(str(lat[1]))
		self.sec2.set(str(lat[2]))
		self.southern.set(south)


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




