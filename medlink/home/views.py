from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth import logout
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import JobCreationForm, JobSearchForm, ProfileUpdateHospitalForm, JobUpdateForm, ProfileUpdateWorkerForm
from .models import JobInfo, WorkerInfo

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
                job_type = cd['job_type']
                job_location_zipcode = cd['job_location_zipcode']
                job_location_hospital = cd['job_location_hospital']
                hospital_type = cd['hospital_type']
                job_on_call = cd['job_on_call']
                job_start_time = cd['job_start_time']
                job_end_time = cd['job_end_time']
                locum_shift_day = cd['locum_shift_day']
                locum_shift_hour = cd['locum_shift_hour']
                job_experience = cd['job_experience']
                job_supervision = cd['job_supervision']
                job_payment = cd['job_payment']
                job_vacation = cd['job_vacation']
                education_money = cd['education_money']

                job_info = JobInfo(
                    job_name=job_name,
                    job_type=job_type,
                    job_location_zipcode=job_location_zipcode,
                    job_location_hospital=job_location_hospital,
                    hospital_type=hospital_type,
                    job_on_call=job_on_call,
                    job_start_time=job_start_time,
                    job_end_time=job_end_time,
                    locum_shift_day=locum_shift_day,
                    locum_shift_hour=locum_shift_hour,
                    job_experience=job_experience,
                    job_supervision=job_supervision,
                    job_payment=job_payment,
                    job_vacation=job_vacation,
                    education_money=education_money,
                    base_profile=user,
                )

                job_info.save()

    else:
        form = JobCreationForm()

    return render(request, 'create_job.html', {'form': form})


def profile_update(request):
    curr_user = User.objects.filter(email=request.user.email)

    if curr_user.worker:
        return worker_profile_update(request)
        
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

def worker_profile_update(request):
    if request.method == 'POST':
        user = request.user
        form = ProfileUpdateWorkerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
        name = cd['name']
        address = cd['address']
        email = cd['email']
        education = cd['education']
        certifications = cd['certifications']
        provider_type = cd['provider_type']
        peer_references = cd['peer_references']
        cpr_certifications = cd['cpr_certifications']

        worker_info = WorkerInfo(
                    name=name,
                    address=address,
                    email=email,
                    education=education,
                    certifications=certifications,
                    provider_type=provider_type,
                    peer_references=peer_references,
                    cpr_certifications=cpr_certifications,
                    base_profile=user,
        )
        
        previous_info = WorkerInfo.objects.filter(base_profile_id=user.id)
        previous_info.delete()

        worker_info.save()
    
    else:
        form = ProfileUpdateWorkerForm()

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
            level_contains_query = cd['level_contains']
            description_contains_query = cd['description_contains']

            if location_contains_query != '' and location_contains_query is not None:
                qs = qs.filter(job_location_hospital__icontains=location_contains_query)
                qs = qs.filter(job_location_city__icontains=location_contains_query)

            if level_contains_query != '' and level_contains_query is not None:
                qs = qs.filter(job_level__icontains=level_contains_query)

            if description_contains_query != '' and description_contains_query is not None:
                qs = qs.filter(job_description__icontains=description_contains_query)
            
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
    job = JobInfo.objects.get(id=job_id)
    if request.method == 'POST':
        form = JobUpdateForm(request.POST)
        new_fields = []
        if form.is_valid():
            cd = form.cleaned_data
            for field in cd:
                if cd[field]:
                    new_fields.append(field)

            job.job_name = cd['job_name']
            job.job_type = cd['job_type']
            job.job_location_zipcode = cd['job_location_zipcode']
            job.job_location_hospital = cd['job_location_hospital']
            job.hospital_type = cd['hospital_type']
            job.job_on_call = cd['job_on_call']
            job.job_start_time = cd['job_start_time']
            job.job_end_time = cd['job_end_time']
            job.locum_shift_day = cd['locum_shift_day']
            job.locum_shift_hour = cd['locum_shift_hour']
            job.job_experience = cd['job_experience']
            job.job_supervision = cd['job_supervision']
            job.job_payment = cd['job_payment']
            job.job_vacation = cd['job_vacation']
            job.education_money = cd['education_money']

        job.save(update_fields=new_fields)
    
    else:
        form = JobUpdateForm()
    
    return render(request, 'job_update.html', {'form': form, 'job': job})
