from django.urls import path
from django.conf.urls import url
# from home.forms import JobCreationForm1, JobCreationForm2
# from home.views import ContactWizard

from . import views

urlpatterns = [
    path('hospital/', views.home_hospital, name='home_hospital'),
    path('user/', views.home_user, name="home_user"),
    url(r'user/job_details/(?P<job_id>\d+)/$', views.user_job_details,),
    path('user/preference/', views.user_job_preference,),
    url(r'hospital/hospital_job_details/(?P<job_id>\d+)/find_workers/', views.find_workers, name="find_workers"),
    url(r'hospital/hospital_job_details/(?P<job_id>\d+)/$', views.hospital_job_details, name="hospital_job_details"),
    url(r'hospital/hospital_job_details/(?P<job_id>\d+)/reject/(?P<user_id>\d+)/$', views.hospital_reject_applicant),
    url(r'hospital/hospital_job_details/(?P<job_id>\d+)/accept/(?P<user_id>\d+)/$', views.hospital_accept_applicant),
    url(r'hospital/delete/(?P<job_id>\d+)/$', views.hospital_delete_job,),
    path('hospital/post_job/', views.hospital_post_job, name='home/hospital/post_job'),
    path(r'worker_query/', views.worker_query, name='worker_query'),
    url(r'hospital/update/(?P<job_id>\d+)/$', views.hospital_update_job,),    
    path(r'hospital/profile_update/', views.profile_update, name='profile_update'), 
    path(r'user/update_profile/', views.worker_profile_update, name='update_profile'),   
    path(r'logout/', views.logout_request, name='logout'),    
    path(r'switch/', views.switch_request, name='switch'),    
    path(r'job_query/', views.job_query, name='job_query'),
    url(r'job_query/application/(?P<job_id>\d+)/$', views.application),
    path(r'logout', views.logout_request, name="logout"),
    path(r'profile_page/<int:profile_id>', views.profile_page, name="profile_page"),
    path(r'applications', views.applications, name="applications")
]
