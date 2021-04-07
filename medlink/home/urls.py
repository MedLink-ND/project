from django.urls import path

from . import views

urlpatterns = [
    path('hospital/', views.home_hospital, name='home/hospital'),
    path('hospital/post_job/', views.hospital_post_job, name='home/hospital/post_job'),
    path(r'profile_update/', views.profile_update, name='profile_update'),    
    path(r'logout/', views.log_out, name='logout'),    
    path(r'job_query/', views.job_query, name='job_query')
]
