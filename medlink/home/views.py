import datetime
from .models import JobInfo, JobApplicants
from .forms import JobCreationForm, JobSearchForm, ProfileUpdateHospitalForm, JobUpdateForm
from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.auth import logout
from django.core.exceptions import MultipleObjectsReturned
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render

# For application email
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage

from .forms import JobCreationForm, JobPreferenceForm, JobPreferenceUpdateForm, \
    JobSearchForm, WorkerSearchForm, JobUpdateForm, ProfileUpdateHospitalForm, ProfileUpdateWorkerForm
from .models import JobInfo, JobPreference, WorkerInfo, WorkerProfileInfo

import googlemaps
import requests
import responses

import pprint

gmaps = googlemaps.Client(key='AIzaSyAZ2ZbOptR7Xx5OIsL_33tZ_30n9cD0f7c')


User = get_user_model()


def home_user(request):
    user = request.user

    user_preference = None
    user_preference = JobPreference.objects.filter(base_profile=user.id)
    if user_preference:
        user_preference = user_preference[0]
    print(user_preference)

    all_jobs = JobInfo.objects.all()
    context = {}

    if not user_preference:
        context['job_rec'] = None
    else:
        user_job_type = user_preference.job_type
        if user_preference.job_location_radius == 'No preference':
            user_job_radius = 10000000
        else:
            user_job_radius = int(user_preference.job_location_radius)
        user_location_lat = user_preference.home_location_lat
        user_location_lng = user_preference.home_location_lng

        job_rec = None

        if user_job_type == 'No preference':
            job_rec = all_jobs
        else:
            job_rec = all_jobs.filter(job_type=user_job_type)

        job_rec_distance_filtered = []

        if len(job_rec) > 0:
            for job in job_rec:
                job_zip = job.job_location_zipcode
                geo_res = gmap_to_zip(gmaps.geocode(job_zip))
                lat, lng = geo_res['lat'], geo_res['lng']
                if lat == -1 and lng == -1:
                    continue
                else:
                    origin = (user_location_lat, user_location_lng)
                    destination = (lat, lng)
                    distance = distance_bt_locations(origin, destination)
                    # ignore distances greater than user preferred distance
                    if distance <= user_job_radius:
                        job_rec_distance_filtered.append(job)
                    else:
                        print(distance)

            context['job_rec'] = job_rec_distance_filtered

    return render(request, 'home_user.html', context)


def user_job_details(request, job_id):
    job = JobInfo.objects.get(id=job_id)
    return render(request, 'job_details.html', {'job': job})


def profile_page(request, profile_id):
    profile_user = WorkerInfo.objects.raw("SELECT CONCAT(first_name, ' ', last_name) as name, address, email, education, provider_type, peer_references, cpr_certifications, base_profile_id AS id FROM home_workerprofileinfo WHERE base_profile_id = " + str(profile_id))

    if not profile_user:
        return redirect("../..")

    return render(request, 'profile_page.html', {'profile': profile_user[0]})

def applications(request):
    if not request.user.is_authenticated:
        return redirect("../..")

    user = request.user
    applied_job_ids = JobApplicants.objects.raw("SELECT job_id_id AS id, job_status FROM home_jobapplicants WHERE user_id = " + str(user.id))

    if not applied_job_ids:
        # NO APPLICATIONS, might wanna redirect to applications page instead of home. Doing this for now to avoid error
        return redirect("../..")

    jobs_info = []

    for application in applied_job_ids:
        job_name = JobInfo.objects.raw("SELECT id, job_name FROM home_jobinfo WHERE id = " + str(application.id))
        jobs_info.append({"job_name": job_name[0].job_name, "job_status": application.job_status})

    print(jobs_info)
    
    return render(request, 'applications.html', {'jobs_info': jobs_info})


