from tkinter import *
from tkinter import ttk
import placeslistdlg
import geonames
import texts
import util


class PlaceList:
	PLACE = 0
	COUNTRY = 1
	LON = 2
	LAT = 3
	ZONE = 4
	ALT = 5
	COLNUM = ALT+1

	def __init__(self, parent, li):
		self.parent = parent
		self.tree = ttk.Treeview(parent, columns=('coun', 'lon', 'lat', 'zone', 'alt'), selectmode='browse', height=10)

		self.tree.column('#0', width=140, anchor='center')
		self.tree.column('coun', width=120, anchor='center')
		self.tree.column('lon', width=80, anchor='center')
		self.tree.column('lat', width=70, anchor='center')
		self.tree.column('zone', width=60, anchor='center')
		self.tree.column('alt', width=60, anchor='center')

		ysb = ttk.Scrollbar(self.parent, orient='vertical', command=self.tree.yview)
		ysb.grid(row=0, column=1, sticky=(N,S))
		xsb = ttk.Scrollbar(parent, orient='horizontal', command=self.tree.xview)
		xsb.grid(row=1, column=0, sticky=(E,W))
		self.tree.configure(yscroll=ysb.set, xscroll=xsb.set)

		self.tree.heading('#0', text=texts.txtsplacesdlg['Places'])
		self.tree.heading('coun', text=texts.txtsplacesdlg['Country'])
		self.tree.heading('lon', text=texts.txtsplacesdlg['Long'])
		self.tree.heading('lat', text=texts.txtsplacesdlg['Lat'])
		self.tree.heading('zone', text=texts.txtsplacesdlg['Zone'])
		self.tree.heading('alt', text=texts.txtsplacesdlg['Alt'])

		self.iids = []
		self.load(li)
		self.tree.bind('<<TreeviewSelect>>', self.onSelect)
		self.changed = False
		self.selitem = None


	def onSelect(self, event):
		self.selitem = self.tree.selection()[0]


	def load(self, li):
		for it in li:
			dirtxt = 'E'
			lon = it[geonames.Geonames.LON]
			if (lon < 0.0):
				dirtxt = 'W'
				lon *= -1
			d, m, s = util.decToDeg(lon)
			lontxt = str(d).zfill(2)+dirtxt+str(m).zfill(2)

			dirtxt = 'N'
			lat = it[geonames.Geonames.LAT]
			if (lat < 0.0):
				dirtxt = 'S'
				lat *= -1
			d, m, s = util.decToDeg(lat)
			lattxt = str(d).zfill(2)+dirtxt+str(m).zfill(2)

			gmtoffs = it[geonames.Geonames.GMTOFFS]
			signtxt = '+'
			if (gmtoffs < 0.0):
				signtxt = '-'
				gmtoffs *= -1

			frac = int((gmtoffs-int(gmtoffs))*60.0)
			gmtoffstxt = signtxt+str(int(gmtoffs))+':'+str(frac).zfill(2)

			iid = self.tree.insert('', 'end', text=it[geonames.Geonames.NAME], values=(it[geonames.Geonames.COUNTRYNAME], lontxt, lattxt, gmtoffstxt, it[geonames.Geonames.ALTITUDE]))
			self.iids.append(iid)


	def getIdx(self):
		if (self.selitem != None):
			num = len(self.iids)
			for i in range(num):
				if (self.iids[i] == self.selitem):
					return i

		return None


class PlacesListDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent, li):
		self.parent = parent

		self.win = Toplevel()
		self.win.title(texts.txtsplacesdlg['Places'])
		self.win.parent = parent
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		#PlacesList
		listpanel = ttk.LabelFrame(frame, text='')
		listpanel.grid(column=0, row=0, padx=PlacesListDlg.PANELDISTX, pady=PlacesListDlg.PANELDISTY, sticky=(W,N,S,E)) 
		self.treeobj = PlaceList(listpanel, li)
		self.treeobj.tree.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

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


	def getIdx(self):
		return self.treeobj.getIdx()


	def copyData(self):
		vals = self.treeobj.tree.item(self.treeobj.selitem)
		self.it = []
		self.it.append(vals['text'])
		self.it.append(vals['values'][0])
		self.it.append(vals['values'][1])
		self.it.append(vals['values'][2])
		self.it.append(vals['values'][3])
		self.it.append(vals['values'][4])


	def ok(self, event=None):
#		if (self.treeobj.selitem != None):
#			self.copyData()

		self.allright = True
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
		sw = self.parent.win.winfo_screenwidth()
		sh = self.parent.win.winfo_screenheight()
		w = self.win.winfo_reqwidth()
		h = self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()













