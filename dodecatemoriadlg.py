from tkinter import *
from tkinter import ttk
import chart
import planets
import dodecatemoria
import texts
import util


class DodecatemoriaDlg:

	def __init__(self, parent, chrt, opts):
		self.parent = parent
		self.chart = chrt
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtsdodecatemoria['Dodecatemoria'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)
#		frame.configure(width=300)
#		frame.grid_columnconfigure(0, weight=1)
#		frame.grid_rowconfigure(0, weight=1)
#		frame.columnconfigure(0, weight=1)
#		frame.rowconfigure(0, weight=1)

		bkg_rgb = util.getRGBTxt(self.options.clrbackground) 
#		txt_rgb = util.getRGBTxt(self.options.clrtexts) 
		tree = ttk.Treeview(frame, columns=('long'), selectmode='none', height=18)

#		tree.column('#0', width=100, minwidth=2000, anchor='center') #!! Horizontal scrollbar only takes minwidth into account !!
		tree.column('#0', width=80, anchor='center')
		tree.column('long', width=120, anchor='center')

		ysb = ttk.Scrollbar(frame, orient='vertical', command=tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(frame, orient='horizontal', command=tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		tree.configure(yscroll=ysb.set, xscroll=xsb.set)

	#	tree.heading('#0', text='Planets')
		tree.heading('long', text=texts.txtsdodecatemoria['Longitude'])

		if (self.options.clrtextsintablesblack):
			tree.tag_configure('ascmc', background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			tree.tag_configure('ascmc', background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrtexts))
		#AscMC
		txts = (texts.txtscommon['Asc'], texts.txtscommon['MC'])
		num = len(self.chart.dodec.ascmclons)
		for i in range(num):
			lon = self.chart.dodec.ascmclons[i]
			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			iid = tree.insert('', 'end', text=txts[i], values=(lontxt, ), tags='ascmc')
		#Planets
		tagstxts = ('saturntag', 'jupitertag', 'marstag', 'suntag', 'venustag', 'mercurytag', 'moontag', 'anodetag')
		num = len(self.chart.dodec.plslons)
		for i in range(num):
			lon = self.chart.dodec.plslons[i]
			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			if (self.options.clrtextsintablesblack):
				tree.tag_configure(tagstxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				tree.tag_configure(tagstxts[i], background=bkg_rgb, foreground=util.getRGBTxt(self.options.clrplanets[i]))
			iid = tree.insert('', 'end', text=texts.planets[i], values=(lontxt, ), tags=tagstxts[i])
		#Lots
		lotclrs = (self.options.clrplanets[planets.Planets.MOON], self.options.clrplanets[planets.Planets.SUN], self.options.clrplanets[planets.Planets.VENUS], self.options.clrplanets[planets.Planets.JUPITER], self.options.clrplanets[planets.Planets.MERCURY], self.options.clrplanets[planets.Planets.MARS], self.options.clrplanets[planets.Planets.SATURN])
		tagstxts = ('fortunetag', 'spirittag', 'erostag', 'victorytag', 'necessitytag', 'couragetag', 'nemesistag')
		num = len(self.chart.dodec.lotslons)
		for i in range(num):
			lon = self.chart.dodec.lotslons[i]
			d, m, s = util.decToDeg(lon)
			sign = int(d/chart.Chart.SIGN_DEG)
			pos = int(d%chart.Chart.SIGN_DEG)
			lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
			if (self.options.clrtextsintablesblack):
				tree.tag_configure(tagstxts[i], background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
			else:
				tree.tag_configure(tagstxts[i], background=bkg_rgb, foreground=util.getRGBTxt(lotclrs[i]))
			iid = tree.insert('', 'end', text=texts.lotsList[i], values=(lontxt, ), tags=tagstxts[i])
		#Syzygy
		tagtxt = 'syzygytag'
		syzclr = self.options.clrsigns
		lon = self.chart.dodec.syzlon
		d, m, s = util.decToDeg(lon)
		sign = int(d/chart.Chart.SIGN_DEG)
		pos = int(d%chart.Chart.SIGN_DEG)
		lontxt = (str(pos)).rjust(2)+texts.signs2[sign]+' '+(str(m)).zfill(2)+"'"+' '+(str(s)).zfill(2)+'"'
		if (self.options.clrtextsintablesblack):
			tree.tag_configure(tagtxt, background=bkg_rgb, foreground=util.getRGBTxt((0,0,0)))
		else:
			tree.tag_configure(tagtxt, background=bkg_rgb, foreground=util.getRGBTxt(syzclr))
		iid = tree.insert('', 'end', text=texts.txtscommon['Syzygy'], values=(lontxt, ), tags=tagtxt)

		tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Close'], command=self.ok)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=0, row=2, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.win.bind('<Destroy>', self.ok)
#		self.allright = False
		self.center()
#		self.win.geometry('%dx%d+%d+%d' % (400, 300, 0, 0))
#		self.win.update_idletasks()


	def ok(self, event=None):
#		self.allright = True
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