def user_job_preference(request):
    user = request.user
    currUser = User.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')
    preference_has_set = None
    existing_preference = None
    if(JobPreference.objects.filter(base_profile=currUserID).count()):
        existing_preference = JobPreference.objects.get(
            base_profile=currUserID)
    preference_has_set = (existing_preference != None)
    print(preference_has_set)

    if request.method == 'POST':
        if preference_has_set:
            print('Update form')
            form = JobPreferenceUpdateForm(request.POST)
        else:
            print('New form')
            form = JobPreferenceForm(request.POST)

        if not user.is_hospital:
            if form.is_valid():
                cd = form.cleaned_data
                new_fields = []
                for field in cd:
                    if cd[field]:
                        new_fields.append(field)

                job_type = cd['job_type']
                home_location_zipcode = cd['home_location_zipcode']
                job_location_radius = cd['job_location_radius']
                hospital_type = cd['hospital_type']
                job_on_call = cd['job_on_call']
                job_start_time = cd['job_start_time']
                job_end_time = cd['job_end_time']
                locum_shift_day = cd['locum_shift_day']
                locum_shift_hour = cd['locum_shift_hour']
                job_experience = cd['job_experience']
                job_payment = cd['job_payment']

                if home_location_zipcode:
                    try:
                        geo_res = gmap_to_zip(
                            gmaps.geocode(home_location_zipcode))
                        lat, lng = geo_res['lat'], geo_res['lng']
                    except:
                        lat, lng = 0, 0
                        print('Zipcode invalid')
                else:
                    lat, lng = 0, 0

                if preference_has_set:
                    existing_preference.job_type = job_type
                    existing_preference.home_location_zipcode = home_location_zipcode
                    existing_preference.job_location_radius = job_location_radius
                    existing_preference.home_location_lat = lat
                    existing_preference.home_location_lng = lng
                    existing_preference.hospital_type = hospital_type
                    existing_preference.job_start_time = job_start_time
                    existing_preference.job_end_time = job_end_time
                    existing_preference.locum_shift_day = locum_shift_day
                    existing_preference.job_experience = job_experience
                    existing_preference.job_payment = job_payment

                    print('Update job preference')
                    print(new_fields)
                    existing_preference.save(update_fields=new_fields)
                    print(existing_preference.home_location_zipcode)
                    return render(request, 'job_preference.html', {'form': form, 'preference_has_set': preference_has_set, 'existing_preference': existing_preference})

                else:
                    job_preference = JobPreference(
                        job_type=job_type,
                        home_location_zipcode=home_location_zipcode,
                        home_location_lat=lat,
                        home_location_lng=lng,
                        job_location_radius=job_location_radius,
                        hospital_type=hospital_type,
                        job_on_call=job_on_call,
                        job_start_time=job_start_time,
                        job_end_time=job_end_time,
                        locum_shift_day=locum_shift_day,
                        locum_shift_hour=locum_shift_hour,
                        job_experience=job_experience,
                        job_payment=job_payment,
                        base_profile=user.id,
                    )
                    print('Save job preference')
                    job_preference.save()
                    return render(request, 'job_preference.html', {'form': form, 'preference_has_set': preference_has_set})

    else:
        if preference_has_set:
            form = JobPreferenceUpdateForm()
        else:
            form = JobPreferenceForm()
        print('not post')

    if preference_has_set:
        return render(request, 'job_preference.html', {'form': form, 'preference_has_set': preference_has_set, 'existing_preference': existing_preference})
    else:
        return render(request, 'job_preference.html', {'form': form, 'preference_has_set': preference_has_set})


def home_hospital(request):
    user = get_user_model()
    currUser = user.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')

    allJobs = []
    existingJob = None
    #applicants = {}
    try:
        for existingJob in JobInfo.objects.filter(base_profile_id=currUserID):
            existingJob.applicants = len(JobApplicants.objects.filter(job_id=getattr(existingJob,'id')))
            allJobs.append(existingJob)
    except JobInfo.DoesNotExist:
        print("user is ok, no existing job")
    except MultipleObjectsReturned:
        return redirect('failure/')

    existingJobFlag = (len(allJobs) != 0)
    print(existingJobFlag)
    return render(request, 'home_hospital.html', {'existingJob': allJobs, 'existingJobFlag': existingJobFlag}) #'applicants': applicants})


def hospital_post_job(request):
    if request.method == 'POST':
        form = JobCreationForm(request.POST)
        user = request.user
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

                return redirect("../")
    else:
        form = JobCreationForm()

    return render(request, 'create_job.html', {'form': form})


