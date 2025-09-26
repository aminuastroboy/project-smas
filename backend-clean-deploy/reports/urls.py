from django.urls import path
from . import views
urlpatterns = [
    path('send/<int:class_id>/', views.send_reports, name='send-reports'),
    path('status/<str:task_id>/', views.report_status, name='report-status'),
]
