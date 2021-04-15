from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth import logout
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import JobCreationForm, JobSearchForm, ProfileUpdateHospitalForm, JobUpdateForm
from .models import JobInfo

User = get_user_model()

# Create your views here.
def home_hospital(request):
    user = get_user_model()
    currUser = user.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')

    allJobs = []
    existingJob = None
    try:
        for existingJob in JobInfo.objects.filter(base_profile_id=currUserID):
            allJobs.append(existingJob)
        print('Job found')
    except JobInfo.DoesNotExist:
        print("user is ok, no existing job")
    except MultipleObjectsReturned:
        return redirect('failure/')

    return render(request, 'home_hospital.html', {'existingJob': allJobs})

def hospital_post_job(request):
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        user = request.user
        # print(user.is_hospital)
        if user.is_hospital:
            if form.is_valid():
                cd = form.cleaned_data
                job_name = cd['job_name']
                job_description = cd['job_description']
                job_location_hospital = cd['job_location_hospital']
                job_location_city = cd['job_location_city']

                job_info = JobInfo(
                    job_name=job_name,
                    job_description=job_description,
                    job_location_hospital=job_location_hospital,
                    job_location_city=job_location_city,
                    base_profile=user,
                )

                job_info.save()

    else:
        form = JobCreationForm()

    return render(request, 'create_job.html', {'form': form})


def profile_update(request):
    curr_user = User.objects.filter(email=request.user.email)
    if request.method == 'POST':
        form = ProfileUpdateHospitalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            hospital_name = cd['hospital_name']

        curr_user.update(first_name=first_name, last_name=last_name, hospital_name=hospital_name)
    
    else:
        form = ProfileUpdateHospitalForm()

    return render(request, 'profile_update.html', {'form': form})


def log_out(request):
    logout(request)


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

def hospital_delete_job(request, job_id):
    job = JobInfo.objects.filter(id=job_id)
    job.delete()

    return redirect("../../")

def hospital_update_job(request, job_id):
    job = JobInfo.objects.filter(id=job_id)
    if request.method == 'POST':
        form = JobUpdateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            job_name = cd['job_name']
            job_level = cd['job_level']
            job_description = cd['job_description']
            job_location_hospital = cd['job_location_hospital']
            job_location_city = cd['job_location_city']

        job.update(
            job_name=job_name,
            job_level=job_level,
            job_description=job_description,
            job_location_hospital=job_location_hospital,
            job_location_city=job_location_city,
        )
    
    else:
        form = JobUpdateForm()
    
    return render(request, 'job_update.html', {'form': form})
