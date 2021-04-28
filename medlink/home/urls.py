from django.urls import path
from django.conf.urls import url
# from home.forms import JobCreationForm1, JobCreationForm2
# from home.views import ContactWizard

from . import views

urlpatterns = [
    path('hospital/', views.home_hospital, name='home/hospital'),
    path('user/', views.home_user,),
    url(r'user/job_details/(?P<job_id>\d+)/$', views.user_job_details,),
    path('user/preference/', views.user_job_preference,),
    url(r'hospital/delete/(?P<job_id>\d+)/$', views.hospital_delete_job,),
    path('hospital/post_job/', views.hospital_post_job, name='home/hospital/post_job'),
    url(r'hospital/update/(?P<job_id>\d+)/$', views.hospital_update_job,),    
    path(r'hospital/profile_update/', views.profile_update, name='profile_update'), 
    path(r'worker/profile_update/', views.worker_profile_update, name='worker_profile_update'),   
    path(r'logout/', views.logout_request, name='logout'),    
    path(r'job_query/', views.job_query, name='job_query'),
    url(r'job_query/application/(?P<job_id>\d+)/$', views.application),
    path(r'logout', views.logout_request, name="logout")
]
