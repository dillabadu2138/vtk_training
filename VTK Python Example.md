# VTK 파이썬 예제

* 실제 파이프라인 만들어 볼 것
  * **Reader** -> **Filter** -> **Mapper** -> **Actor** -> **Renderer** -> **RendererWindow**
* 클래스 레퍼런스 문서 보는법
  * 다이어그램
    * 상속(inheritance)
  * 상세 설명(Detailed Description)
  * 메소드(함수)



# Ex1) NetCDF 파일

## Step1) Reader

```python
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
#print(reader.GetOutput().GetPointData())
#print(reader.GetOutput().GetPointData().GetArray(0))
arrayName = reader.GetOutput().GetPointData().GetArrayName(0)
rangeStart, rangeEnd = reader.GetOutput().GetPointData().GetArray(0).GetRange()
print('%s의 범위는 %d에서 %d사이이다' % (arrayName, rangeStart, rangeEnd))
```

* `import vtk`로 VTK 파이썬 라이브러리 불러오기

* `vtk.vtkNetCDFCDFReader()` 클래스를 상속하는 reader 인스턴스를 생성
  
  * CF 규약을 따르는 NetCDF 파일만 읽음
  
* `__dir__()` 사용하여 속성과 메소드 정보를 리스트로 확인할 수 있음
  
  * VTK는 객체 지향 언어로서 객체 안에 많은 메소드 및 속성들이 은닉되어있음
  
* `__doc__` 또는 `__vtkname__` 사용하여 부모 클래스(superclass) 등의 정보 확인

* `SetSphericalCoordinates()` 메소드
  
  * Boolean 값 (0 또는 1)을 파라미터로 입력
  * **Paraview** GUI 프로그램의 Spherical Coordinates 선택박스와 같은 기능
  * 위경도로 이뤄진 2D/3D 데이터를 Sphercial coordinate로 읽을지 아니면 Cartesian coordiante로 읽을지 설정함
  
* `Update()` 메소드
  
  * 언제 사용될까?
    
    파이프라인이 Update 해주기를 기다리기 전에 객체를 사용해야하던지 등의 경우에 먼저 Update 하고싶을때 사용 (원래 actor를 renderer에 연결할 때, pipeline이 업데이트를 실행함)
    
    * 케이스1) `Update()` 적용 전후의 데이터셋 비교
    
    ```python
    import vtk
    vtk.vtkObject.GlobalWarningDisplayOff() # Disable the VTK warning window
    
    reader = vtk.vtkNetCDFCFReader()
    reader.SetFileName('files/etopo11.nc')
    reader.SetSphericalCoordinates(0)
    
    '''<reader를 Update하기 전>'''
    print(reader.GetOutput())
    
    '''<reader를 Update한 후>'''
    reader.Update()
    print(reader.GetOutput())
    ```
    
    * 케이스1) `Update()` 적용 전후의 데이터셋의 attributes 중 하나인 Point data 비교
    
    ```python
    import vtk
    vtk.vtkObject.GlobalWarningDisplayOff() # Disable the VTK warning window
    
    reader = vtk.vtkNetCDFCFReader()
    reader.SetFileName('files/etopo11.nc')
    reader.SetSphericalCoordinates(0)
    
    '''<reader를 Update하기 전>'''
    print(reader.GetOutput().GetPointData().GetArrayName(0))
    
    '''<reader를 Update한 후>'''
    reader.Update()
    print(reader.GetOutput().GetPointData().GetArrayName(0))
    ```
    
  * reader 인스턴스를 `Update()` 하기 전에는 reader가 아직 파일을 읽지 않은 것을 알 수 있지만, `Update()`를 적용 후에는 데이터셋에 접근할 수 있음.
  
* `GetOutput()` 메소드를 사용하여 데이터셋 확인
  
  * `print(reader.GetOutput())`
  
*  `GetPointData()` 메소드 사용하여 데이터셋의 attribute 중 하나인 point data를 출력
  
  * `print(reader.GetOutput().GetPointData())`
  
*  `vtk.vtkObject.GlobalWarningDisplayOff()`

  * VTK warning 메세지 윈도우 비활성화



## Step2) Filter(s)

```python
...

'''<Filter>'''
reader.GetOutput().GetPointData().SetActiveScalars(varName) # 'Active' Scalar 설정
warp = vtk.vtkWarpScalar()
warp.SetInputConnection(reader.GetOutputPort())
warp.SetNormal(0, 0, 1)
warp.SetScaleFactor(0.0002)
```

* `print(reader.GetOutPut().GetPointData())` 입력하여 데이터셋의 Point data attribute 다시 확인

  <img src="./images/ex2_img1.png" width="40%" height="30%"></img>

  * 디폴트로 활성화된 Scalar 또는 Vector가 없음을 알 수 있음
  * Array 갯 수는 하나이고 이름은 'Band1' 인 것을 알 수 있음
  * 'Band1' 이름을 가진 Array를 'Active' Scalar로 활성화 방법
    * `SetActiveScalars()` 메소드 사용
      * 입력 파라미터로는 활성화하고자 하는 Array의 문자열 지정
      * 예) `SetActiveScalars('Band1')`

