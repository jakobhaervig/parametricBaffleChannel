#!/usr/bin/env python

###
### This file is generated automatically by SALOME v9.14.0 with dump python functionality
###

import sys
import salome

def salome_init():
    salome.salome_init()
    import salome_notebook
    notebook = salome_notebook.NoteBook()
    import GEOM
    from salome.geom import geomBuilder
    import math
    import SALOMEDS

def create_baffle(pos, angle, height, width):
    """
    Create a baffle with the given position, angle, height, and width.
    """
    geompy = geomBuilder.New()
    O = geompy.MakeVertex(0, 0, 0)
    OX = geompy.MakeVectorDXDYDZ(1, 0, 0)
    OY = geompy.MakeVectorDXDYDZ(0, 1, 0)
    OZ = geompy.MakeVectorDXDYDZ(0, 0, 1)
    
    baffle = geompy.MakeFaceHW(width, height, 1)
    geompy.Rotate(baffle, OY, angle * math.pi / 180.0)
    geompy.TranslateDXDYDZ(baffle, pos[0], pos[1], pos[2])
    
    return baffle

def export_baffle_to_stl(baffle, filename, binary=True, tolerance=0.001):
    """
    Export the baffle to an STL file.
    """
    geompy = geomBuilder.New()
    geompy.ExportSTL(baffle, filename, binary, tolerance, True)

if __name__ == "__main__":

    # Initialize the environment
    salome_init()

    # Create a baffle
    baffle = create_baffle((1, 0, 0), 45, 1, 1)

    # Export the baffle to an STL file
    export_baffle_to_stl(baffle, "baffle.stl", True, 0.001)