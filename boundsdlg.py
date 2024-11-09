import copy
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import chart
import rangechecker
import placesdlg
import texts
import util


class BoundsDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent, opts):

		self.parent = parent
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsboundsdlg['Bounds'])
		self.win.resizable(FALSE, FALSE)

		# storage of vars of widgets
		self.bounds = [[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]],
					[[None, None], [None, None], [None, None], [None, None], [None, None]]]

		self.boundsval = copy.deepcopy(opts.bounds)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#Selection Panel
		selpanel = ttk.LabelFrame(frame, text='') #texts.txtsboundsdlg[''])
		selpanel.grid(column=0, row=0, padx=BoundsDlg.PANELDISTX, pady=BoundsDlg.PANELDISTY, sticky=(W, E))
		self.sel = StringVar()
		self.selcombo = ttk.Combobox(selpanel, textvariable=self.sel, width=20, state='readonly', values=texts.boundsList)
		self.selcombo.grid(column=0, row=0, columnspan=2, padx=5, pady=5, sticky=(W))
		self.sel.set(texts.boundsList[self.options.selbounds])
		self.selcombo.bind('<<ComboboxSelected>>', self.onSelect)

		boundspanel = ttk.LabelFrame(frame, text='') #texts.txtsboundsdlg[''])
		boundspanel.grid(column=0, row=1, padx=BoundsDlg.PANELDISTX, pady=BoundsDlg.PANELDISTY, sticky=(W, E))
		degcmd = boundspanel.register(self.validateDeg)
		pls = texts.planets2
		num = len(self.bounds)
		subnum = len(self.bounds[0])
		for i in range(num):
			label = ttk.Label(boundspanel, text=texts.signs[i]+':')
			label.grid(column=0, row=i, padx=5, pady=5, sticky=(W))
			for j in range(subnum):
				self.bounds[i][j][0] = StringVar()
				cb = ttk.Combobox(boundspanel, textvariable=self.bounds[i][j][0], width=7, state='readonly', values=pls)
				self.bounds[i][j][0].set(pls[self.boundsval[self.options.selbounds][i][j][0]])
				cb.grid(column=2*j+1, row=i, padx=5, pady=5, sticky=(W))
				self.bounds[i][j][1] = StringVar()
				ent = ttk.Entry(boundspanel, textvariable=self.bounds[i][j][1] , width=3, validate='key', validatecommand=(degcmd, '%d', '%s'))
				self.bounds[i][j][1].set(str(self.boundsval[self.options.selbounds][i][j][1]))
				ent.grid(column=2*j+2, row=i, padx=5, pady=5, sticky=(W))


		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		self.selcombo.focus()
		self.win.bind('<Return>', self.ok)
		self.currsel = 0
		self.allright = False
		self.center()


	def onSelect(self, event=None):
		self.selcombo.selection_clear()
		idx = self.selcombo.current()
		oldidx = 0
		if (idx == 0):
			oldidx = 1
		if (self.validate()):
			#save the old and display the new
			pls = texts.planets2
			plsnum = len(pls)
			num = len(self.bounds)
			subnum = len(self.bounds[0])
			for i in range(num):
				for j in range(subnum):
					pltxt = self.bounds[i][j][0].get()
					for k in range(plsnum):
						if (pltxt == pls[k]):
							break

					self.boundsval[oldidx][i][j][0] = k
					self.boundsval[oldidx][i][j][1] = int(self.bounds[i][j][1].get())
	
					self.bounds[i][j][0].set(pls[self.boundsval[idx][i][j][0]])
					self.bounds[i][j][1].set(str(self.boundsval[idx][i][j][1]))
		else:
			self.selcombo.current(oldidx)


	# check if there is an empty Entry ('') and is the value 0-20 ?
	def validate(self):
		num = len(self.bounds)
		subnum = len(self.bounds[0])
		for i in range(num):
			for j in range(subnum):
				if (self.bounds[i][j][1].get() == ''):
					messagebox.showerror(parent=self.win, message=texts.txtsvalidators['NumFieldsCannotBeEmpty'])
					return False
				if (int(self.bounds[i][j][1].get()) > 20):
					messagebox.showerror(parent=self.win, message=texts.txtsboundsdlg['RangeError']+'%2d' % 20)
					return False

		return True


	def validateDeg(self, why, what):
		if ((len(what) >= 2) and (int(why) == 1)):		#"why=1 if insertion"
			return False

		return True


	def ok(self, event=None):
		if (self.validate()):
			pls = texts.planets2
			plsnum = len(pls)
			num = len(self.bounds)
			subnum = len(self.bounds[0])
			curridx = self.selcombo.current()
			#save current selections, values
			for i in range(num):
				for j in range(subnum):
					pltxt = self.bounds[i][j][0].get()
					for k in range(plsnum):
						if (pltxt == pls[k]):
							break

					self.boundsval[curridx][i][j][0] = k
					self.boundsval[curridx][i][j][1] = int(self.bounds[i][j][1].get())

			#check multiplanetselections, 30deg
			OK = 0
			MULTIPLANETS = 1
			NOT30 = 2
			errcode = OK
			boundsListLen = len(texts.boundsList)
			for typ in range(boundsListLen):
				for i in range(num):
					summa = 0
					plssel = [False, False, False, False, False, False, False]
					for j in range(subnum):
						if (not plssel[self.boundsval[typ][i][j][0]]):
							plssel[self.boundsval[typ][i][j][0]] = True
						else:
							errcode = 1
							summa = chart.Chart.SIGN_DEG
							break
						summa += self.boundsval[typ][i][j][1]

					if (summa != chart.Chart.SIGN_DEG):
						errcode = 2
					if (errcode != 0):
						break
				if (errcode != 0):
					break

			if (errcode == OK):
				self.allright = True
				self.currsel = self.selcombo.current()
				self.destroy()
			else:
				self.allright = False
				self.currsel = 0
				txt = texts.txtsboundsdlg['MultiPlanets']+'('+texts.boundsList[typ]+','+texts.signs[i]+')'
				if (errcode == NOT30):
					txt = texts.txtsboundsdlg['NOT30']+'('+texts.boundsList[typ]+','+texts.signs[i]+')'
				messagebox.showerror(parent=self.win, message=txt)


	def check(self, opts):
		changed = False

		if (opts.selbounds != self.currsel):
			opts.selbounds = self.currsel
			changed = True

		num = len(self.boundsval[0])
		subnum = len(self.boundsval[0][0])
		boundsListLen = len(texts.boundsList)
		for typ in range(boundsListLen):
			for i in range(num):
				for j in range(subnum):
					if (self.boundsval[typ][i][j][0] != opts.bounds[typ][i][j][0] or self.boundsval[typ][i][j][1] != opts.bounds[typ][i][j][1]):
						opts.bounds[typ][i][j][0] = self.boundsval[typ][i][j][0] 
						opts.bounds[typ][i][j][1] = self.boundsval[typ][i][j][1] 
						changed = True
						
		return changed


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