* 파이프라인 연결 (Reader & Filter 연결)

  * `SetInputConnection()` 메소드
    * `B.SetInputConnection(A.GetOutputPort())`
    * A의 output 포트를 B의 Input 포트와 연결

* `vtkWarpScalar()` 필터

  * 클래스 레퍼런스 문서 확인
  * 2차원 좌표상의 스칼라(scalar) 값을 일정 방향으로 왜곡하여 3차원 생성

* `vtkwarpScalar()`의 `SetNormal()` 메소드

  * 어느 유닛벡터 방향으로 왜곡할지 설정
  * (0,0,1)이면 +z 축 방향을 의미함

* `vtkwarpScalar()`의 `SetScaleFactor()` 메소드

  * x & y는 단위가 degree인데 z는 -8430에서 3577사이의 m 단위이므로 상대적 스케일 조정이 필요



## Step3) Mapper & Actor

```python
...

'''<Mapper>'''
mapper = vtk.vtkDataSetMapper()
mapper.SetInputConnection(warp.GetOutputPort())
mapper.SetScalarRange(rangeStart, rangeEnd)

'''<Actor>'''
actor = vtk.vtkActor()
actor.SetMapper(mapper)
```

* `vtk.vtkDataSetMapper()` 클래스를 사용하여, mapper라는 인스턴스 생성
* 파이프라인 연결 (Filter & Mapper 연결)
  * `SetInputConnection()` 메소드
    * `B.SetInputConnection(A.GetOutputPort())`
    * A의 output 포트를 B의 Input 포트와 연결
* `vtk.vtkActor()` 클래스를 사용하여, actor라는 인스튼스 생성
* `SetMapper()` 메소드를 사용하여, mapper와 actor를 연결



## Step4) Renderer & RenderWindow 

```python
...

'''<Renderer>'''
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)
renderer.ResetCamera()

'''<RendererWindow>'''
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
```

* `vtk.vtkRenderer()` 클래스를 사용하여 renderer라는 인스턴스 생성
* `AddActor()` 메소드
  * actor를 renderer에 추가
* `SetBackground()` 메소드
  * 배경색 설정
  * 입력 파라미터 R, G, B
* `ResetCamera()` 메소드
  * 데이터에 맞게 화면 재설정
* `vtk.vtkRenderWindow()` 클래스를 사용하여 renderWindow라는 인스턴스 생성
* `AddRenderer()` 메소드
  * renderer를 renderWindow에 연결



## Step5) RenderWindowInteractor

```python
...

'''<RendererWindowInteractor>'''
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Start()
```

* `vtk.vtkRenderWindowInteractor()` 클래스를 사용하여 renderWindowInteracotr 인스턴스 생성
  * RenderWindowInteractor는 마우스 또는 키보드 이벤트와 같은 인터랙션 메커니즘을 제공

* `SetRenderWindow()` 메소드를 사용하여 RenderWindow 설정
* `Start()` 메소드로 이벤트 루프를 시작해야함.
  * 이벤트 루프(event loop)의 개념
    * 컴퓨터 과학 용어로서,
    * 프로그램의 이벤트를 대기하다가 디스패치(효율적으로 처리)하는 프로그래밍 구조체
    * 그래픽 유저 인터페이스에서 대부분 사용됨
    * 나중에 Qt 교육 시, 자세히 다룰 예정



## Step6) vtkWarpScalar() 클래스의 SetScaleFactor() 메소드의 입력 파라미터 변경

* 파이프라인을 연결하는 이유
* `vtkWarpScalar()`의 `SetScaleFactor()` 메소드의 파라미터 값을 변경하고 파이프라인을 실행해보시오.
  * Test cases - 1, 0.1, 0.01, 0.001
* Qt 라이브러리를 사용하여 이벤트 루프 개념이 적용된 프로그램을 만들면, GUI 상에서 Scale Factor 값을 사용자가 변경시 화면이 업데이트될 수 있게 할 수 있음
  * Qt 교육 시, vtk와 Qt를 연결하는 방법에 대해 다룰 예정



# Ex1) VTK 파일

## Step1) Reader

```python
import vtk

'''<Reader>'''
reader = vtk.vtkStructuredGridReader()
#print(reader.__dir__())
#print(reader.__doc__)
#print(reader.__vtkname__)
reader.SetFileName('files/output.vtk')
reader.Update()
#print(reader.GetOutput())
#'Active' Scalar 지정 또는 변경(이미 default로 되어있는 경우)
varName = reader.GetOutput().GetPointData().GetArrayName(0)
reader.GetOutput().GetPointData().SetActiveScalars(varName)
rangeStart, rangeEnd = reader.GetOutput().GetScalarRange()
# 출력 테스트
print('%s의 범위는 %d에서 %d사이이다' % (varName, rangeStart, rangeEnd))
```

