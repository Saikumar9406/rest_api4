from django.urls import path,include
from . import api
from rest_framework.routers import DefaultRouter
#from .api import studentviewset
router=DefaultRouter()
router.register('student',api.studentviewset,basename='student')
router.register('student_generic',api.studentgenericviewset,basename='student')
router.register('studentmodelviewset',api.studentmodelviewset,basename='student')
urlpatterns=[
    path('modelviewset/',include(router.urls)),
    path('genericviewset/',include(router.urls)),
    path('viewset/',include(router.urls)),
    path('viewset/<int:id>/',include(router.urls)),
    path('student_list',api.studentlist,name='student_list'),
    path('update/<int:id>/',api.updatestudent,name='update'),
    path('studentlist',api.student_list,name='studentlist'),
    path('update_/<int:id>/',api.update_student,name='update'),
    path('classbasedapi',api.studentapiview.as_view(),name='classbasedapi'),
    path('updateclassbasedapi/<int:id>/',api.updatestudentapiview.as_view(),name='updateclassbasedapi'),
    path('genericviews',api.studentgenericview.as_view(),name='genericview'),
    path('genericviews/<int:id>/',api.studentgenericview.as_view(),name='genericview'),
    path('authentication',api.userauthentication.as_view(),name='authentication'),

]