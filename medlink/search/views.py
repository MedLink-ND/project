#from django.contrib.auth import authenticate, login as auth_login, get_user_model
#from django.shortcuts import redirect, render
#from django.http import HttpResponse, HttpResponseRedirect
#from .forms import LoginForm, HospitalProfileForm
from django.shortcuts import render

# ADD IMPORT JOB OBJECTS

def FilterView(request):
        #qs = Job.objects.all()
        location_contains_query = request.GET.get('location_contains')
        print(location_contains)

        #if location_contains_query != '' and location_contains_query is not Noe:
            #qs = qs.filter(title__icontains=title_contains_query)


        return render(request, "filter.html")