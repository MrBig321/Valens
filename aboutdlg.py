from tkinter import *
from tkinter import ttk
import texts


class AboutDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtscommon['About'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Panel
		apanel = ttk.LabelFrame(frame, text='')#texts.txtsrevolutionsdlg['Planets'])
		apanel.grid(column=0, row=0, padx=AboutDlg.PANELDISTX, pady=AboutDlg.PANELDISTY, sticky=(W,N,S,E)) 
		label = ttk.Label(apanel, text=texts.licensetxt)
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=1, padx=5, pady=5, sticky=(S,E))

		self.win.bind('<Return>', self.ok)
		self.center()


	def ok(self, event=None):
		self.destroy()


	def doModal(self):
		self.win.focus_set()
#		self.win.grab_set()							# events go only to this wnd
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




