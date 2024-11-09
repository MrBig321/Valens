import os
import pickle
import copy
from tkinter import messagebox
import texts


class Options:

	NONE = 0
	ANTIS = 1
	DODEC = 2

	def __init__(self):
		#Appearance
		self.def_hellenistic = self.hellenistic = True
		self.def_showbounds = self.showbounds = False
		self.def_showboundsround = self.showboundsround = False
		self.def_showdata = self.showdata = True
		self.def_showcuspspos = self.showcuspspos = False
		self.def_topocentric = self.topocentric = False
		self.def_outer = self.outer = Options.NONE
		self.lots = [True, True, False, False, False, False, False]
		self.def_lots = self.lots[:]
		self.def_syzygy = self.syzygy = True

		#Ayanamsha
		self.def_ayanamsa = self.ayanamsa = 0

		#Housesystem
		self.def_hsys = self.hsys = 1

		#Node
		self.def_meannode = self.meannode = True

		#Bounds
		self.def_selbounds = self.selbounds = 0

		self.bounds = [[[[1, 6], [4, 6], [5, 8], [2, 5], [0, 5]],
					[[4, 8], [5, 6], [1, 8], [0, 5], [2, 3]],
					[[5, 6], [1, 6], [4, 5], [2, 7], [0, 6]],
					[[2, 7], [4, 6], [5, 6], [1, 7], [0, 4]],
					[[1, 6], [4, 5], [0, 7], [5, 6], [2, 6]],
					[[5, 7], [4, 10], [1, 4], [2, 7], [0, 2]],
					[[0, 6], [5, 8], [1, 7], [4, 7], [2, 2]],
					[[2, 7], [4, 4], [5, 8], [1, 5], [0, 6]],
					[[1, 12], [4, 5], [5, 4], [0, 5], [2, 4]],
					[[5, 7], [1, 7], [4, 8], [0, 4], [2, 4]],
					[[5, 7], [4, 6], [1, 7], [2, 5], [0, 5]],
					[[4, 12], [1, 4], [5, 3], [2, 9], [0, 2]]],
					[[[1, 6], [4, 8], [5, 7], [2, 5], [0, 4]],
					[[4, 8], [5, 7], [1, 7], [0, 2], [2, 6]],
					[[5, 7], [1, 6], [4, 7], [2, 6], [0, 4]],
					[[2, 6], [1, 7], [5, 7], [4, 7], [0, 3]],
					[[1, 6], [5, 7], [0, 6], [4, 6], [2, 5]],
					[[5, 7], [4, 6], [1, 5], [0, 6], [2, 6]],
					[[0, 6], [4, 5], [5, 5], [1, 8], [2, 6]],
					[[2, 6], [4, 7], [1, 8], [5, 6], [0, 3]],
					[[1, 8], [4, 6], [5, 5], [0, 6], [2, 5]],
					[[4, 6], [5, 6], [1, 7], [0, 6], [2, 5]],
					[[0, 6], [5, 6], [4, 8], [1, 5], [2, 5]],
					[[4, 8], [1, 6], [5, 6], [2, 5], [0, 5]]]]

		self.def_bounds = copy.deepcopy(self.bounds)

		#Default Location
		self.def_deflocname = self.deflocname = 'Budapest, HUN'
		self.def_deflocplus = self.deflocplus = True
		self.def_defloczhour = self.defloczhour = 1
		self.def_defloczminute = self.defloczminute = 0
		self.def_deflocdst = self.deflocdst = False
		self.def_defloclondeg = self.defloclondeg = 19
		self.def_defloclonmin = self.defloclonmin = 4
		self.def_defloclatdeg = self.defloclatdeg = 47
		self.def_defloclatmin = self.defloclatmin = 30
		self.def_defloceast = self.defloceast = True
		self.def_deflocnorth = self.deflocnorth = True
		self.def_deflocalt = self.deflocalt = 100

		#Colors
		self.def_bw = self.bw = False
		self.def_clrframe = self.clrframe = (0,0,255)
		self.def_clrsigns = self.clrsigns = (0,0,255)
		self.def_clrAscMC = self.clrAscMC = (0,0,0)

