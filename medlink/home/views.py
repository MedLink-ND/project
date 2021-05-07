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
from .models import JobInfo, JobPreference, WorkerInfo

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
    applicants = {}
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
    applicant = None
    try:
        for applicant in JobApplicants.objects.filter(job_id=job_id):
            app = User.objects.get(id=getattr(applicant, 'user_id'))
            allApplicants.append(app)
        print('Applicant found')
    except JobApplicants.DoesNotExist:
        print("user is ok, no existing applicant")
    except MultipleObjectsReturned:
        return redirect('failure/')

    return render(request, 'hospital_job_details.html', {'existingApplicants': allApplicants, 'job': job})


def find_workers(request, job_id):
    user = get_user_model()

    #preference_has_set = None
    #existing_preference = None
    job = JobInfo.objects.get(id=job_id)
    all_workers = JobPreference.objects.all()
    
    context = {}
    context['job_rec'] = None

    user_job_type = job.job_type
    worker_rec = all_workers.filter(job_type=user_job_type)
    
    if job.job_location_zipcode:
        try:
            geo_res = gmap_to_zip(gmaps.geocode(job.job_location_zipcode))
            lat, lng = geo_res['lat'], geo_res['lng']
        except:
            lat, lng = 0, 0
            print('Zipcode invalid')
    else:
        lat, lng = 0, 0

    # if user_preference.job_location_radius == 'No preference':
    #        user_job_radius = 10000000
    #    else:
    #user_job_radius = int(50)  # Default?
    #user_location_lat = user_preference.home_location_lat
    #user_location_lng = user_preference.home_location_lng
    #rec_distance_filtered = []
    #if len(worker_rec) > 0:
    #    for worker in worker_rec:
    #        job_zip = worker.job_location_zipcode
    #        geo_res = gmap_to_zip(gmaps.geocode(job_zip))
    #        lat, lng = geo_res['lat'], geo_res['lng']
    #        if lat == -1 and lng == -1:
    #           continue
    #        else:
    #            origin = (user_location_lat, user_location_lng)
    #            destination = (lat, lng)
    #            distance = distance_bt_locations(origin, destination)
                # ignore distances greater than user preferred distance
                #if distance <= user_job_radius:
                #    job_rec_distance_filtered.append(job)
                #else:
                #        print(distance)

            #context['job_rec'] = job_rec_distance_filtered

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
            if zipcode_query:
                if zipcode_query == 'No preference':
                    radius = 100000
                else:
                    radius = int(zipcode_query)
            else:
                radius = 20
            
            allJobs = []

            if zip_contains_query:
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
            
            qs = allJobs
            context['queryset'] = qs
            context['num_jobs'] = len(qs)

    else:
        form = JobSearchForm()
        print('GET')
        context['queryset'] = None
    
    context['form'] = form

    return render(request, "job_query.html", context)


def hospital_delete_job(request, job_id):
    job = JobInfo.objects.filter(id=job_id)
    job.delete()

    return redirect("../../")

def hospital_reject_applicant(request, job_id, worker_id):
    application = JobApplicants.objects.filter(job_id=job_id, user_id=worker_id)
    application.status = 'rejected'
    return redirect("../../")

def hospital_accept_applicant(request, job_id, worker_id):
    application = JobApplicants.objects.filter(job_id=job_id, user_id=worker_id)
    application.status = 'accepted'

    ## Email to set up further correspondence
    current_site = get_current_site(request)
    user = get_user_model()
    applicant = user.objects.filter(id=application.user_id)
    job = JobInfo.objects.filter(id=job_id)[0]
    employer = job.base_user

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

    job = JobInfo.objects.filter(id=job_id)[0]
    user = get_user_model()
    currUser = user.objects.filter(email=request.user.email)
    currUserID = getattr(currUser[0], 'id')
    applicant = request.user

    JobApplicants.objects.create(user_id=currUserID, job_id=job, job_status='')

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
                    qs = JobPreference.objects.filter(
                        job_start_time__lte=start_time_contains_query, job_end_time__gte=end_time_contains_query)
            else:
                qs = JobPreference.objects.all()

            print(qs)
            # by location
            # TODO: maybe combine location and zip
            if zip_contains_query != '' and zip_contains_query is not None:
                qs = qs.filter(
                    job_location_zipcode__icontains=zip_contains_query)

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

            context['queryset'] = qs
            context['num_jobs'] = len(qs)
            print('POST')

    else:
        form = WorkerSearchForm()
        print('GET')
        context['queryset'] = None
    
    context['form'] = form

    return render(request, "worker_query.html", context)