from django.urls import path
from .views import job_list_view, job_detail_view

urlpatterns = [
    path('jobs/', job_list_view, name='job-list'),
    path('jobs/<int:pk>', job_detail_view, name='job-detail')
]