#		self.def_clraux = self.clraux = (0,0,128)

		self.clrplanets = [(0,0,0), (0,0,255), (178,34,34), (255,215,0), (0,128,0), (138,43,226), (0,191,255), (139,54,38)]
		self.def_clrplanets = self.clrplanets[:]

		self.def_clrbackground = self.clrbackground = (192,192,192)
		self.def_clrtexts = self.clrtexts = (0,0,0)

		self.def_clrtextsintablesblack = self.clrtextsintablesblack = False

		#Sect
		self.def_sectecl = self.sectecl = True
		self.def_sectuseorb = self.sectuseorb = False
		self.def_sectorb = self.sectorb = 0
		self.def_sectptolemy = self.sectptolemy = False

		#PDs
		self.def_subzodiacal = self.subzodiacal = 0
		self.def_bianchini = self.bianchini = False

		self.zodpromsigasps = [True, False]
		self.def_zodpromsigasps = self.zodpromsigasps[:]
		self.ascmchcsasproms = False
		self.def_ascmchcsasproms = self.ascmchcsasproms

			#Proms
		self.promplanets = [True, True, True, True, True, True, True, False]
		self.def_promplanets = self.promplanets[:]
		self.pdsecmotion = self.def_pdsecmotion = False
		self.pdsecmotioniter = self.def_pdsecmotioniter = 2 #3rd iter is the default

		self.pdbounds = self.def_pdbounds = False

		self.def_pduser = self.pduser = False
		self.pduserlon = [0,0,0]
		self.def_pduserlon = self.pduserlon[:]
		self.pduserlat = [0,0,0]
		self.def_pduserlat = self.pduserlat[:]
		self.def_pdusersouthern = self.pdusersouthern = False

			#Asps
		self.pdaspects = [True, True, True, True, True]
		self.def_pdaspects = self.pdaspects[:]

			#Sigs
		self.sigascmc = [True, True]
		self.def_sigascmc = self.sigascmc[:]
		self.sigplanets = [True, True, True, True, True, True, True, False]
		self.def_sigplanets = self.sigplanets[:]

		self.def_pduser2 = self.pduser2 = False
		self.pduser2lon = [0,0,0]
		self.def_pduser2lon = self.pduser2lon[:]
		self.pduser2lat = [0,0,0]
		self.def_pduser2lat = self.pduser2lat[:]
		self.def_pduser2southern = self.pduser2southern = False

			#Keys
		self.pdkeydyn = False
		self.def_pdkeydyn = self.pdkeydyn
		self.pdkeyd = 0
		self.def_pdkeyd = self.pdkeyd
		self.pdkeys = 0 
		self.def_pdkeys = self.pdkeys
		self.pdkeydeg = 0
		self.def_pdkeydeg = self.pdkeydeg
		self.pdkeymin = 0
		self.def_pdkeymin = self.pdkeymin
		self.pdkeysec = 0
		self.def_pdkeysec = self.pdkeysec

		#Lots
		self.def_lotsopts = self.lotsopts = []
		self.def_hcmeanssigncusp = self.hcmeanssigncusp = False
		self.def_ascissigncusp = self.ascissigncusp = False

		#ZodRel
		self.zregyptian = self.def_zregyptian = True
		self.zr27cap = self.def_zr27cap = True

		#General
		self.autosave = False
		self.def_autosave = self.autosave

		self.optionsfile = 'Valens.opt'
		self.load()


	def reload(self):
		#Appearance
		self.hellenistic = self.def_hellenistic
		self.showbounds = self.def_showbounds
		self.showboundsround = self.def_showboundsround
		self.showdata = self.def_showdata
		self.showcuspspos = self.def_showcuspspos
		self.topocentric = self.def_topocentric
		self.outer = self.def_outer
		self.lots = self.def_lots[:]
		self.syzygy = self.def_syzygy

		#Ayanamsha
		self.ayanamsa = self.def_ayanamsa

		#Housesystem
		self.hsys = self.def_hsys

		#Node
		self.meannode = self.def_meannode

		#Terms
		self.selbounds = self.def_selbounds
		self.bounds = copy.deepcopy(self.def_bounds)

		#Default Location
		self.deflocname = self.def_deflocname
		self.deflocplus = self.def_deflocplus
		self.defloczhour = self.def_defloczhour
		self.defloczminute = self.def_defloczminute
		self.deflocdst = self.def_deflocdst
		self.defloclondeg = self.def_defloclondeg
		self.defloclonmin = self.def_defloclonmin
		self.defloclatdeg = self.def_defloclatdeg
		self.defloclatmin = self.def_defloclatmin
		self.defloceast = self.def_defloceast
		self.deflocnorth = self.def_deflocnorth
		self.deflocalt = self.def_deflocalt

		#Colors
		self.bw = self.def_bw
		self.clrframe = self.def_clrframe
		self.clrsigns = self.def_clrsigns
		self.clrAscMC = self.def_clrAscMC

