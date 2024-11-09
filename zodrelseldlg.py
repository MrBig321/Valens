from tkinter import *
from tkinter import ttk
import houses
import texts
import util


class ZodRelSelDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtszodrelseldlg['ZodRel'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Signs Panel
		signspanel = ttk.LabelFrame(frame, text='')
		signspanel.grid(column=0, row=0, padx=ZodRelSelDlg.PANELDISTX, pady=ZodRelSelDlg.PANELDISTY, sticky=(W,N,S,E)) 
		label = ttk.Label(signspanel, text=texts.txtszodrelseldlg['StartRelFrom']+':')
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
			#Combo
		self.sel = StringVar()
		self.sicombo = ttk.Combobox(signspanel, textvariable=self.sel, width=10, state='readonly', values = texts.signs)
		self.sicombo.grid(column=0, row=1, padx=5, pady=5, sticky=(W,E))
		self.sel.set(texts.signs[0])
		self.sicombo.bind('<<ComboboxSelected>>', self.onSelected)

		#GeneralPeriod Panel
		genpanel = ttk.LabelFrame(frame, text=texts.txtszodrelseldlg['GeneralPeriod'])
		genpanel.grid(column=0, row=2, padx=ZodRelSelDlg.PANELDISTX, pady=ZodRelSelDlg.PANELDISTY, sticky=(W,N,S,E)) 
		initval = 6
		self.txtvar = StringVar()
		self.txtvar.set(texts.txtszodrelseldlg['Value']+': '+str(initval).zfill(3))
		scalelabel = ttk.Label(genpanel, textvariable=self.txtvar)
		scalelabel.grid(column=0, row=0, columnspan=2, padx=5, pady=5)
		self.scalevar = IntVar()
		self.scalevar.set(initval)
		scale = ttk.Scale(genpanel, orient=HORIZONTAL, from_=1, to=100, length=200, variable=self.scalevar, command=self.onScale)
		scale.grid(column=0, row=1, columnspan=4, padx=5, pady=5, sticky=(E, W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=3, padx=5, pady=5, sticky=(S,E))

		self.sicombo.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onScale(self, event=None):
		self.txtvar.set(texts.txtszodrelseldlg['Value']+': '+(str(self.scalevar.get())).zfill(3))


	def onSelected(self, event=None):
		self.sicombo.selection_clear()


	def copyData(self):
		self.var_sel = texts.signs.index(self.sel.get())
		self.var_sca = self.scalevar.get()


	def ok(self, event=None):
		self.copyData()
		self.allright = True
		self.destroy()


	def cancel(self):
		self.allright = False
		self.destroy()


	def doModal(self):
		self.win.focus_set()
		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


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