def hospital_job_details(request, job_id):
    # get job
    job = JobInfo.objects.filter(id=job_id)[0]

    user = get_user_model()
    currUser = user.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')

    allApplicants = []
    allProfiles = []
    applicant = None
    applications = []
    try:
        for applicant in JobApplicants.objects.filter(job_id=job_id):
            print('status')
            print(applicant.job_status)
            print(applicant.user_id)
            print(applicant.job_id)
            if applicant.job_status != 'rejected':
                applications.append(applicant)
                app = User.objects.get(id=getattr(applicant, 'user_id'))
                app.application_id = applicant.id
                allApplicants.append(app)

                user = User.objects.get(id=getattr(applicant, 'user_id'))
                print(user.id)
                # print(applicant.user_id)
                profile = WorkerProfileInfo.objects.filter(base_profile=user)[0]
                app.application_id = applicant.id
                allApplicants.append(app)
                allProfiles.append(profile)
                
        print('Applicant found')
    except JobApplicants.DoesNotExist:
        print("user is ok, no existing applicant")
    except MultipleObjectsReturned:
        return redirect('failure/')

    return render(request, 'hospital_job_details.html', {'existingApplicants': allProfiles, 'job': job}) #'applications': applications})


def find_workers(request, job_id):
    user = get_user_model()
    users = user.objects.all()
    job = JobInfo.objects.get(id=job_id)
    all_workers = JobPreference.objects.all()
    
    context = {}
    #context['job_rec'] = []

    #user_job_type = job.job_type
    #context['type_pref'] = []
    #context['type_pref'] = all_workers.filter(job_type=user_job_type)
    #type_preference = all_workers.filter(job_type=user_job_type)
    #for worker in type_preference:
    #    context['type_pref'].append(users.get(id=worker.base_profile))

    job_begin = job.job_start_time
    job_end = job.job_end_time
    context['date_contains'] = []
    context['rec_list'] = []
    type_date = all_workers
    if job_end : 
        type_date = type_date.exclude(
            # exclude 
            # when end before start
            job_start_time__gte=job_end, 
            #job_end_time__lte=job_begin
            )
    if job_begin:
        type_date = type_date.exclude(
            # exclude 
            # when end before start
            job_start_time__gte=job_begin, 
            #job_end_time__lte=job_begin
            )
    for worker in type_date:
        w = users.get(id=worker.base_profile)
        w.date_range = 1
        w.job_start_time = worker.job_start_time
        w.job_end_time = worker.job_end_time
        context['date_contains'].append(w)
        

    # People Nearby
    lat = -1
    lng = -1
    if job.job_location_zipcode:
        try:
            geo_res = gmap_to_zip(gmaps.geocode(job.job_location_zipcode))
            lat, lng = geo_res['lat'], geo_res['lng']
        except:
            lat, lng = 0, 0
            print('Zipcode invalid')
    #else:
    #    lat, lng = -1, 0

    user_job_radius = 200


    context['dist_rec'] = []
    for worker in all_workers:
        wlat = worker.home_location_lat
        wlng = worker.home_location_lng
        if wlat == -1 or wlng == -1 or lat == -1 or lng == -1:
            continue
        else:
            origin = (lat,lng)
            destination = (wlat, wlng)
            distance = distance_bt_locations(origin, destination)
            #ignore distances greater than user preferred distance
            if distance <= user_job_radius:
                print("found match")
                w = users.get(id=worker.base_profile)
                w.distance = user_job_radius
                context['dist_rec'].append(w)
                #job_rec_distance_filtered.append(worker)
            else:
                print("not close enough")
                print(distance)
    #context['dist_rec'] = []
    #for worker in job_rec_distance_filtered:
    #    context['dist_rec'].append(users.get(id=worker.base_profile))

    #context['rec_list'] = {}
    for worker in context['dist_rec']:
        if worker in context['date_contains']:
            worker.date_range = 1
        else:
            worker.date_range = 0

    for worker in context['date_contains']:
        if(worker not in context['dist_rec']):
            worker.distance = 201
            context['dist_rec'].append(worker)


    #context['dist_rec'] = job_rec_distance_filtered
    #print(full_list)
    return render(request, 'find_workers.html', context)


def profile_update(request):
    curr_user = User.objects.filter(email=request.user.email)

    if request.user.worker:
        return worker_profile_update(request)
        
    if request.method == 'POST':
        form = ProfileUpdateHospitalForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            first_name = cd['first_name']
            last_name = cd['last_name']
            hospital_name = cd['hospital_name']

        curr_user.update(first_name=first_name,
                         last_name=last_name, hospital_name=hospital_name)

    else:
        form = ProfileUpdateHospitalForm()

    return render(request, 'profile_update.html', {'form': form})


