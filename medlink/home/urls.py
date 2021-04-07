from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path(r'job_query/', views.job_query, name='job_query')
]
