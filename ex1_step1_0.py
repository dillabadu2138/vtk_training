import vtk
vtk.vtkObject.GlobalWarningDisplayOff() # Disable the VTK warning window

'''<Reader>'''
reader = vtk.vtkNetCDFCFReader()
#print(reader.__dir__())
#print(reader.__doc__)
#print(reader.__vtkname__)
reader.SetFileName('files/etopo11.nc')
reader.SetSphericalCoordinates(0)
reader.Update()
#print(reader.GetOutput())
#print(reader.__doc__)
#print(reader.GetOutput().__doc__)
#print(reader.GetOutput().GetPointData().__doc__)
#print(reader.GetOutput().GetPointData().GetArray(0))
#print(reader.GetOutput().GetPointData().GetArray(0).GetRange())
varName = reader.GetOutput().GetPointData().GetArrayName(0)
rangeStart, rangeEnd = reader.GetOutput().GetPointData().GetArray(0).GetRange()
print('%s의 범위는 %d에서 %d사이이다' % (varName, rangeStart, rangeEnd))
