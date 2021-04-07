from django.urls import path

from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path(r'hospital_profile_creation/', views.hospital_profile_creation, name='hospital_login'),    
]
