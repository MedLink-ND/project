from django import forms
from django.contrib.auth import get_user_model
import datetime
from tempus_dominus.widgets import DatePicker, TimePicker, DateTimePicker

User = get_user_model()

### For hospital recruiters

DURATION = (
<<<<<<< HEAD
    ('', 'NA'),
    ('full-time', 'Full Time'),
    ('part-time', 'Part Time'),
    ('locum', 'Short Term Locum'),
)
HOSPITAL = (
    ('', 'NA'),
    ('outpatient', 'Outpatient'),
    ('inpatient', 'Inpatient'),
    ('outpatient+inpatient', 'Both outpatient/inpatient'),
)
ONCALL = (
    ('', 'NA'),
    ('oncall', 'On Call'),
    ('nocall', 'No Call'),
    
)
TIME = (
    ('', 'NA'),
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
=======
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
>>>>>>> 213eaa81e94e4e390881e18b929e66f53d125bc2
)
# TIME = (
#     (1, '1 AM'),
#     (2, '2 AM'),
#     (3, '3 AM'),
#     (4, '4 AM'),
#     (5, '5 AM'),
#     (6, '6 AM'),
#     (7, '7 AM'),
#     (8, '8 AM'),
#     (9, '9 AM'),
#     (10, '10 AM'),
#     (11, '11 AM'),
#     (12, '12 PM'),
#     (13, '1 PM'),
#     (14, '2 PM'),
#     (15, '3 PM'),
#     (16, '4 PM'),
#     (17, '5 PM'),
#     (18, '6 PM'),
#     (19, '7 PM'),
#     (20, '8 PM'),
#     (21, '9 PM'),
#     (22, '10 PM'),
#     (23, '11 PM'),
#     (24, '12 AM'),
# )
EXPERIENCE = (
<<<<<<< HEAD
    ('', 'NA'),
    ('gt2', 'Greater than 2 years'),
    ('new grad', 'New Grad (fewer than 2 years)'),
)
SUPERVISION = (
    ('', 'NA'),
    ('no', 'No supervision'),
    ('yes', 'Supervised by anesthesiologist'),
)
PAYMENT = (
    ('', 'NA'),
    ('w2', 'W2'),
    ('1099', '1099/No Benefits'),
)

YES_NO = (
    ('True', 'Yes'),
    ('', 'No'),
)


=======
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