def worker_profile_update(request):
    user_id = request.user.id
    print(user_id)
    #print(WorkerProfileInfo.objects.all())
    try:
        worker_info = WorkerProfileInfo.objects.filter(base_profile=request.user)[0]
        print('a')
        print(worker_info)
        profile_set = True
    except:
        print('profile is not set')
        profile_set = False
        worker_info = None
    if request.method == 'POST':
        user = request.user
        form = ProfileUpdateWorkerForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            new_fields = []
            for field in cd:
                if cd[field]:
                    new_fields.append(field)
            if not worker_info:
                first_name = cd['first_name']
                last_name = cd['last_name']
                address = cd['address']
                email = cd['email']
                education = cd['education']
                provider_type = cd['provider_type']
                peer_references = cd['peer_references']
                cpr_certifications = cd['cpr_certifications']
                worker_info = WorkerProfileInfo(
                    last_name=last_name,
                    address=address,
                    email=email,
                    education=education,
                    provider_type=provider_type,
                    peer_references=peer_references,
                    cpr_certifications=cpr_certifications,
                    base_profile=user,
                )
                worker_info.save()
                print('create new profile')
            else:
                worker_info.first_name = cd['first_name']
                worker_info.last_name = cd['last_name']
                worker_info.address = cd['address']
                worker_info.email = cd['email']
                worker_info.education = cd['education']
                worker_info.provider_type = cd['provider_type']
                worker_info.peer_references = cd['peer_references']
                worker_info.cpr_certifications = cd['cpr_certifications']
        
            # previous_info = WorkerInfo.objects.filter(base_profile_id=user_id)
            # previous_info.delete()
                worker_info.save(update_fields=new_fields)
    
    else:
        form = ProfileUpdateWorkerForm()
        print('new form')
    print('Success')
    return render(request, 'worker_profile_update.html', {'form': form, 'profile': worker_info, 'profile_set': profile_set})

'''
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

    return render(request, 'worker_profile_update.html', {'form': form})
'''

def logout_request(request):
    logout(request)
    return redirect('/')

def switch_request(request):
    logout(request)
    return redirect('/login')


def job_query(request):
    qs = JobInfo.objects.all()
    context = {}
    if request.method == 'GET':
        form = JobSearchForm(request.GET)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            zip_contains_query = cd['zip_contains']
            # new queries
            type_contains_query = cd['type_contains']
            hospital_contains_query = cd['hospital_contains']
            hospital_type_contains_query = cd['hospital_type_contains']
            on_call_contains_query = cd['on_call_contains']
            experience_contains_query = cd['experience_contains']
            supervision_contains_query = cd['supervision_contains']
            payment_contains_query = cd['payment_contains']
            vacation_contains_query = cd['vacation_contains']
            education_money_contains_query = cd['education_money_contains']
            shift_day_contains_query = cd['locum_shift_day_contains']
            shift_hour_contains_query = cd['locum_shift_hour_contains']
            zipcode_query = cd['radius_contains']

            # TODO: maybe give more options for how to search by date
            # Example: instead of yes and no maybe an option is range, option with no end date,
            # option where you give an end date and it automatically puts start date as current date
            # maybe it should always filter with the start date as the current date
            # check if searching by range
            if cd['by_date']:
                start_time_contains_query = cd['start_time_contains']
                end_time_contains_query = cd['end_time_contains']

                # Query by dates
                if cd['by_date'] and start_time_contains_query != '' and start_time_contains_query is not None and end_time_contains_query != '' and end_time_contains_query is not None:
                    qs = JobInfo.objects.filter(
                        job_start_time__lte=start_time_contains_query, job_end_time__gte=end_time_contains_query)
            else:
                qs = JobInfo.objects.all()

            # new queries
            if type_contains_query != '' and type_contains_query is not None:
                qs = qs.filter(job_type__icontains=type_contains_query)

            if hospital_contains_query != '' and hospital_contains_query is not None:
                qs = qs.filter(
                    job_location_hospital__icontains=hospital_contains_query)

            if hospital_type_contains_query != '' and hospital_type_contains_query is not None:
                qs = qs.filter(
                    hospital_type__icontains=hospital_type_contains_query)

            if on_call_contains_query != '' and on_call_contains_query is not None:
                qs = qs.filter(job_on_call__icontains=on_call_contains_query)

            if experience_contains_query != '' and experience_contains_query is not None:
                qs = qs.filter(
                    job_experience__icontains=experience_contains_query)

            if supervision_contains_query != '' and supervision_contains_query is not None:
                qs = qs.filter(
                    job_supervision__icontains=supervision_contains_query)

            if payment_contains_query != '' and payment_contains_query is not None:
                qs = qs.filter(job_payment__icontains=payment_contains_query)

            if vacation_contains_query != '' and vacation_contains_query is not None:
                qs = qs.filter(job_vacation__icontains=vacation_contains_query)

            if education_money_contains_query != '' and education_money_contains_query is not None:
                qs = qs.filter(
                    education_money__icontains=education_money_contains_query)

            if shift_hour_contains_query != '' and shift_hour_contains_query is not None:
                qs = qs.filter(
                    locum_shift_hour__icontains=shift_hour_contains_query)

            if shift_day_contains_query != '' and shift_day_contains_query is not None:
                qs = qs.filter(
                    locum_shift_day__icontains=shift_day_contains_query)

             # by location
            if zipcode_query != '' and zipcode_query is not None:
                if zipcode_query == 'No preference':
                    radius = 100000
                else:
                    radius = int(zipcode_query)
            else:
                radius = 20
            
            allJobs = []

            if zip_contains_query != '' and zipcode_query is not None:
                geo_res = gmap_to_zip(gmaps.geocode(zip_contains_query))
                lat, lng = geo_res['lat'], geo_res['lng']
                if lat == -1 and lng == -1:
                    print('bad input')
                else:
                    for job in qs:
                        job_zip = job.job_location_zipcode
                        job_geo_res = gmap_to_zip(gmaps.geocode(job_zip))
                        job_lat, job_lng = job_geo_res['lat'], job_geo_res['lng']

                        origin = (lat, lng)
                        destination = (job_lat, job_lng)
                        distance = distance_bt_locations(origin, destination)
                        # ignore distances greater than user preferred distance
                        if distance <= radius:
                            allJobs.append(job)
                        else:
                            print(distance)
            
            if len(allJobs) > 0:
                qs = allJobs
            context['queryset'] = qs
            context['num_jobs'] = len(qs)

    else:
        form = JobSearchForm()
        print('GET')
        context['queryset'] = None #JobInfo.objects.all()
    
    context['form'] = form

    return render(request, "job_query.html", context)


