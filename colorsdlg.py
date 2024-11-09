from tkinter import *
from tkinter import ttk
from tkinter import colorchooser
from tkinter import Button
import planets
import texts
import util


class ColorsDlg:

	PANELDISTX = 2
	PANELDISTY = 2

	def __init__(self, parent, opts):
		self.parent = parent
		self.options = opts

		self.win = Toplevel()
		self.win.title(texts.txtscolorsdlg['Colors'])
		self.win.resizable(FALSE, FALSE)

		frame = ttk.Frame(self.win)
		frame.grid(column=0, row=0, sticky=(N, W, E, S), padx=2, pady=2)

		self.clrarr = []
		for i in range(planets.Planets.PLANETS_NUM+1):
			self.clrarr.append(self.options.clrplanets[i])

		self.clrarr.append(self.options.clrframe)
		self.clrarr.append(self.options.clrsigns)
		self.clrarr.append(self.options.clrAscMC)
		self.clrarr.append(self.options.clrbackground)
		self.clrarr.append(self.options.clrtexts)

		#Planets
		planetspanel = ttk.LabelFrame(frame, text=texts.txtscolorsdlg['Planets'])
		planetspanel.grid(column=0, row=0, rowspan=3, padx=ColorsDlg.PANELDISTX, pady=ColorsDlg.PANELDISTY, sticky=(W, E, N, S))
		label = ttk.Label(planetspanel, text=texts.planets[0]+':')
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.satbtn = Button(planetspanel, width=5, command=self.onSaturn, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.SATURN]))
		self.satbtn.grid(column=1, row=0, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[1]+':')
		label.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.jupbtn = Button(planetspanel, width=5, command=self.onJupiter, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.JUPITER]))
		self.jupbtn.grid(column=1, row=1, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[2]+':')
		label.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.marbtn = Button(planetspanel, width=5, command=self.onMars, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.MARS]))
		self.marbtn.grid(column=1, row=2, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[3]+':')
		label.grid(column=0, row=3, padx=5, pady=5, sticky=(W))
		self.sunbtn = Button(planetspanel, width=5, command=self.onSun, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.SUN]))
		self.sunbtn.grid(column=1, row=3, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[4]+':')
		label.grid(column=0, row=4, padx=5, pady=5, sticky=(W))
		self.venbtn = Button(planetspanel, width=5, command=self.onVenus, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.VENUS]))
		self.venbtn.grid(column=1, row=4, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[5]+':')
		label.grid(column=0, row=5, padx=5, pady=5, sticky=(W))
		self.merbtn = Button(planetspanel, width=5, command=self.onMercury, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.MERCURY]))
		self.merbtn.grid(column=1, row=5, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[6]+':')
		label.grid(column=0, row=6, padx=5, pady=5, sticky=(W))
		self.moobtn = Button(planetspanel, width=5, command=self.onMoon, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.MOON]))
		self.moobtn.grid(column=1, row=6, padx=5, pady=5)
		label = ttk.Label(planetspanel, text=texts.planets[7]+':')
		label.grid(column=0, row=7, padx=5, pady=5, sticky=(W))
		self.nodbtn = Button(planetspanel, width=5, command=self.onNode, bg=util.getRGBTxt(self.options.clrplanets[planets.Planets.ANODE]))
		self.nodbtn.grid(column=1, row=7, padx=5, pady=5)

		#Chart
		chartpanel = ttk.LabelFrame(frame, text=texts.txtscolorsdlg['Chart'])
		chartpanel.grid(column=1, row=0, padx=ColorsDlg.PANELDISTX, pady=ColorsDlg.PANELDISTY, sticky=(W, E, N, S))
		label = ttk.Label(chartpanel, text=texts.txtscolorsdlg['Frame']+':')
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.framebtn = Button(chartpanel, width=5, command=self.onFrame, bg=util.getRGBTxt(self.options.clrframe))
		self.framebtn.grid(column=1, row=0, padx=5, pady=5)
		label = ttk.Label(chartpanel, text=texts.txtscolorsdlg['Signs']+':')
		label.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.signsbtn = Button(chartpanel, width=5, command=self.onSigns, bg=util.getRGBTxt(self.options.clrsigns))
		self.signsbtn.grid(column=1, row=1, padx=5, pady=5)
		label = ttk.Label(chartpanel, text=texts.txtscolorsdlg['AscMC']+':')
		label.grid(column=0, row=2, padx=5, pady=5, sticky=(W))
		self.ascmcbtn = Button(chartpanel, width=5, command=self.onAscMC, bg=util.getRGBTxt(self.options.clrAscMC))
		self.ascmcbtn.grid(column=1, row=2, padx=5, pady=5)

		#General
		generalpanel = ttk.LabelFrame(frame, text=texts.txtscolorsdlg['General'])
		generalpanel.grid(column=1, row=1, padx=ColorsDlg.PANELDISTX, pady=ColorsDlg.PANELDISTY, sticky=(W, E, N, S))
		label = ttk.Label(generalpanel, text=texts.txtscolorsdlg['Background']+':')
		label.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		self.bkgbtn = Button(generalpanel, width=5, command=self.onBkg, bg=util.getRGBTxt(self.options.clrbackground))
		self.bkgbtn.grid(column=1, row=0, padx=5, pady=5)
		label = ttk.Label(generalpanel, text=texts.txtscolorsdlg['Texts']+':')
		label.grid(column=0, row=1, padx=5, pady=5, sticky=(W))
		self.textsbtn = Button(generalpanel, width=5, command=self.onTexts, bg=util.getRGBTxt(self.options.clrtexts))
		self.textsbtn.grid(column=1, row=1, padx=5, pady=5)

		#TextsblackinTables
		textsinblackpanel = ttk.LabelFrame(frame, text=texts.txtscolorsdlg['Tables'])
		textsinblackpanel.grid(column=1, row=2, padx=ColorsDlg.PANELDISTX, pady=ColorsDlg.PANELDISTY, sticky=(W, E, N, S))
		self.textsblack = BooleanVar()
		self.textsblack.set(self.options.clrtextsintablesblack)
		textsblackbtn = ttk.Checkbutton(textsinblackpanel, text=texts.txtscolorsdlg['TextsBlack'], variable=self.textsblack, onvalue=True)
		textsblackbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))

		okpanel = ttk.Frame(frame)
		okbtn = ttk.Button(okpanel, text=texts.txtscommon['Ok'], command=self.ok)
		cancelbtn = ttk.Button(okpanel, text=texts.txtscommon['Cancel'], command=self.cancel)
		okbtn.grid(column=0, row=0, padx=5, pady=5, sticky=(W))
		cancelbtn.grid(column=1, row=0, padx=5, pady=5, sticky=(W))
		okpanel.grid(column=1, row=3, padx=5, pady=5, sticky=(S,E))

		okbtn.focus()
		self.win.bind('<Return>', self.ok)
		self.allright = False
		self.center()


	def onSaturn(self):
		#colorchooser.askcolor(initialcolor='#ff0000')
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.SATURN], title='')
		#result= (triple, color). triple=(r,g,b). Cancel=(None, None)
		if (res[0] != None):
			self.clrarr[planets.Planets.SATURN] = res[0]
			self.satbtn.configure(bg=res[1])


	def onJupiter(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.JUPITER], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.JUPITER] = res[0]
			self.jupbtn.configure(bg=res[1])


	def onMars(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.MARS], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.MARS] = res[0]
			self.marbtn.configure(bg=res[1])


	def onSun(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.SUN], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.SUN] = res[0]
			self.sunbtn.configure(bg=res[1])


	def onVenus(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.VENUS], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.VENUS] = res[0]
			self.venbtn.configure(bg=res[1])


	def onMercury(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.MERCURY], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.MERCURY] = res[0]
			self.merbtn.configure(bg=res[1])


	def onMoon(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.MOON], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.MOON] = res[0]
			self.moobtn.configure(bg=res[1])


	def onNode(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrplanets[planets.Planets.ANODE], title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.ANODE] = res[0]
			self.nodbtn.configure(bg=res[1])


	def onFrame(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrframe, title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.ANODE+1] = res[0]
			self.framebtn.configure(bg=res[1])


	def onSigns(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrsigns, title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.ANODE+2] = res[0]
			self.signsbtn.configure(bg=res[1])


	def onAscMC(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrAscMC, title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.ANODE+3] = res[0]
			self.ascmcbtn.configure(bg=res[1])


	def onBkg(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrbackground, title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.ANODE+4] = res[0]
			self.bkgbtn.configure(bg=res[1])


	def onTexts(self):
		res = colorchooser.askcolor(parent=self.win, color=self.options.clrtexts, title='')
		if (res[0] != None):
			self.clrarr[planets.Planets.ANODE+5] = res[0]
			self.textsbtn.configure(bg=res[1])


	def check(self, opts):
		changed = False

		for i in range(planets.Planets.PLANETS_NUM+1):
			if (self.options.clrplanets[i] != self.clrarr[i]):
				changed = True	#return True

		if (self.options.clrframe != self.clrarr[planets.Planets.ANODE+1]):
			changed = True

		if (self.options.clrsigns != self.clrarr[planets.Planets.ANODE+2]):
			changed = True
		if (self.options.clrAscMC != self.clrarr[planets.Planets.ANODE+3]):
			changed = True
		if (self.options.clrbackground != self.clrarr[planets.Planets.ANODE+4]):
			changed = True
		if (self.options.clrtexts != self.clrarr[planets.Planets.ANODE+5]):
			changed = True
		if (self.options.clrtextsintablesblack != self.textsblack.get()):
			changed = True

		return changed


	def ok(self, event=None):
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
		sw = self.parent.winfo_screenwidth()
		sh = self.parent.winfo_screenheight()
		w = self.win.winfo_reqwidth()
		h = self.win.winfo_reqheight()
		x = (sw // 2) - (w // 2)
		y = (sh // 2) - (h // 2)
		self.win.geometry('%dx%d+%d+%d' % (w, h, x, y))
		self.win.deiconify()






