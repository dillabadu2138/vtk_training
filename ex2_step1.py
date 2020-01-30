import vtk

'''<Reader>'''
reader = vtk.vtkStructuredGridReader()
#print(reader.__dir__())
#print(reader.__doc__)
#print(reader.__vtkname__)
reader.SetFileName('files/output.vtk')
reader.Update()
#print(reader.GetOutput())
print(reader.GetOutput().GetPointData().__doc__)
#'Active' Scalar 지정 또는 변경(이미 default로 되어있는 경우)
varName = reader.GetOutput().GetPointData().GetArrayName(0)
reader.GetOutput().GetPointData().SetActiveScalars(varName)
rangeStart, rangeEnd = reader.GetOutput().GetScalarRange()
# 출력 테스트
print('%s의 범위는 %d에서 %d사이이다' % (varName, rangeStart, rangeEnd))