#		self.clraux = self.def_clraux

		self.clrplanets = self.def_clrplanets[:]

		self.clrbackground = self.def_clrbackground
		self.clrtexts = self.def_clrtexts
		self.clrtextsintablesblack = self.def_clrtextsintablesblack

		#Sect
		self.sectecl = self.def_sectecl
		self.sectuseorb = self.def_sectuseorb
		self.sectorb = self.def_sectorb
		self.sectptolemy = self.def_sectptolemy

		#PDs
		self.subzodiacal = self.def_subzodiacal
		self.bianchini = self.def_bianchini

		self.zodpromsigasps = self.def_zodpromsigasps[:]
		self.ascmchcsasproms = self.def_ascmchcsasproms

			#Proms
		self.promplanets = self.def_promplanets[:]
		self.pdsecmotion = self.def_pdsecmotion
		self.pdsecmotioniter = self.def_pdsecmotioniter

		self.pdbounds = self.def_pdbounds

		self.pduser = self.def_pduser
		self.pduserlon = self.def_pduserlon[:]
		self.pduserlat = self.def_pduserlat[:]
		self.pdusersouthern = self.def_pdusersouthern

			#Asps
		self.pdaspects = self.def_pdaspects[:]

			#Sigs
		self.sigascmc = self.def_sigascmc[:]
		self.sigplanets = self.def_sigplanets[:]

		self.pduser2 = self.def_pduser2
		self.pduser2lon = self.def_pduser2lon[:]
		self.pduser2lat = self.def_pduser2lat[:]
		self.pduser2southern = self.def_pduser2southern

			#Keys
		self.pdkeydyn = self.def_pdkeydyn
		self.pdkeyd = self.def_pdkeyd
		self.pdkeys = self.def_pdkeys
		self.pdkeydeg = self.def_pdkeydeg
		self.pdkeymin = self.def_pdkeymin
		self.pdkeysec = self.def_pdkeysec

		#Lots
		self.lotsopts = self.def_lotsopts[:]
		self.hcmeanssigncusp = self.def_hcmeanssigncusp
		self.ascissigncusp = self.def_ascissigncusp

		#ZodRel
		self.zregyptian = self.def_zregyptian
		self.zr27cap = self.def_zr27cap

		#General
		self.autosave = self.def_autosave


	def load(self):
		try:
			f = open(self.optionsfile, 'rb')		
			#Appearance
			self.hellenistic = pickle.load(f)
			self.showbounds = pickle.load(f)
			self.showboundsround = pickle.load(f)
			self.showdata = pickle.load(f)
			self.showcuspspos = pickle.load(f)
			self.topocentric = pickle.load(f)
			self.outer = pickle.load(f)
			self.lots = pickle.load(f)
			self.syzygy = pickle.load(f)
			#Ayanamsa
			self.ayanamsa = pickle.load(f)
			#Housesystem
			self.hsys = pickle.load(f)
			#Node
			self.meannode = pickle.load(f)
			#Bounds
			self.selbounds = pickle.load(f)
			self.bounds = pickle.load(f)
			#DefaultLocation
			self.deflocname = pickle.load(f)
			self.deflocplus = pickle.load(f)
			self.defloczhour = pickle.load(f)
			self.defloczminute = pickle.load(f)
			self.deflocdst = pickle.load(f)
			self.defloclondeg = pickle.load(f)
			self.defloclonmin = pickle.load(f)
			self.defloclatdeg = pickle.load(f)
			self.defloclatmin = pickle.load(f)
			self.defloceast = pickle.load(f)
			self.deflocnorth = pickle.load(f)
			self.deflocalt = pickle.load(f)
			#Colors
			self.bw = pickle.load(f)
			self.clrframe = pickle.load(f)
			self.clrsigns = pickle.load(f)
			self.clrAscMC = pickle.load(f)
#			self.clraux = pickle.load(f)
			self.clrplanets = pickle.load(f)
			self.clrbackground = pickle.load(f)
			self.clrtexts = pickle.load(f)
			self.clrtextsintablesblack = pickle.load(f)
			#Sect
			self.sectecl = pickle.load(f)
			self.sectuseorb = pickle.load(f)
			self.sectorb = pickle.load(f)
			self.sectptolemy = pickle.load(f)
			#PDs
			self.subzodiacal = pickle.load(f)
			self.bianchini = pickle.load(f)
			self.zodpromsigasps = pickle.load(f)
			self.ascmchcsasproms = pickle.load(f)
			self.promplanets = pickle.load(f)
			self.pdsecmotion = pickle.load(f)
			self.pdsecmotioniter = pickle.load(f)
			self.pdbounds = pickle.load(f)
			self.pduser = pickle.load(f)
			self.pduserlon = pickle.load(f)
			self.pduserlat = pickle.load(f)
			self.pdusersouthern = pickle.load(f)
			self.pdaspects = pickle.load(f)
			self.sigascmc = pickle.load(f)
			self.sigplanets = pickle.load(f)
			self.pduser2 = pickle.load(f)
			self.pduser2lon = pickle.load(f)
			self.pduser2lat = pickle.load(f)
			self.pduser2southern = pickle.load(f)
			self.pdkeydyn = pickle.load(f)
			self.pdkeyd = pickle.load(f)
			self.pdkeys = pickle.load(f)
			self.pdkeydeg = pickle.load(f)
			self.pdkeymin = pickle.load(f)
			self.pdkeysec = pickle.load(f)
			#Lots
			self.lotsopts = pickle.load(f)
			self.hcmeanssigncusp = pickle.load(f)
			self.ascissigncusp = pickle.load(f)
			#ZodRel
			self.zregyptian = pickle.load(f)
			self.zr27cap = pickle.load(f)

			#General
			self.autosave = pickle.load(f)
			f.close()
			return True
		except IOError:
