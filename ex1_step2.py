import vtk
vtk.vtkObject.GlobalWarningDisplayOff() # Disable the VTK warning window

'''<Reader>'''
reader = vtk.vtkNetCDFCFReader()
reader.SetFileName('files/etopo11.nc')
reader.SetSphericalCoordinates(0) 
reader.Update()
varName = reader.GetOutput().GetPointData().GetArrayName(0)
rangeStart, rangeEnd = reader.GetOutput().GetPointData().GetArray(0).GetRange()

'''<Filter>'''
reader.GetOutput().GetPointData().SetActiveScalars(varName) # 'Active' Scalar 설정
warp = vtk.vtkWarpScalar()
warp.SetInputConnection(activeScalar.GetOutputPort())
warp.SetNormal(0, 0, 1)
warp.SetScaleFactor(0.0002)
