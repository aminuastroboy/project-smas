from django.urls import path
from . import views
urlpatterns = [
    path('me/', views.MeView.as_view(), name='me'),
    path('students/', views.StudentList.as_view(), name='students'),
    path('students/<int:pk>/', views.StudentDetail.as_view(), name='student_detail'),
    path('students/<int:pk>/results/', views.StudentResults.as_view(), name='student_results'),
]
