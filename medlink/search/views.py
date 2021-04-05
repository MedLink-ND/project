#from django.contrib.auth import authenticate, login as auth_login, get_user_model
#from django.shortcuts import redirect, render
#from django.http import HttpResponse, HttpResponseRedirect
#from .forms import LoginForm, HospitalProfileForm
from django.shortcuts import render

def FilterView(request):
        location_contains = request.GET.get('location_contains')
        print(location_contains)
        return render(request, "filter.html")