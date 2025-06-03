#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.14.0 with dump python functionality
###

import sys
import salome

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()
sys.path.insert(0, r'/home/jakob')

###
### GEOM component
###

import GEOM
from salome.geom import geomBuilder
import math
import SALOMEDS


geompy = geomBuilder.New()

O = geompy.MakeVertex(0, 0, 0)
OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
Vertex_1 = geompy.MakeVertex(0, -0.005, -0.005)
Vertex_2 = geompy.MakeVertex(0, 0.005, -0.005)
Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
Extrusion_1 = geompy.MakePrismVecH(Line_1, OZ, 0.003)
geompy.Rotate(Extrusion_1, Line_1, 30*math.pi/180.0)
Multi_Translation_1 = geompy.MakeMultiTranslation1D(Extrusion_1, OX, 0.01, 5)
geompy.ExportSTL(Multi_Translation_1, "baffles.stl", True, 0.001, True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Vertex_2, 'Vertex_2' )
geompy.addToStudy( Line_1, 'Line_1' )
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )
geompy.addToStudy( Multi_Translation_1, 'Multi-Translation_1' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
