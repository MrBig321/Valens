from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import texts


class ZodRelOptDlg:

	PANELDISTX = 2
	PANELDISTY = 2


	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtszodreloptdlg['ZodRel'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Calendar Panel
		calpanel = ttk.LabelFrame(frame, text=texts.txtszodreloptdlg['Calendar'])
		calpanel.grid(column=0, row=0, padx=ZodRelOptDlg.PANELDISTX, pady=ZodRelOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.cal = StringVar()
		egybtn = ttk.Radiobutton(calpanel, text=texts.txtszodreloptdlg['Egyptian'], variable=self.cal, value='egy')
		egybtn.grid(column=0, row=0, padx=5, pady=2, sticky=(W))
		modbtn = ttk.Radiobutton(calpanel, text=texts.txtszodreloptdlg['Modern'], variable=self.cal, value='mod')
		modbtn.grid(column=0, row=1, padx=5, pady=2, sticky=(W))
		#Planetary Periods Panel
		pppanel = ttk.LabelFrame(frame, text='')
		pppanel.grid(column=0, row=1, padx=ZodRelOptDlg.PANELDISTX, pady=ZodRelOptDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.cap = BooleanVar()
		self.cap.set(False)
		capbtn = ttk.Checkbutton(pppanel, text=texts.txtszodreloptdlg['Cap27'], variable=self.cap, onvalue=True)
		capbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=3, padx=5, pady=5, sticky=(S,E))

		egybtn.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def initialize(self, opts):
		if (opts.zregyptian):
			self.cal.set('egy')
		else:
			self.cal.set('mod')
		self.cap.set(opts.zr27cap)


	def copyData(self):
		self.var_egy = self.cal.get()
		if (self.var_egy == 'egy'):
			self.var_egy = True
		else:
			self.var_egy = False
		self.var_cap = self.cap.get()


	def check(self, opts):
		changed = False
		
		if (opts.zregyptian != self.var_egy):
			opts.zregyptian = self.var_egy
			changed = True

		if (opts.zr27cap != self.var_cap):
			opts.zr27cap = self.var_cap
			changed = True

		return changed


	def ok(self, event=None):
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





