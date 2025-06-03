#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.14.0 with dump python functionality
###

import sys
import salome
import math

salome.salome_init()
import salome_notebook
notebook = salome_notebook.NoteBook()

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

baffles = []
for i in range(0, 4):
  if i % 2 == 0:
      angle = 10
  else:
      angle = -10

  Vertex_1 = geompy.MakeVertex(i*0.01, 0, -0.01)
  Vertex_2 = geompy.MakeVertex(i*0.01, 0, 0.01)
  Line_1 = geompy.MakeLineTwoPnt(Vertex_1, Vertex_2)
  Extrusion_1 = geompy.MakePrismVecH2Ways(Line_1, OY, 0.003)
  geompy.Rotate(Extrusion_1, Line_1, angle*math.pi/180.0)

  baffles.append(Extrusion_1)

Compound_1 = geompy.MakeCompound(baffles)

geompy.ExportSTL(Compound_1, "constant/triSurface/baffles.stl", True, 0.001, True)
geompy.addToStudy( O, 'O' )
geompy.addToStudy( OX, 'OX' )
geompy.addToStudy( OY, 'OY' )
geompy.addToStudy( OZ, 'OZ' )
geompy.addToStudy( Vertex_1, 'Vertex_1' )
geompy.addToStudy( Vertex_2, 'Vertex_2' )
geompy.addToStudy( Line_1, 'Line_1' )
geompy.addToStudy( Extrusion_1, 'Extrusion_1' )


if salome.sg.hasDesktop():
  salome.sg.updateObjBrowser()
