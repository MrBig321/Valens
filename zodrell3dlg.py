from tkinter import *
from tkinter import ttk
import zodrell3
import texts
import util


class ZodRelL3Dlg:

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
		self.tree = ttk.Treeview(frame, selectmode='none', height=20)

		self.tree.column('#0', width=250, anchor='center')

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
			signtxt = texts.signs2[self.zrs[i][zodrell3.ZodRelL3.SIGN]]
			leveltxt = texts.txtszodreldlg['L']+str(self.zrs[i][zodrell3.ZodRelL3.LEVEL])
			offstxt = ''
			if (self.zrs[i][zodrell3.ZodRelL3.LEVEL] == 3):
				leveltxt += '/'+texts.txtszodreldlg['L']+'4'
			else:
				offstxt = '     '
			lbtxt = ''
			if (self.zrs[i][zodrell3.ZodRelL3.LB]):
				lbtxt = ' --- '+texts.txtszodreldlg['LB']
			datetxt = str(self.zrs[i][zodrell3.ZodRelL3.DAY])+'/'+str(self.zrs[i][zodrell3.ZodRelL3.MONTH])+'/'+str(self.zrs[i][zodrell3.ZodRelL3.YEAR])
			timetxt = str(self.zrs[i][zodrell3.ZodRelL3.HOUR]).zfill(2)+':'+str(self.zrs[i][zodrell3.ZodRelL3.MINUTE]).zfill(2)

			txt = offstxt+signtxt+' '+leveltxt+' '+datetxt+' '+timetxt+lbtxt
			self.iids.append(self.tree.insert('', 'end', text=txt, values=(), tags='astrotext'))

		self.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
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
		if (self.parent != None):
			self.parent.destroying(self)


	def center(self):
		self.win.withdraw()
		self.win.update_idletasks()
		sw = self.parent.win.winfo_screenwidth()
		sh = self.parent.win.winfo_screenheight()
		w = self.win.winfo_reqwidth()
		h = self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()






