from django import forms
from django.contrib.auth import get_user_model
import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

User = get_user_model()

DURATION = (
    ('full-time', 'Full Time'),
    ('part-time', 'Part Time'),
    ('locum', 'Short Term Locum'),
)
HOSPITAL = (
    ('outpatient', 'Outpatient'),
    ('inpatient', 'Inpatient'),
    ('outpatient+inpatient', 'Both outpatient/inpatient')
)
ONCALL = (
    ('oncall', 'On Call'),
    ('nocall', 'No Call'),
)
TIME = (
    (1, '1 AM'),
    (2, '2 AM'),
    (3, '3 AM'),
    (4, '4 AM'),
    (5, '5 AM'),
    (6, '6 AM'),
    (7, '7 AM'),
    (8, '8 AM'),
    (9, '9 AM'),
    (10, '10 AM'),
    (11, '11 AM'),
    (12, '12 PM'),
    (13, '1 PM'),
    (14, '2 PM'),
    (15, '3 PM'),
    (16, '4 PM'),
    (17, '5 PM'),
    (18, '6 PM'),
    (19, '7 PM'),
    (20, '8 PM'),
    (21, '9 PM'),
    (22, '10 PM'),
    (23, '11 PM'),
    (24, '12 AM'),
)
EXPERIENCE = (
    ('gt2', 'Greater than 2 years'),
    ('new grad', 'New Grad (fewer than 2 years)')
)
class JobCreationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)

    job_name = forms.CharField(
        label="What is the name of the job?", 
    )
    job_type = forms.CharField(
        label='What is the type of this job?',
        widget=forms.Select(choices=DURATION),
    )
    job_location = forms.CharField(
        label='Where is the job? (Enter zipcode of hospital)', 
    )
    hospital_type = forms.CharField(
        label="What is the type of the hospital?",
        widget=forms.Select(choices=HOSPITAL),
    )
    job_on_call = forms.CharField(
        label="Does this job require on call?",
        widget=forms.RadioSelect(choices=ONCALL),
    )
    job_start_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%b %d, %Y, %H:%M %p"],
        label='What is the start date of this job?', 
        widget=DateTimePicker(
            options={
                'format': 'MMM DD, YYYY',
                'useCurrent': True,
                'stepping': 10,
                'ignoreReadonly': True,
                'sideBySide': True,
           },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
    )
    job_end_time = forms.DateTimeField(
        input_formats=["%Y-%m-%dT%H:%M", "%Y-%m-%d %H:%M", "%b %d, %Y, %H:%M %p"],
        label='What is the end date of this job?', 
        widget=DateTimePicker(
            options={
                'format': 'MMM DD, YYYY',
                'useCurrent': True,
                'stepping': 10,
                'ignoreReadonly': True,
                'sideBySide': True,
           },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
    )
    job_hour_start = forms.CharField(
        label='What time does the job begin in a day?',
        widget=forms.Select(choices=TIME),
    )
    job_hour_end = forms.CharField(
        label='What time does the job end in a day?',
        widget=forms.Select(choices=TIME),
    )
    job_experience = forms.CharField(
        label='What is the experience level required for this job?',
        widget=forms.Select(choices=EXPERIENCE),
    )
    job_description = forms.CharField(
        label='Describe in a few sentences what this job is and what you are looking for?', 
    )
    job_location_hospital = forms.CharField(
        label='Which hospital is this job associated with?', 
    )


class ProfileUpdateHospitalForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(ProfileUpdateHospitalForm, self).__init__(*args, **kwargs)

    first_name = forms.CharField(
        label="First Name", 
    )
    last_name = forms.CharField(
        label='Last Name', 
    )
    hospital_name = forms.CharField(
        label='Hospital Name',
    )

class JobSearchForm(forms.Form):

    def __init__(self, * args, **kwargs):
        super(JobSearchForm, self).__init__(*args, **kwargs)

    location_contains = forms.CharField(
        label="Where would you like to search for a job?",
        required = False
    )

class JobUpdateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)

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