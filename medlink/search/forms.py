from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class LoginForm(forms.Form):
    username = forms.EmailField(label='Email')
    password = forms.CharField(widget=forms.PasswordInput)


RECRUITING_STATUS = [
    ('Not looking for medical workers at this moment', 'Not looking for medical workers at this moment'),
    ('Currently seeking medical workers', 'Currently seeking medical workers'),
]

class HospitalProfileForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(HospitalProfileForm, self).__init__(*args, **kwargs)


    hospital_name = forms.CharField(
        label="What is the name of your hospital?", 
    )
    hospital_location_city = forms.CharField(
        label='Which city is it located in?', 
    )
    hospital_location_state = forms.CharField(
        label='Which state is it located in?', 
    )
    hospital_location_zipcode = forms.CharField(
        label='What is your area code?', 
    )
    hospital_position = forms.CharField(
        label='What is your position?', 
    )
    hospital_recruiting_status = forms.CharField(
        label='Are you currently looking for medical workers?', 
        widget=forms.Select(choices=RECRUITING_STATUS)
    )