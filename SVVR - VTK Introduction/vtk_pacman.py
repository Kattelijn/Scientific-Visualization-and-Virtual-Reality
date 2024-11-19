#!/usr/bin/env vtkpython

import sys
import os
import vtk

# Window width and height
WIDTH=800
HEIGHT=800

v = vtk.vtkVersion()
version = v.GetVTKSourceVersion()
print(version)

def main(argv):

  sphere = vtk.vtkSphereSource()
  sphere.SetEndTheta(315)
  sphere.SetThetaResolution(100)

  ren = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  renWin.SetSize(WIDTH, HEIGHT)

  # create a renderwindowinteractor
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(sphere.GetOutputPort())

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)

  ren.AddActor(actor)

  iren.Initialize()
  iren.Start()

main(sys.argv)
