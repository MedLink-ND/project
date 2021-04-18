from django.urls import path
from django.conf.urls import url
# from home.forms import JobCreationForm1, JobCreationForm2
# from home.views import ContactWizard

from . import views

urlpatterns = [
    path('hospital/', views.home_hospital, name='home/hospital'),
    url(r'hospital/delete/(?P<job_id>\d+)/$', views.hospital_delete_job,),
    path('hospital/post_job/', views.hospital_post_job, name='home/hospital/post_job'),
    # path('hospital/post_job/', ontactWizard.as_view([JobCreationForm1, JobCreationForm2])),
    url(r'hospital/update/(?P<job_id>\d+)/$', views.hospital_update_job,),    
    path(r'hospital/profile_update/', views.profile_update, name='profile_update'),    
    path(r'logout/', views.log_out, name='logout'),    
    path(r'job_query/', views.job_query, name='job_query'),
]
