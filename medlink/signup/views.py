from django.contrib.auth import authenticate, login as auth_login, get_user_model
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect, render
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import is_safe_url, urlsafe_base64_encode, urlsafe_base64_decode
from .forms import SignUpForm
from .tok import account_activation_token

User = get_user_model()

# Create your views here.
def worker_signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = form.save()
            user.save()
            
            current_site = get_current_site(request)

            mail_subject = 'Welcome to MedLink!'
            message = render_to_string('email-confirmation.html', {
                'user':     user,
                'domain':   current_site.domain,
                'uid':      urlsafe_base64_encode(force_bytes(user.pk)),
                'token':    account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email], from_email="MedLink <jz.project.testing@gmail.com>"
            )
            email.content_subtype = "html"
            email.send()

            return redirect('confirmation/')

    # if a GET (or any other method) we'll create a blank form
    else:
      form = SignUpForm()
    
    return render(request, "signup.html", {"signup_form": form})

def hospital_signup(request):
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = SignUpForm(request.POST)

        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            user = form.save()
            user.save()
            
            current_site = get_current_site(request)

            mail_subject = 'Welcome to MedLink!'
            message = render_to_string('email-confirmation.html', {
                'user':     user,
                'domain':   current_site.domain,
                'uid':      urlsafe_base64_encode(force_bytes(user.pk)),
                'token':    account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                mail_subject, message, to=[to_email], from_email="MedLink <jz.project.testing@gmail.com>"
            )
            email.content_subtype = "html"
            email.send()

            return redirect('confirmation/')

    # if a GET (or any other method) we'll create a blank form
    else:
      form = SignUpForm()
    
    return render(request, "signup.html", {"signup_form": form})


def activate(request, uidb64, token):
  request.session['login'] = False

  try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      user = User.objects.get(pk=uid)

  except(TypeError, ValueError, OverflowError, User.DoesNotExist):
      user = None

  if user is not None and account_activation_token.check_token(user, token):
      user.active = True
      user.save()
      auth_login(request, user)
      return redirect('signup-success/')
  else:
      return HttpResponse('Activation link is invalid!')

def confirmation(request):
    request.session['login'] = False

    return render(request, "confirmation.html")

def signup_success(request):
    request.session['login'] = False

    return render(request, "signup-success.html")