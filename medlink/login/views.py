from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LoginForm

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
                return redirect("/")  

            else:
                print("login error")
                return render(request, 'login.html', {
                    'error_message': ' Login Failed! Try again, or create an account.',
                    'login_form': form})

    # if a GET (or any other method) we'll create a blank form
    else:
        form = LoginForm()

    return render(request, 'login.html', {'login_form': form})
