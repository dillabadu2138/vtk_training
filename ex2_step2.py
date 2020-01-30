import vtk

'''<Reader>'''
reader = vtk.vtkStructuredGridReader()
reader.SetFileName('files/output.vtk')
reader.Update()
# 'Active' Scalar 지정 또는 변경(이미 default로 되어있는 경우)
varName = reader.GetOutput().GetPointData().GetArrayName(1)
reader.GetOutput().GetPointData().SetActiveScalars(varName)
rangeStart, rangeEnd = reader.GetOutput().GetScalarRange()

'''<Filter 1>'''
transformation = vtk.vtkTransform()
transformation.Scale(1, 1, 0.001)

Filter1 = vtk.vtkTransformFilter()
Filter1.SetInputConnection(reader.GetOutputPort())
Filter1.SetTransform(transformation)

'''<Filter 2>'''
Filter2 = vtk.vtkThreshold()
Filter2.ThresholdBetween(rangeStart, rangeEnd)
Filter2.SetInputConnection(Filter1.GetOutputPort())
