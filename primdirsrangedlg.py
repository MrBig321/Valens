from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import queue
import primdirs
import placidiansapd
import texts


class AbortFindTime:
	def __init__(self):
		self.init()

	def aborting(self):
		self.abort = True

	def setReady(self):
		self.ready = True

	def init(self):
		self.abort = False
		self.ready = False

	def isAborting(self):
		return self.abort

	def isReady(self):
		return self.ready


class PrimDirsRangeDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	FIRSTQUATER = 0
	SECONDQUATER = 1
	THIRDQUATER = 2
	FOURTHQUATER = 3
	ALL = 4

	DIRECT = 0
	CONVERSE = 1
	BOTH = 2

	arr = ['0', '25', '50', '75', 'all']
	dirarr = ['direct', 'converse', 'both']

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsprimdirsrangedlg['PrimaryDirs'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		self.abort = AbortFindTime()
		self.theend = False
		self.pds = []

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

#		frame.columnconfigure(1, weight=1) #column 1 will expand

		#Age Panel
		agepanel = ttk.LabelFrame(frame, text=texts.txtsprimdirsrangedlg['Age'])
		agepanel.grid(column=0, row=0, padx=PrimDirsRangeDlg.PANELDISTX, pady=PrimDirsRangeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.age = StringVar()
		age0btn = ttk.Radiobutton(agepanel, text='0-25', variable=self.age, value=PrimDirsRangeDlg.arr[PrimDirsRangeDlg.FIRSTQUATER])
		age0btn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		age1btn = ttk.Radiobutton(agepanel, text='25-50', variable=self.age, value=PrimDirsRangeDlg.arr[PrimDirsRangeDlg.SECONDQUATER])
		age1btn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		age2btn = ttk.Radiobutton(agepanel, text='50-75', variable=self.age, value=PrimDirsRangeDlg.arr[PrimDirsRangeDlg.THIRDQUATER])
		age2btn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		age3btn = ttk.Radiobutton(agepanel, text='75-100', variable=self.age, value=PrimDirsRangeDlg.arr[PrimDirsRangeDlg.FOURTHQUATER])
		age3btn.grid(column=0, row=3, padx=5, pady=5, sticky=(W))
		age4btn = ttk.Radiobutton(agepanel, text='0-100', variable=self.age, value=PrimDirsRangeDlg.arr[PrimDirsRangeDlg.ALL])
		age4btn.grid(column=0, row=4, padx=5, pady=5, sticky=(W))
		self.age.set('0')

		#Direction
		dirpanel = ttk.LabelFrame(frame, text='')
		dirpanel.grid(column=1, row=0, padx=PrimDirsRangeDlg.PANELDISTX, pady=PrimDirsRangeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.direct = StringVar()
		dirbtn = ttk.Radiobutton(dirpanel, text=texts.txtsprimdirsrangedlg['Direct'], variable=self.direct, value=PrimDirsRangeDlg.dirarr[PrimDirsRangeDlg.DIRECT])
		dirbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		conbtn = ttk.Radiobutton(dirpanel, text=texts.txtsprimdirsrangedlg['Converse'], variable=self.direct, value=PrimDirsRangeDlg.dirarr[PrimDirsRangeDlg.CONVERSE])
		conbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		bothbtn = ttk.Radiobutton(dirpanel, text=texts.txtsprimdirsrangedlg['Both'], variable=self.direct, value=PrimDirsRangeDlg.dirarr[PrimDirsRangeDlg.BOTH])
		bothbtn.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.direct.set('direct')

		#Prog Panel
		progpanel = ttk.LabelFrame(frame, text='')
		progpanel.grid(column=0, row=1, columnspan=2, padx=PrimDirsRangeDlg.PANELDISTX, pady=PrimDirsRangeDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.progbar = ttk.Progressbar(progpanel, mode='indeterminate', orient='horizontal', length=100)#, maximum=6000)
		self.progbar.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky=(W,E))
		self.startbtn = ttk.Button(progpanel, width=10, text=texts.txtsprimdirsrangedlg['Start'], command=self.onStartBtn)
		self.startbtn.grid(column=0, row=1, padx=5, pady=5, sticky=(W,E))
		self.stopbtn = ttk.Button(progpanel, width=10, text=texts.txtsprimdirsrangedlg['Stop'], command=self.onStopBtn)
		self.stopbtn.grid(column=1, row=1, padx=5, pady=5, sticky=(W,E))

		self.stopbtn.configure(state='disabled')

		okpanel = ttk.Frame(frame)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		cancelbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=2, padx=5, pady=5, sticky=(S,E))

		age0btn.focus()
		self.win.bind('<Return>', self.cancel)
		self.allright = False
		self.center()


	def onStopBtn(self, event=None):
		self.abort.aborting()
		self.progbar.stop()
		self.startbtn.configure(state='normal')
		self.stopbtn.configure(state='disabled')


	def onStartBtn(self, event=None):
		del self.pds[:]
		self.startbtn.configure(state='disabled')
		self.stopbtn.configure(state='normal')
		self.abort.init()
		self.progbar.start()
		self.queuepd = queue.Queue()
		threadID = placidiansapd.PlacidianSAPD(self.chart, self.options, PrimDirsRangeDlg.arr.index(self.age.get()), PrimDirsRangeDlg.dirarr.index(self.direct.get()), self.abort, self.queuepd).start()
		self.parent.after(100, self.processQueue)
#		self.queuepd.join()			# wait for taskdone


	def qsort(self, L):
		if L == []: return []
		return self.qsort([x for x in L[1:] if x.time < L[0].time]) + L[0:1] + self.qsort([x for x in L[1:] if x.time >= L[0].time])


	def processQueue(self):
		while (not self.queuepd.empty() or self.abort.isAborting()):
			pd = self.queuepd.get(0)
			self.queuepd.task_done()
			self.pds.append(pd)

		if (not self.theend):
			if (self.abort.isAborting() or self.abort.isReady()):
				self.progbar.stop()
				self.startbtn.configure(state='normal')
				self.stopbtn.configure(state='disabled')
				if (self.abort.isReady()):
					self.pds = self.qsort(self.pds)
					self.cancel()
					return
			else:
				self.parent.after(100, self.processQueue)


	def initialize(self, age, direct):
		self.age.set(PrimDirsRangeDlg.arr[age])
		self.direct.set(PrimDirsRangeDlg.dirarr[direct])


	def cancel(self, event=None):
		self.theend = True
		self.abort.aborting()
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




