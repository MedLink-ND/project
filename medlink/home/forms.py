from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class JobCreationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)


    job_name = forms.CharField(
        label="What is the name of the job?", 
    )
    job_level = forms.CharField(
        label='What is its level?', 
    )
    job_description = forms.CharField(
        label='Describe in a few sentences what this job is and what you are looking for?', 
    )
    job_location_hospital = forms.CharField(
        label='Which hospital is this job associated with?', 
    )
    job_location_city = forms.CharField(
        label='Where is the hospital?', 
    )