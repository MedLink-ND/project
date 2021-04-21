from django import forms
from django.contrib.auth import get_user_model
import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

User = get_user_model()

DURATION = (
    (None, ''),
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Locum', 'Short Term Locum'),
    ('NA', 'NA')

)
HOSPITAL = (
    (None, ''),
    ('Outpatient', 'Outpatient'),
    ('Inpatient', 'Inpatient'),
    ('Both outpatient / inpatient', 'Both outpatient/inpatient'),
    ('NA', 'NA')
)
ONCALL = (
    (None, ''),
    ('On call', 'On Call'),
    ('No call', 'No Call'),
    ('NA', 'NA')
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
    (None, ''),
    ('Greater than 2 years', 'Greater than 2 years'),
    ('New Grad / Fewer than 2 years', 'New Grad (fewer than 2 years)'),
    ('NA', 'NA')
)
SUPERVISION = (
    (None, ''),
    ('No supervision', 'No supervision'),
    ('Supervised by anesthesiologist', 'Supervised by anesthesiologist'),
)
PAYMENT = (
    (None, ''),
    ('W2', 'W2'),
    ('1099 / No Benefits', '1099/No Benefits'),
    ('NA', 'NA')
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
    job_location_zipcode = forms.IntegerField(
        label='Where is the job? (Enter zipcode of hospital)', 
    )
    job_location_hospital = forms.CharField(
        label='Which hospital is this job associated with?', 
    )
    hospital_type = forms.CharField(
        label="What is the type of the hospital?",
        widget=forms.Select(choices=HOSPITAL),
    )
    job_on_call = forms.CharField(
        label="Does this job require on call?",
        widget=forms.Select(choices=ONCALL),
    )
    job_start_time = forms.DateTimeField(
        label='What is the start date of this job?', 
        widget=DatePicker(
            options={
                'minDate': '2021-01-01',
                'maxDate': '2030-01-01',
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
    )
    job_end_time = forms.DateTimeField(
        label='What is the end date of this job?', 
        widget=DatePicker(
            options={
                'minDate': '2021-01-01',
                'maxDate': '2030-01-01',
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
    )
    locum_shift_day = forms.CharField(
        label='For locum: How many days in a week?'
    )
    locum_shift_hour = forms.CharField(
        label='For locum: How many hours in a day?'
    )
    job_experience = forms.CharField(
        label='What is the experience level required for this job?',
        widget=forms.Select(choices=EXPERIENCE),
    )
    job_supervision = forms.CharField(
        label='Does this job require supervision from an anesthesiologist',
        widget=forms.Select(choices=SUPERVISION),
    )
    job_payment = forms.CharField(
        label='What is the payment type for this job?',
        widget=forms.Select(choices=PAYMENT),
    )
    job_vacation = forms.CharField(
        label='What are the vacation benefits of this job?', 
    )
    education_money = forms.CharField(
        label='Are there any education credits with this job?', 
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

    ##### BASIC SEARCH QUERIES ########
    location_contains = forms.CharField(
        label="Where do you want to search for a job?",
        required = False
    )

    level_contains = forms.CharField(
        label='What job level?', 
        required = False
    )

    description_contains = forms.CharField(
        label='Search in job description?', 
        required = False
    )

class JobUpdateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobUpdateForm, self).__init__(*args, **kwargs)

    job_name = forms.CharField(
        label="What is the name of the job?", 
        required=False
    )
    job_type = forms.CharField(
        label='What is the type of this job?',
        widget=forms.Select(choices=DURATION),
        required=False
    )
    job_location_zipcode = forms.IntegerField(
        label='Where is the job? (Enter zipcode of hospital)', 
        required=False
    )
    job_location_hospital = forms.CharField(
        label='Which hospital is this job associated with?', 
        required=False
    )
    hospital_type = forms.CharField(
        label="What is the type of the hospital?",
        widget=forms.Select(choices=HOSPITAL),
        required=False
    )
    job_on_call = forms.CharField(
        label="Does this job require on call?",
        widget=forms.Select(choices=ONCALL),
        required=False
    )
    job_start_time = forms.DateTimeField(
        label='What is the start date of this job?', 
        widget=DatePicker(
            options={
                'minDate': '2021-01-01',
                'maxDate': '2030-01-01',
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
        required=False
    )
    job_end_time = forms.DateTimeField(
        label='What is the end date of this job?', 
        widget=DatePicker(
            options={
                'minDate': '2021-01-01',
                'maxDate': '2030-01-01',
            },
            attrs={
                'append': 'fa fa-calendar',
                'icon_toggle': True,
            },
        ),
        required=False
    )
    locum_shift_day = forms.CharField(
        label='For locum: How many days in a week?',
        required=False
    )
    locum_shift_hour = forms.CharField(
        label='For locum: How many hours in a day?',
        required=False
    )
    job_experience = forms.CharField(
        label='What is the experience level required for this job?',
        widget=forms.Select(choices=EXPERIENCE),
        required=False
    )
    job_supervision = forms.CharField(
        label='Does this job require supervision from an anesthesiologist',
        widget=forms.Select(choices=SUPERVISION),
        required=False
    )
    job_payment = forms.CharField(
        label='What is the payment type for this job?',
        widget=forms.Select(choices=PAYMENT),
        required=False
    )
    job_vacation = forms.CharField(
        label='What are the vacation benefits of this job?', 
        required=False
    )
    education_money = forms.CharField(
        label='Are there any education credits with this job?', 
        required=False
    )