from django.urls import path
from .views import SubmitExamView, GetMyResultsView
urlpatterns = [
    path('<int:exam_id>/submit/', SubmitExamView.as_view(), name='submit_exam'),
    path('my-results/', GetMyResultsView.as_view(), name='my_results'),
]
