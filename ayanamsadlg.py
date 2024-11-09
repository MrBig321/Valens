from tkinter import *
from tkinter import ttk
import texts


class AyanamsaDlg:

	def __init__(self, parent, opts):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtscommon['Ayanamsa'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		ayanpanel = ttk.LabelFrame(frame, text='')
		ayanpanel.grid(column=0, row=0, padx=2, pady=2, sticky=(W,N,S,E)) 
		self.ayan = StringVar()
		self.ayancombo = ttk.Combobox(ayanpanel, textvariable=self.ayan, width=20, state='readonly', values = texts.ayanamsaList)
		self.ayancombo.grid(column=0, row=0, padx=10, pady=20, sticky=(W))
		self.ayancombo.set(texts.ayanamsaList[opts.ayanamsa])
		self.ayancombo.bind('<<ComboboxSelected>>', self.onAyanamsaSelected)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onAyanamsaSelected(self, event=None):
		self.ayancombo.selection_clear()


	def copyData(self):
		self.ayanamsatxt = self.ayan.get()
		self.ayanamsa = 0
		num = len(texts.ayanamsaList)
		for i in range(num):
			if (self.ayanamsatxt == texts.ayanamsaList[i]):
				self.ayanamsa = i


	def check(self, opts):
		changed = False
		if (opts.ayanamsa != self.ayanamsa):
			opts.ayanamsa = self.ayanamsa
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







