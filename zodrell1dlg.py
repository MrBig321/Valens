from tkinter import *
from tkinter import ttk
import zodrell1
import zodrell3
import zodrell3dlg
import texts
import util


class ZodRelL1Dlg:

	def __init__(self, parent, zrs, opts):
		self.parent = parent
		self.zrs = zrs
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtszodreldlg['ZodRel'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		self.tree = ttk.Treeview(frame, selectmode='browse', height=20)

		self.tree.column('#0', width=200, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

		ttk.Style().configure('Treeview', fieldbackground=bkg_rgb)
		if (self.options.clrtextsintablesblack):
			self.tree.tag_configure('astrotext', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			self.tree.tag_configure('astrotext', background=bkg_rgb, foreground=txt_rgb)

		self.iids = []
		num = len(self.zrs)
		for i in range(num):
			signtxt = texts.signs2[self.zrs[i][zodrell1.ZodRelL1.SIGN]]
			leveltxt = texts.txtszodreldlg['L']+str(self.zrs[i][zodrell1.ZodRelL1.LEVEL])
			offstxt = ''
			if (self.zrs[i][zodrell1.ZodRelL1.LEVEL] == 1):
				leveltxt += '/'+texts.txtszodreldlg['L']+'2'
			else:
				offstxt = '     '
			lbtxt = ''
			if (self.zrs[i][zodrell1.ZodRelL1.LB]):
				lbtxt = ' --- '+texts.txtszodreldlg['LB']
			datetxt = str(self.zrs[i][zodrell1.ZodRelL1.DAY])+'/'+str(self.zrs[i][zodrell1.ZodRelL1.MONTH])+'/'+str(self.zrs[i][zodrell1.ZodRelL1.YEAR])

			txt = offstxt+signtxt+' '+leveltxt+' '+datetxt+lbtxt
			self.iids.append(self.tree.insert('', 'end', text=txt, values=(), tags='astrotext'))

		self.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		self.chldren = []
		self.closing = False

		okbtn.focus()
		self.tree.bind('<Button-1>', self.onListClicked)
		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
		self.center()


	def destroying(self, obj):
		if (not self.closing):
			num = len(self.chldren)
			for i in range(num):
				if (self.chldren[i] == obj):
					del self.chldren[i]
					break


	def destroyChildren(self):
		self.closing = True
		num = len(self.chldren)
		for i in range(num):
			self.chldren[i].destroy()
		del self.chldren[:]
		self.closing = False


	def onListClicked(self, event=None):
		item = self.tree.identify('item', event.x, event.y)
		if (item != ''):
			idx = self.iids.index(item)
			zrl3 = zodrell3.ZodRelL3(self.zrs[idx][zodrell1.ZodRelL1.YEAR], self.zrs[idx][zodrell1.ZodRelL1.MONTH], self.zrs[idx][zodrell1.ZodRelL1.DAY], self.zrs[idx][zodrell1.ZodRelL1.HOUR], self.zrs[idx][zodrell1.ZodRelL1.MINUTE], self.zrs[idx][zodrell1.ZodRelL1.SIGN], self.options)
			zrl3.calc()
			dlg = zodrell3dlg.ZodRelL3Dlg(self, zrl3.zrs, self.options)
			self.chldren.append(dlg)
			dlg.doModal()


	def ok(self, event=None):
		self.destroyChildren()
		self.destroy()


	def doModal(self):
		self.win.focus_set()
#		self.win.grab_set()							# events go only to this wnd
		self.win.transient()						# stay on top
		self.win.wait_window(self.win)				# display and wait


	def destroy(self):
		self.win.destroy()
		if (self.parent != None):
			self.parent.destroying(self)


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






