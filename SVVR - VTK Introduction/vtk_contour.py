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
  if len(argv) < 2:
    sys.stderr.write("Usage: %s <volume.vtk> [contourvalue]\n" % argv[0])
    return 1

  filename = argv[1]

  if not os.path.exists(filename):
    sys.stderr.write("file '%s' not found\n" % filename)
    return 1

  reader = vtk.vtkDataSetReader()
  reader.SetFileName(filename)
  reader.Update()

  data = reader.GetOutput()
  print("Dimensions   : ", data.GetDimensions())
  print("Scalar range : ", data.GetScalarRange())
  srange = data.GetScalarRange()

  if len(argv) == 3:
    value = int(argv[2])
  else:
    value = (srange[1] - srange[0])/2

  ren = vtk.vtkRenderer()
  renWin = vtk.vtkRenderWindow()
  renWin.AddRenderer(ren)
  renWin.SetSize(WIDTH, HEIGHT)

  # create a renderwindowinteractor
  iren = vtk.vtkRenderWindowInteractor()
  iren.SetRenderWindow(renWin)

  # Contour pipeline:
  contour = vtk.vtkContourFilter()
  contour.SetInputConnection(reader.GetOutputPort())
  contour.ComputeScalarsOff() ;# the default is to generate scalars
  contour.SetValue(0, 1)

  mapper = vtk.vtkPolyDataMapper()
  mapper.SetInputConnection(contour.GetOutputPort())

  actor = vtk.vtkActor()
  actor.SetMapper(mapper)

  ren.AddActor(actor)

  # First, the representation of the slider:
  slider_rep = vtk.vtkSliderRepresentation2D()
  slider_rep.SetMinimumValue(1)
  slider_rep.SetMaximumValue(3000)
  slider_rep.SetValue(1) ;# default value, same as set above
  #slider_rep.SetTitleText("Resolution")
  slider_rep.GetPoint1Coordinate().SetCoordinateSystemToNormalizedDisplay()
  slider_rep.GetPoint1Coordinate().SetValue(0.3, 0.05)
  slider_rep.GetPoint2Coordinate().SetCoordinateSystemToNormalizedDisplay()
  slider_rep.GetPoint2Coordinate().SetValue(0.7, 0.05)
  slider_rep.SetSliderLength(0.02)
  slider_rep.SetSliderWidth(0.03)
  slider_rep.SetEndCapLength(0.01)
  slider_rep.SetEndCapWidth(0.03)
  slider_rep.SetTubeWidth(0.005)
  slider_rep.SetLabelFormat("%3.0lf")
  slider_rep.SetTitleHeight(0.02)
  slider_rep.SetLabelHeight(0.02)

  # The slider (see https://vtk.org/doc/nightly/html/classvtkSliderWidget.html):
  slider = vtk.vtkSliderWidget()
  slider.SetInteractor(iren)
  slider.SetRepresentation(slider_rep)
  slider.KeyPressActivationOff()
  slider.SetAnimationModeToAnimate()
  slider.SetEnabled(True)

  # Define what to do if the slider value changed:
  def processEndInteractionEvent(obj,event):
    value = int (obj.GetRepresentation().GetValue())
    contour.SetValue(0, value)

  #slider.AddObserver("EndInteractionEvent", processEndInteractionEvent) ;# change value only when released
  slider.AddObserver("InteractionEvent", processEndInteractionEvent) ;# change value when moved

  iren.Initialize()
  iren.Start()

main(sys.argv)