def hospital_delete_job(request, job_id):
    job = JobInfo.objects.filter(id=job_id)
    job.delete()

    return redirect("../../")

def hospital_reject_applicant(request, job_id, user_id):
    print(job_id)
    print(user_id)
    application = JobApplicants.objects.filter(job_id=job_id)
    application = application.get(user_id=user_id)
    application.job_status = 'rejected'
    print("new status")
    print(application.job_status)
    application.save()
    return redirect("../../")

def hospital_accept_applicant(request, job_id, user_id):
    application = JobApplicants.objects.get(job_id=job_id, user_id=user_id)
    application.job_status = 'accepted'
    application.save()
    ## Email to set up further correspondence
    current_site = get_current_site(request)
    user = get_user_model()
    applicant = user.objects.get(id=application.user_id)
    job = JobInfo.objects.filter(id=job_id)[0]
    employer = job.base_profile

    mail_subject = 'Jop Update!'
    message = render_to_string('applicant_accept.html', {
        'applicant':     applicant,
        'employer': employer,
        'job':      job,
        'domain':   current_site.domain,
        # 'uid':      urlsafe_base64_encode(force_bytes(user.pk)),
        # 'token':    account_activation_token.make_token(user),
    })
    to_email = applicant.email
    email = EmailMessage(
        mail_subject, message, to=[
            to_email], from_email="MedLink <jz.project.testing@gmail.com>"
    )
    email.content_subtype = "html"
    email.send()


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


def gmap_to_zip(gmap_res):
    try:
        geometry = gmap_res[0]['geometry']
    except:
        return {'lat': -1, 'lng': -1}

    return geometry['location']


def distance_bt_locations(origin, destination):
    origins = origin
    destinations = destination
    matrix = gmaps.distance_matrix(origins, destinations)
    rows = matrix['rows'][0]
    elements = rows['elements'][0]
    try:
        distance = elements['distance']['value']
    except:
        distance = 1000000000
    print(distance)
    return distance / 1000


