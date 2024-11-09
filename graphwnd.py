from tkinter import *
import graphephem
import texts


class GraphWnd:
	XSIZE = 512
	YSIZE = 512

	def __init__(self, parent, year, posArr, opts):

		self.parent = parent
		self.year = year
		self.posArr = posArr
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsgraphephemwnd['Ephemeris'])
#		self.win.resizable(FALSE, FALSE)
		self.win.bind('<Destroy>', self.ok)
		self.win.minsize(300,300)

		self.firsttime = True
		self.prevw = GraphWnd.XSIZE
		self.prevh = GraphWnd.YSIZE

		#Popup-menu
		self.bw = BooleanVar()
		self.menu = Menu(self.win, tearoff=0)
		self.menu.add_checkbutton(label=texts.txtscommon['BW'], variable=self.bw, command=self.onBW, onvalue=True)
		self.win.bind('<Button-3>', self.onMenu)
		self.win.bind('<Button-1>', self.onLeftClick)

		origcursor = self.win.config(cursor='watch')
		self.graph = graphephem.GraphEphem(self.win, year, posArr, opts, (GraphWnd.XSIZE, GraphWnd.YSIZE))
		self.graph.can.pack(fill=BOTH, expand=1)
		origcursor = self.win.config(cursor='left_ptr')

		self.win.bind('<Configure>', self.onResize)
		self.center() ##


	def onBW(self, event=None):
		self.graph.bw = self.bw.get()
		self.graph.drawCanvas((self.prevw, self.prevh))


	def onMenu(self, event=None):
		self.menu.post(event.x_root, event.y_root)


	def onLeftClick(self, event=None):
		self.menu.unpost()


	def onResize(self, event):
		self.win.update_idletasks()
		w = self.win.winfo_width()
		h = self.win.winfo_height()
		if (self.firsttime or w != self.prevw or h != self.prevh):
			self.firsttime = False
			self.graph.drawCanvas((w, h))
			self.prevw = w
			self.prevh = h


	def ok(self, event=None):
		self.destroy()


	def show(self):
		self.win.focus_set()
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def destroy(self):
		self.win.destroy()


	def center(self):
		self.win.withdraw()
		self.win.update_idletasks()
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		w = 640 #self.win.winfo_reqwidth()
		h = 400 #self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()








