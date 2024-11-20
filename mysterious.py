import sys
import os
import vtk

def main(argv):
    
    filename = argv[1]

    if not os.path.exists(filename):
        sys.stderr.write("file '%s' not found\n" % filename)
        return 1

    reader = vtk.vtkDataSetReader()
    reader.SetFileName(filename)
    reader.Update()

    data = reader.GetOutput()

    print(data)

main(sys.argv)
