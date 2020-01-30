import vtk
vtk.vtkObject.GlobalWarningDisplayOff() # Disable the VTK warning window

reader = vtk.vtkNetCDFCFReader()
reader.SetFileName('files/etopo11.nc')
reader.SetSphericalCoordinates(0)

'''<reader를 Update하기 전>'''
print(reader.GetOutput().GetPointData().GetArrayName(0))


'''<readr를 Update한 후>'''
reader.Update()
print(reader.GetOutput().GetPointData().GetArrayName(0))