* `import vtk`로 VTK 파이썬 라이브러리 불러오기
* `vtk.vtkStructuredGridReader()` 클래스를 상속하는 reader 인스턴스를 생성
* `__dir__()` 
* `__doc__` 
* `__vtkname__` 
* `SetFileName()` 메소드
* `Update()` 메소드

  * 언제 사용될까?
* 파이프라인이 Update 해주기를 기다리기 전에 객체를 사용해야하던지 등의 경우에 먼저 Update 하고싶을때 사용 (원래 actor를 renderer에 연결할 때, pipeline이 업데이트를 실행함)
  * 이 경우에는 'Active'한 Scalar를 변경해야하기 때문에 Update()를 파이프라인에 앞서 먼저함 
* `print(reader.GetOutput().GetPointData().__doc__)`
* `reader.GetOutput().GetPointData()`의 상속 클래스는 `vtkDataSetAttributes()`

* `vtkDataSetAttributes()` 클래스의 `SetActiveScalars()` 메소드
  * 'Active' Scalar를 설정
  * 입력 파라미터로는 활성화하고자 하는 Array의 문자열 지정



## Step2) Filter(s)

```python
...

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
```

* `print(reader.GetOutPut().GetPointData())` 입력하여 데이터셋의 Point data attribute 다시 확인
* 디폴트로 현재 활성화된 'Active' Scalar는 temp라는 것을 알 수 있음
  * point data의 기타 Array로는 salt가 있다는 것을 알 수 있음
* `vtkTransformFilter()` 필터
* 클래스 레퍼런스 문서 확인
* `vtkThreshold()` 필터
* 클래스 레퍼런스 문서 확인
* 파이프라인 연결 (Reader와 Filter의 연결 & Filter와 Filter의 연결)
* `SetInputConnection()` 메소드
    * `B.SetInputConnection(A.GetOutputPort())`
    * A의 output 포트를 B의 Input 포트와 연결



## Step3) Mapper & Actor

```python
...

'''<Mapper>'''
mapper = vtk.vtkDataSetMapper()
mapper.SetInputConnection(Filter2.GetOutputPort())
mapper.SetScalarRange(reader.GetOutput().GetScalarRange())

'''<Actor>'''
actor = vtk.vtkActor()
actor.SetMapper(mapper)
```

* `vtk.vtkDataSetMapper()` 클래스를 사용하여, mapper라는 인스턴스 생성
* 파이프라인 연결 (Filter와 Mapper의 연결)
  * `SetInputConnection()` 메소드
    * `B.SetInputConnection(A.GetOutputPort())`
    * A의 output 포트를 B의 Input 포트와 연결
* `vtk.vtkActor()` 클래스를 사용하여, actor라는 인스튼스 생성
* `SetMapper()` 메소드를 사용하여, mapper와 actor를 연결



## Step4) Renderer & RenderWindow 

```python
...

'''<Renderer>'''
renderer = vtk.vtkRenderer()
renderer.AddActor(actor)
renderer.SetBackground(1, 1, 1)
renderer.ResetCamera()

'''<RendererWindow>'''
renderWindow = vtk.vtkRenderWindow()
renderWindow.AddRenderer(renderer)
```

* `vtk.vtkRenderer()` 클래스를 사용하여 renderer라는 인스턴스 생성
* `AddActor()` 메소드
  * actor를 renderer에 추가
* `SetBackground()` 메소드
  * 배경색 설정
  * 입력 파라미터 R, G, B
* `ResetCamera()` 메소드
  * 데이터에 맞게 화면 재설정
* `vtk.vtkRenderWindow()` 클래스를 사용하여 renderWindow라는 인스턴스 생성
* `AddRenderer()` 메소드
  * renderer를 renderWindow에 연결



## Step5) RenderWindowInteractor

```python
...

'''<RendererWindowInteractor>'''
renderWindowInteractor = vtk.vtkRenderWindowInteractor()
renderWindowInteractor.SetRenderWindow(renderWindow)
renderWindowInteractor.Start()
```

* `vtk.vtkRenderWindowInteractor()` 클래스를 사용하여 renderWindowInteracotr 인스턴스 생성
  * RenderWindowInteractor는 마우스 또는 키보드 이벤트와 같은 인터랙션 메커니즘을 제공

* `SetRenderWindow()` 메소드를 사용하여 RenderWindow 설정
* `Start()` 메소드로 이벤트 루프를 시작해야함.
  * 이벤트 루프(event loop)의 개념
    * 컴퓨터 과학 용어로서,
    * 프로그램의 이벤트를 대기하다가 디스패치(효율적으로 처리)하는 프로그래밍 구조체
    * 그래픽 유저 인터페이스에서 대부분 사용됨
    * 나중에 Qt 교육 시, 자세히 다룰 예정



## Step6) 'Active' Scalar를 temp에서 salt로 변경

```python
varName = reader.GetOutput().GetPointData().GetArrayName(1)
reader.GetOutput().GetPointData().SetActiveScalars(varName)
```

* `GetArrayName()` 메소드
  * 입력 파라미터로 array의 index 입력
  * 1로 변경해보시오