#			messagebox.showerror(message=texts.txtsfiles['OptFileError'])
			return False


	def save(self):
		try:
			f = open(self.optionsfile, 'wb')		
			pickle.dump(self.hellenistic, f)
			pickle.dump(self.showbounds, f)
			pickle.dump(self.showboundsround, f)
			pickle.dump(self.showdata, f)
			pickle.dump(self.showcuspspos, f)
			pickle.dump(self.topocentric, f)
			pickle.dump(self.outer, f)
			pickle.dump(self.lots, f)
			pickle.dump(self.syzygy, f)
			#Ayanamsa
			pickle.dump(self.ayanamsa, f)
			#Housesystem
			pickle.dump(self.hsys, f)
			#Node
			pickle.dump(self.meannode, f)
			#Bounds
			pickle.dump(self.selbounds, f)
			pickle.dump(self.bounds, f)
			#DefaultLocation
			pickle.dump(self.deflocname, f)
			pickle.dump(self.deflocplus, f)
			pickle.dump(self.defloczhour, f)
			pickle.dump(self.defloczminute, f)
			pickle.dump(self.deflocdst, f)
			pickle.dump(self.defloclondeg, f)
			pickle.dump(self.defloclonmin, f)
			pickle.dump(self.defloclatdeg, f)
			pickle.dump(self.defloclatmin, f)
			pickle.dump(self.defloceast, f)
			pickle.dump(self.deflocnorth, f)
			pickle.dump(self.deflocalt, f)
			#Colors
			pickle.dump(self.bw, f)
			pickle.dump(self.clrframe, f)
			pickle.dump(self.clrsigns, f)
			pickle.dump(self.clrAscMC, f)
#			pickle.dump(self.clraux, f)
			pickle.dump(self.clrplanets, f)
			pickle.dump(self.clrbackground, f)
			pickle.dump(self.clrtexts, f)
			pickle.dump(self.clrtextsintablesblack, f)
			#Sect
			pickle.dump(self.sectecl, f)
			pickle.dump(self.sectuseorb, f)
			pickle.dump(self.sectorb, f)
			pickle.dump(self.sectptolemy, f)
			#PDs
			pickle.dump(self.subzodiacal, f)
			pickle.dump(self.bianchini, f)
			pickle.dump(self.zodpromsigasps, f)
			pickle.dump(self.ascmchcsasproms, f)
			pickle.dump(self.promplanets, f)
			pickle.dump(self.pdsecmotion, f)
			pickle.dump(self.pdsecmotioniter, f)
			pickle.dump(self.pdbounds, f)
			pickle.dump(self.pduser, f)
			pickle.dump(self.pduserlon, f)
			pickle.dump(self.pduserlat, f)
			pickle.dump(self.pdusersouthern, f)
			pickle.dump(self.pdaspects, f)
			pickle.dump(self.sigascmc, f)
			pickle.dump(self.sigplanets, f)
			pickle.dump(self.pduser2, f)
			pickle.dump(self.pduser2lon, f)
			pickle.dump(self.pduser2lat, f)
			pickle.dump(self.pduser2southern, f)
			pickle.dump(self.pdkeydyn, f)
			pickle.dump(self.pdkeyd, f)
			pickle.dump(self.pdkeys, f)
			pickle.dump(self.pdkeydeg, f)
			pickle.dump(self.pdkeymin, f)
			pickle.dump(self.pdkeysec, f)
			#Lots
			pickle.dump(self.lotsopts, f)
			pickle.dump(self.hcmeanssigncusp, f)
			pickle.dump(self.ascissigncusp, f)
			#ZodRel
			pickle.dump(self.zregyptian, f)
			pickle.dump(self.zr27cap, f)
			#General
			pickle.dump(self.autosave, f)
			f.close()
			return True
		except IOError:
			messagebox.showerror(message=texts.txtsfiles['OptFileError'])
			return False


	def checkOptsFile(self):
		if (os.path.exists(self.optionsfile)):
			return True

		return False


	def removeOptsFile(self):
		if (os.path.exists(self.optionsfile)):
			os.remove(self.optionsfile)





