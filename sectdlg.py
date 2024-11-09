from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import texts


class SectDlg:

	PANELDISTX = 2
	PANELDISTY = 2


	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtssectdlg['Sect'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Diurnal/Nocturnal Panel
		dnpanel = ttk.LabelFrame(frame, text=texts.txtssectdlg['DiurnalNocturnal'])
		dnpanel.grid(column=0, row=0, padx=SectDlg.PANELDISTX, pady=SectDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.ecl = StringVar()
		ebtn = ttk.Radiobutton(dnpanel, text=texts.txtssectdlg['Ecliptic'], variable=self.ecl, value='ecl')
		ebtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		sbtn = ttk.Radiobutton(dnpanel, text=texts.txtssectdlg['Semiarc'], variable=self.ecl, value='sem')
		sbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		#Orb
		orbpanel = ttk.LabelFrame(frame, text=texts.txtssectdlg['Orb'])
		orbpanel.grid(column=0, row=1, padx=SectDlg.PANELDISTX, pady=SectDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.use = BooleanVar()
		self.use.set(False)
		usebtn = ttk.Checkbutton(orbpanel, text=texts.txtssectdlg['Use'], variable=self.use, command=self.onUse, onvalue=True)
		usebtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.orb = StringVar()
		orbcmd = orbpanel.register(self.validateOrb)
		self.orbentry = ttk.Entry(orbpanel, textvariable=self.orb, width=3, validate='key', validatecommand=(orbcmd, '%d'))
		self.orbentry.grid(column=1, row=0, padx=5, pady=0, sticky=(W))
		self.orb.set('0')
		ptpanel = ttk.LabelFrame(frame, text=texts.txtssectdlg['Ptolemy'])
		ptpanel.grid(column=0, row=2, padx=SectDlg.PANELDISTX, pady=SectDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.alwaysd = BooleanVar()
		self.alwaysd.set(False)
		alwaysdbtn = ttk.Checkbutton(ptpanel, text=texts.txtssectdlg['AlwaysDiurnal'], variable=self.alwaysd, onvalue=True)
		alwaysdbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=3, padx=5, pady=5, sticky=(S,E))

		ebtn.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onUse(self):
		if (self.use.get()):
			self.orbentry.configure(state='normal')
		else:
			self.orbentry.configure(state='disabled')


	def validateOrb(self, why):
		n = self.orb.get()
		if ((len(n) >= 1) and (int(why) == 1)):
			return False

		return True


	def initialize(self, opts):
		if (opts.sectecl):
			self.ecl.set('ecl')
		else:
			self.ecl.set('sem')
		self.use.set(opts.sectuseorb)
		self.orb.set(str(opts.sectorb))
		if (not opts.sectuseorb):
			self.orbentry.configure(state='disabled')
		self.alwaysd.set(opts.sectptolemy)


	def validate(self):
		orb = self.orb.get()

		if (orb == ''):
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
			return False

		try:
			int(orb)
		except ValueError:
			messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumericFieldsDigits'])
			return False

		return True


	def copyData(self):
		self.var_ecl = self.ecl.get()
		if (self.var_ecl == 'ecl'):
			self.var_ecl = True
		else:
			self.var_ecl = False
		self.var_use = self.use.get()
		self.var_orb = int(self.orb.get())
		self.var_ptolemy = self.alwaysd.get()


	def check(self, opts):
		changed = False
		
		if (opts.sectecl != self.var_ecl):
			opts.sectecl = self.var_ecl
			changed = True

		if (opts.sectuseorb != self.var_use):
			opts.sectuseorb = self.var_use
			changed = True

		if (opts.sectorb != self.var_orb):
			opts.sectorb = self.var_orb
			changed = True

		if (opts.sectptolemy != self.var_ptolemy):
			opts.sectptolemy = self.var_ptolemy
			changed = True

		return changed


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





