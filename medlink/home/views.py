from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth import logout
from django.core.exceptions import MultipleObjectsReturned
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import JobCreationForm, JobSearchForm, ProfileUpdateHospitalForm, JobUpdateForm
from .models import JobInfo, JobApplicants
import datetime

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
            #location_contains_query = cd['location_contains']
            zip_contains_query = cd['zip_contains']
            #level_contains_query = cd['level_contains']
            description_contains_query = cd['description_contains']
            ### new queries
            type_contains_query = cd['type_contains']
            hospital_contains_query = cd['hospital_contains']
            hospital_type_contains_query = cd['hospital_type_contains']
            on_call_contains_query = cd['on_call_contains']
            experience_contains_query = cd['experience_contains']
            supervision_contains_query = cd['supervision_contains']
            payment_contains_query = cd['payment_contains']
            vacation_contains_query = cd['vacation_contains']
            education_money_contains_query = cd['education_money_contains']

            ### by location
            if zip_contains_query != '' and zip_contains_query is not None:
                #qs = qs.filter(job_location_hospital__icontains=location_contains_query)
                qs = qs.filter(job_location_zipcode__icontains=zip_contains_query)

            #if level_contains_query != '' and level_contains_query is not None:
            #    qs = qs.filter(job_level__icontains=level_contains_query)

            if description_contains_query != '' and description_contains_query is not None:
                qs = qs.filter(job_description__icontains=description_contains_query)

            ### new queries
            if type_contains_query != '' and type_contains_query is not None:
                qs = qs.filter(job_type__icontains=type_contains_query)

            if hospital_contains_query != '' and hospital_contains_query is not None:
                qs = qs.filter(job_hospital__icontains=hospital_contains_query)

            if hospital_type_contains_query != '' and hospital_type_contains_query is not None:
                qs = qs.filter(hospital_type__icontains=hospital_type_contains_query)

            if on_call_contains_query != '' and on_call_contains_query is not None:
                qs = qs.filter(job_on_call__icontains=on_call_contains_query)

            if experience_contains_query != '' and experience_contains_query is not None:
                qs = qs.filter(job_experience__icontains=experience_contains_query)
            
            if supervision_contains_query != '' and supervision_contains_query is not None:
                qs = qs.filter(job_supervision__icontains=supervision_contains_query)

            if payment_contains_query != '' and payment_contains_query is not None:
                qs = qs.filter(job_payment__icontains=payment_contains_query)

            if vacation_contains_query != '' and vacation_contains_query is not None:
                qs = qs.filter(job_vacation__icontains=vacation_contains_query)

            if education_money_contains_query != '' and education_money_contains_query is not None:
                qs = qs.filter(education_money__icontains=education_money_contains_query)

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


def application(request, job_id):
    job = JobInfo.objects.filter(id=job_id)[0]
    user = get_user_model()
    currUser = user.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')

    #application_info = JobApplicants(
    #    job_id = job,
    #    user_id = currUserID,
        #application_date = datetime.date()
    #)

    JobApplicants.objects.create(user_id=currUserID, job_id=job)


    #application_info.save()
    #job = JobInfo.objects.filter(id=job_id)

    #if request.method == 'POST':
        #form = ApplicationCreationForm(request.POST)
        
        
        
        #form = ProfileUpdateForm(request.POST)
        # ADD LATER TODO: see profile
        # if form.is_valid():

    ### Connect worker to job
    # job.update(job_applicant = user)
    
    ### when click applies url with job id again and user id and send email

    return render(request, 'application.html')
