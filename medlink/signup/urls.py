from django.conf.urls import url
from django.urls import path

from . import views

urlpatterns = [
    path(r'worker', views.worker_signup, name='worker_signup'),
    path(r'hospital', views.hospital_signup, name='hospital_signup'),
    path(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        views.activate, name='activate'),
    path(r'confirmation/', views.confirmation, name='confirmation'),
    url(r'signup-success/', views.signup_success, name='signup_success'),
]
