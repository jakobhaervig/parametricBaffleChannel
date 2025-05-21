#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.14.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'C:/Users/jakob/Desktop')

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS

def salome_init():
    salome.salome_init()
    import salome_notebook
    notebook = salome_notebook.NoteBook()
    sys.path.insert(0, r'C:/Users/jakob/Desktop')
    import GEOM
    from salome.geom import geomBuilder
    import math
    import SALOMEDS

def create_

if __name__ == "__main__":
    

geompy = geomBuilder.New()
O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
baffle = geompy.MakeFaceHW(1, 1, 1)
geompy.Rotate(baffle, OY, 45*math.pi/180.0)
geompy.TranslateDXDYDZ(baffle, 1, 0, 0)
geompy.ExportSTL(baffle, "baffle.stl", True, 0.001, True)