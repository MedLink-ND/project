from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm, HospitalProfileForm
from .models import HospitalProfile

# Create your views here.
def login(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = LoginForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            print(username, password)
            
            user = authenticate(request, username=username, password=password)
            if user is not None:
                auth_login(request, user)
                if user.is_hospital == 1:
                    return redirect("../home/hospital")

            else:
                print("login error")
                return render(request, 'login.html', {
                    'error_message': ' Login Failed! Try again, or create an account.',
                    'login_form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'login_form': form})

def hospital_profile_creation(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = HospitalProfileForm(request.POST)
        user = request.user

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL
            cd = form.cleaned_data
            hospital_name = cd['hospital_name']
            hospital_position = cd['hospital_position']
            hospital_location_city = cd['hospital_location_city']
            hospital_location_state = cd['hospital_location_state']
            hospital_location_zipcode = cd['hospital_location_zipcode']
            looking_for_worker = cd['looking_for_worker']

            hospital_info = HospitalProfile(
                hospital_name=hospital_name,
                hospital_position=hospital_position,
                hospital_location_city=hospital_location_city,
                hospital_location_state=hospital_location_state,
                hospital_location_zipcode=hospital_location_zipcode,
                looking_for_worker=looking_for_worker,
                base_profile=user,
            )

            hospital_info.save()
            user.profile_created = True
            
            return redirect('../../home/')

    # if a GET (or any other method) we'll create a blank form
    else:
        form = HospitalProfileForm()

    return render(request, 'hospital_profile_creation.html',  {'form': form})