>>>>>>> 213eaa81e94e4e390881e18b929e66f53d125bc2
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
        label='What is the end date of this job? (If there is no end date, leave this empty)', 
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
        required=False,
    )
    locum_shift_day = forms.CharField(
        label='For locum: How many days in a week?',
        required=False,
    )
    locum_shift_hour = forms.CharField(
        label='For locum: How many hours in a day?',
        required=False,
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

<<<<<<< HEAD
=======
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



### For medical workers

DURATION_U = (
    (None, ''),
    ('Full Time', 'Full Time'),
    ('Part Time', 'Part Time'),
    ('Locum', 'Short Term Locum'),
    ('No preference', 'I am open to all positions')
)
RADIUS = (
    (None, ''),
    ('10', '< 10 miles'),
    ('20', '< 20 miles'),
    ('50', '< 50 miles'),
    ('No preference', "I don't have a preference for job location")
)
HOSPITAL_U = (
    (None, ''),
    ('Outpatient', 'Outpatient'),
    ('Inpatient', 'Inpatient'),
    ('Both outpatient / inpatient', 'Both outpatient/inpatient'),
    ('All', 'I am open to all types of hospitals')
)
ONCALL_U = (
    (None, ''),
    ('On call', 'On Call'),
    ('No call', 'No Call'),
    ('All', 'I am open to either type.')
)
EXPERIENCE_U = (
    (None, ''),
    ('Greater than 2 years', 'Greater than 2 years'),
    ('New Grad / Fewer than 2 years', 'New Grad (fewer than 2 years)'),
)
PAYMENT = (
    (None, ''),
    ('W2', 'W2'),
    ('1099 / No Benefits', '1099/No Benefits'),
    ('All', 'I am open to either type.')
)
>>>>>>> 213eaa81e94e4e390881e18b929e66f53d125bc2

class JobSearchForm(forms.Form):

    def __init__(self, * args, **kwargs):
        super(JobSearchForm, self).__init__(*args, **kwargs)

    ##### BASIC SEARCH QUERIES ########
    ### TODO: maybe add zip and city together in query
    zip_contains = forms.CharField(
        label="What zipcode do you want to search for a job?",
        required = False
    )

    type_contains = forms.CharField(
        label='What type of job?',
        widget=forms.Select(choices=DURATION),
        required = False
    )

    if(type_contains=='full-time'):
        locum_shift_day = forms.CharField(
            label='For locum: How many days in a week?'
        )

    hospital_contains = forms.CharField(
        label='Hospital name?', 
        required = False
    )
    hospital_type_contains = forms.CharField(
        label="Type of hospital?",
        widget=forms.Select(choices=HOSPITAL),
        required = False
    )
    on_call_contains = forms.CharField(
        label="On call?",
        widget=forms.RadioSelect(choices=ONCALL),
        required = False
    )

    experience_contains = forms.CharField(
        label='Experience level?',
        widget=forms.Select(choices=EXPERIENCE),
        required = False
    )
    supervision_contains = forms.CharField(
        label='Does this job require supervision from an anesthesiologist',
        widget=forms.Select(choices=SUPERVISION),
        required = False
    )
    payment_contains = forms.CharField(
        label='What is the payment type for this job?',
        widget=forms.Select(choices=PAYMENT),
        required = False
    )
    vacation_contains = forms.CharField(
        label='What are the vacation benefits of this job?', 
        required = False
    )
    education_money_contains = forms.CharField(
        label='Are there any education credits with this job?', 
        required = False
    )

    ### Query by dates
    by_date = forms.CharField(
        label='Search within date range?',
        widget=forms.RadioSelect(choices=YES_NO),
        required = False
    )

    start_time_contains = forms.DateTimeField(
        label='Start date:', 
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
        required = False
    )

    end_time_contains = forms.DateTimeField(
        label='End Date:', 
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
        required = False
    )

    ### TODO: figure out weither it makes sense for them to be numbers
    ### TODO: also figure out weither it makes sense for >= type comparisons
    locum_shift_day_contains = forms.CharField(
        label='For locum: How many days in a week?',
        required = False
    )
    locum_shift_hour_contains = forms.CharField(
        label='For locum: How many hours in a day?',
        required = False
    )

class JobPreferenceForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobPreferenceForm, self).__init__(*args, **kwargs)

    job_type = forms.CharField(
        label='What type of jobs are you looking for?',
        widget=forms.Select(choices=DURATION_U),
    )
    home_location_zipcode = forms.IntegerField(
        label='Where do you live? (Enter zipcode)', 
    )
    job_location_radius = forms.CharField(
        label='How far from your home would you like to search for job?',
        widget=forms.Select(choices=RADIUS),
    )
    hospital_type = forms.CharField(
        label="What is the type of the hospital that you want to work at?",
        widget=forms.Select(choices=HOSPITAL_U),
    )
    job_on_call = forms.CharField(
        label="Do you mind if your job requires on call?",
        widget=forms.Select(choices=ONCALL_U),
    )
    job_start_time = forms.DateTimeField(
        label='When do you want to start working?', 
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
        label='Do you have an end date in mind for your job?', 
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
        required=False,
    )
    locum_shift_day = forms.CharField(
        label='For locum jobs: How many days do you want to work in a week?',
        required=False,
    )
    locum_shift_hour = forms.CharField(
        label='For locum jobs: How many hours do you want to work in a day?',
        required=False,
    )
    job_experience = forms.CharField(
        label='What is your experience level?',
        widget=forms.Select(choices=EXPERIENCE_U),
    )
    job_payment = forms.CharField(
        label='What is your prefered payment type for the job?',
        widget=forms.Select(choices=PAYMENT),
    )


class JobPreferenceUpdateForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super(JobPreferenceUpdateForm, self).__init__(*args, **kwargs)

    job_type = forms.CharField(
        label='What type of jobs are you looking for?',
        widget=forms.Select(choices=DURATION_U),
        required=False,
    )
    home_location_zipcode = forms.IntegerField(
        label='Where do you live? (Enter zipcode)', 
        required=False,
    )
    job_location_radius = forms.CharField(
        label='How far from your home would you like to search for job?',
        widget=forms.Select(choices=RADIUS),
        required=False,
    )
    hospital_type = forms.CharField(
        label="What is the type of the hospital that you want to work at?",
        widget=forms.Select(choices=HOSPITAL_U),
        required=False,
    )
    job_on_call = forms.CharField(
        label="Do you mind if your job requires on call?",
        widget=forms.Select(choices=ONCALL_U),
        required=False
    )
    job_start_time = forms.DateTimeField(
        label='When do you want to start working?', 
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
        label='Do you have an end date in mind for your job?', 
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
        required=False,
    )
<<<<<<< HEAD


=======
    locum_shift_day = forms.CharField(
        label='For locum jobs: How many days do you want to work in a week?',
        required=False,
    )
    locum_shift_hour = forms.CharField(
        label='For locum jobs: How many hours do you want to work in a day?',
        required=False,
    )
    job_experience = forms.CharField(
        label='What is your experience level?',
        widget=forms.Select(choices=EXPERIENCE_U),
        required=False,
    )
    job_payment = forms.CharField(
        label='What is your prefered payment type for the job?',
        widget=forms.Select(choices=PAYMENT),
        required=False,
    )
>>>>>>> 213eaa81e94e4e390881e18b929e66f53d125bc2
