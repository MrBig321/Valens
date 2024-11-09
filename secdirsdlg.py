from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import texts


class SecDirsDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtssecdirdlg['SecondaryDirs'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Age Panel
		agepanel = ttk.LabelFrame(frame, text=texts.txtssecdirdlg['Age'])
		agepanel.grid(column=0, row=0, padx=SecDirsDlg.PANELDISTX, pady=SecDirsDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.age = StringVar()
		agecmd = agepanel.register(self.validateAge)
		ageentry = ttk.Entry(agepanel, textvariable=self.age, width=4, validate='key', validatecommand=(agecmd, '%d'))
		ageentry.grid(column=0, row=0, padx=5, pady=0, sticky=(W))
		self.age.set('0')
		ageentry.select_range(0,1)

		#Direction Panel
		dirpanel = ttk.LabelFrame(frame, text='')
		dirpanel.grid(column=1, row=0, padx=SecDirsDlg.PANELDISTX, pady=SecDirsDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.direct = StringVar()
		dirbtn = ttk.Radiobutton(dirpanel, text=texts.txtssecdirdlg['Direct'], variable=self.direct, value='direct')
		dirbtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		conbtn = ttk.Radiobutton(dirpanel, text=texts.txtssecdirdlg['Converse'], variable=self.direct, value='converse')
		conbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		self.direct.set('direct')

		#Time Panel
		timepanel = ttk.LabelFrame(frame, text='')
		timepanel.grid(column=0, row=1, columnspan=2, padx=SecDirsDlg.PANELDISTX, pady=SecDirsDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.soltime = StringVar()
		solbtn = ttk.Radiobutton(timepanel, text=texts.txtssecdirdlg['ApparentSolarTime'], variable=self.soltime, value='solar')
		solbtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		meanbtn = ttk.Radiobutton(timepanel, text=texts.txtssecdirdlg['MeanTime'], variable=self.soltime, value='mean')
		meanbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		self.soltime.set('solar')

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=2, padx=5, pady=5, sticky=(S,E))

		ageentry.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def validateAge(self, why):
		n = self.age.get()
		if ((len(n) >= 2) and (int(why) == 1)):
			return False

		return True


	def validate(self):
		age = self.age.get()

		if (age == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(age)
		except ValueError:
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumericFieldsDigits'])
			return False

		return True


	def copyData(self):
		self.var_age = int(self.age.get())
		if (self.direct.get() == 'direct'):
			self.var_direct = True
		else:
			self.var_direct = False
		if (self.soltime.get() == 'solar'):
			self.var_soltime = True
		else:
			self.var_soltime = False


	def initialize(self, age, direct, soltime):
		self.age.set(str(age))
		if (direct):
			self.direct.set('direct')
		else:
			self.direct.set('converse')
		if (soltime):
			self.soltime.set('solar')
		else:
			self.soltime.set('mean')


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




