from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import JobCreationForm, JobSearchForm
from .models import JobInfo

# Create your views here.
def home(request):
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        user = request.user
    
        if form.is_valid():
            cd = form.cleaned_data
            job_name = cd['job_name']
            job_level = cd['job_level']
            job_description = cd['job_description']
            job_location_hospital = cd['job_location_hospital']
            job_location_city = cd['job_location_city']

            job_info = JobInfo(
                job_name=job_name,
                job_level=job_level,
                job_description=job_description,
                job_location_hospital=job_location_hospital,
                job_location_city=job_location_city,
                base_profile=user,
            )

            job_info.save()

    else:
        form = JobCreationForm()

    return render(request, 'home.html', {'form': form})


def job_query(request):
    qs = JobInfo.objects.all()
    context = {}
    if request.method == 'GET':
        form = JobSearchForm(request.GET)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            location_contains_query = cd['location_contains']

            if location_contains_query != '' and location_contains_query is not None:
                qs = qs.filter(job_location_hospital__icontains=location_contains_query)

            
    else:
        form = JobSearchForm()

    context['queryset']= qs
    #context['form'] = form

    return render(request, "job_query.html", context)