def application(request, job_id):
    print(job_id)
    job = JobInfo.objects.filter(id=job_id)[0]
    user = get_user_model()
    currUser = user.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')
    applicant = request.user
    try: 
        j = JobApplicants.objects.get(user_id=currUserID, job_id=job)
        print(j)
        return render(request, 'application.html')
    except:
        print("does not exist yet")
        JobApplicants.objects.create(user_id=currUserID, job_id=job, job_status='Under Review')

        employer = job.base_profile
        
        # send email
        current_site = get_current_site(request)

        mail_subject = 'New Applicant'
        message = render_to_string('applicant_notice.html', {
            'applicant':     applicant,
            'employer': employer,
            'job':      job,
            'domain':   current_site.domain,
            # 'uid':      urlsafe_base64_encode(force_bytes(user.pk)),
            # 'token':    account_activation_token.make_token(user),
        })
        to_email = employer.email
        email = EmailMessage(
            mail_subject, message, to=[
                to_email], from_email="MedLink <jz.project.testing@gmail.com>"
        )
        email.content_subtype = "html"
        email.send()

        return render(request, 'application.html')


def worker_query(request):
    qs = JobPreference.objects.all()
    context = {}
    if request.method == 'GET':
        form = WorkerSearchForm(request.GET)
        context['form'] = form
        if form.is_valid():
            print('here')
            cd = form.cleaned_data
            zip_contains_query = cd['zip_contains']
            type_contains_query = cd['type_contains']
            hospital_type_contains_query = cd['hospital_type_contains']
            on_call_contains_query = cd['on_call_contains']
            experience_contains_query = cd['experience_contains']
            zipcode_query = cd['radius_contains']

            # TODO: maybe give more options for how to search by date
            # Example: instead of yes and no maybe an option is range, option with no end date,
            # option where you give an end date and it automatically puts start date as current date
            # maybe it should always filter with the start date as the current date
            # check if searching by range
            if cd['by_date']:
                start_time_contains_query = cd['start_time_contains']
                end_time_contains_query = cd['end_time_contains']
                # Query by dates
                if start_time_contains_query  and end_time_contains_query:
                    qs = JobPreference.objects.filter(
                        job_start_time__lte=start_time_contains_query, job_end_time__gte=end_time_contains_query)
            else:
                qs = JobPreference.objects.all()

            # new queries
            if type_contains_query:
                if type_contains_query != 'NA':
                    qs = qs.filter(job_type__icontains=type_contains_query)
            if hospital_type_contains_query:
                if hospital_type_contains_query != 'NA':
                    qs = qs.filter(hospital_type__icontains=hospital_type_contains_query)
            if on_call_contains_query:
                if on_call_contains_query != 'NA':
                    qs = qs.filter(job_on_call__icontains=on_call_contains_query)
            if experience_contains_query:
                if experience_contains_query != 'NA':
                    qs = qs.filter(job_experience__icontains=experience_contains_query)
            # by location
            if zipcode_query:
                if zipcode_query == 'No preference':
                    radius = 100000
                else:
                    radius = int(zipcode_query)
            else:
                radius = 20
            
            allJobs = []
            allUsers = []

            if zip_contains_query:
                geo_res = gmap_to_zip(gmaps.geocode(zip_contains_query))
                lat, lng = geo_res['lat'], geo_res['lng']
                if lat == -1 and lng == -1:
                    print('bad input')
                else:
                    for job in qs:
                        job_zip = job.home_location_zipcode
                        job_geo_res = gmap_to_zip(gmaps.geocode(job_zip))
                        job_lat, job_lng = job_geo_res['lat'], job_geo_res['lng']
                        origin = (lat, lng)
                        destination = (job_lat, job_lng)
                        distance = distance_bt_locations(origin, destination)
                        # ignore distances greater than user preferred distance
                        if distance <= radius:
                            allJobs.append(job.base_profile)
                        else:
                            print(distance)

                    for user_id in allJobs:
                        try:
                            # profile_user = WorkerInfo.objects.filter(base_profile_id=request.user.id)
                            profile_user = WorkerProfileInfo.objects.filter(base_profile_id=user_id)
                            allUsers.append(profile_user[0])
                        except:
                            # print('No profile is found for user ' + user_id)
                            print('No profile is found for user ' + str(user_id))

            context['queryset'] = allUsers
            context['num_workers'] = len(allUsers)
    else:
        form = WorkerSearchForm()
        context['queryset'] = None
    
    context['form'] = form
    return render(request, "worker_query.html", context)