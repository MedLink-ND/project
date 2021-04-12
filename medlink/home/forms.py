from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

CATEGORIES = (
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
    ('d', 'D'),
    ('e', 'E'),
    ('f', 'F'),
)

DURATION = (
    ('full-time', 'Full Time'),
    ('locum-tenes', 'Locum Tenens'),
    ('part-time', 'Part Time'),
)

MONTHS = (
    (1, 'January'),
    (2, 'Febuary'),
    (3, 'March'),
    (4, 'April'),
    (5, 'May'),
    (6, 'June'),
    (7, 'July'),
    (8, 'August'),
    (9, 'September'),
    (10, 'October'),
    (11, 'November'),
    (12, 'December'),
)

YEARS = (
    (2021, '2021'),
    (2022, '2022'),
    (2023, '2023'),
    (2024, '2024'),
    (2025, '2025'),
    (2026, '2026'),
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

class JobCreationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobCreationForm, self).__init__(*args, **kwargs)

    job_name = forms.CharField(
        label="What is the name of the job?", 
    )
    job_level = forms.CharField(
        label='What is its level?', 
    )
    job_category = forms.CharField(
        label='What is the category of this job?',
        widget=forms.Select(choices=CATEGORIES),
    )
    job_duration = forms.CharField(
        label='What is the duration of this job?',
        widget=forms.Select(choices=DURATION),
    )
    job_start_month = forms.CharField(
        label='When does this job start?',
        widget=forms.Select(choices=MONTHS),
    )
    job_start_year = forms.CharField(
        label='When does this job start?',
        widget=forms.Select(choices=YEARS),
    )
    job_end_month = forms.CharField(
        label='When does this job end?',
        widget=forms.Select(choices=MONTHS),
    )
    job_end_year = forms.CharField(
        label='When does this job end?',
        widget=forms.Select(choices=YEARS),
    )
    job_hour_start = forms.CharField(
        label='What time does the job begin in a day?',
        widget=forms.Select(choices=TIME),
    )
    job_hour_end = forms.CharField(
        label='What time does the job end in a day?',
        widget=forms.Select(choices=TIME),
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