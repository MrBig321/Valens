#!/usr/bin/env python3


#Valens, Astrology program
#Copyright (C) 2014  Robert Nagy (robert.pluto@gmail.com)

#This program is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.

#This program is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with this program.  If not, see <http://www.gnu.org/licenses/>.


import os
import sys
from tkinter import *
import options
import texts
import vframe

try:
	progPath = os.path.dirname(sys.argv[0])
	os.chdir(progPath)
except:
	pass

opts = options.Options()
frame = vframe.VFrame(opts, texts.txtscommon['ProgramTitle'])
frame.mainloop()



