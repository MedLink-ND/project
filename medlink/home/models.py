from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class JobPreference(models.Model):
    """
    For job preference -- Medical worker
    """
    class Meta:
        app_label = 'home'
    
    job_type = models.CharField(max_length=255, null=True)
    home_location_zipcode = models.IntegerField(null=True)
    home_location_lat = models.FloatField(null=True)
    home_location_lng = models.FloatField(null=True)
    job_location_radius = models.CharField(max_length=255, null=True)
    hospital_type = models.CharField(max_length=255, null=True)
    job_on_call = models.CharField(max_length=255, null=True)
    job_start_time = models.DateTimeField(null=True)
    job_end_time = models.DateTimeField(null=True)
    locum_shift_day = models.CharField(max_length=255, null=True)
    locum_shift_hour = models.CharField(max_length=255, null=True)
    job_experience = models.CharField(max_length=255, null=True)
    job_supervision = models.CharField(max_length=255, null=True)
    job_payment = models.CharField(max_length=255, null=True)
    base_profile = models.IntegerField(primary_key=True, null=False)
    # base_profile = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return 'Job type: ' + self.job_type + '; job_location_radius: ' + self.job_location_radius

class JobInfo(models.Model):
    """
    For job posting -- Hospital recruiter
    """
    class Meta:
        app_label = 'home'

    job_name = models.CharField(max_length=255, null=True)
    job_type = models.CharField(max_length=255, null=True)
    job_location_zipcode = models.IntegerField(null=True)
    job_location_hospital = models.CharField(max_length=255, null=True)
    hospital_type = models.CharField(max_length=255, null=True)
    job_on_call = models.CharField(max_length=255, null=True)
    job_start_time = models.DateTimeField(null=True)
    job_end_time = models.DateTimeField(null=True)
    locum_shift_day = models.CharField(max_length=255, null=True)
    locum_shift_hour = models.CharField(max_length=255, null=True)
    job_experience = models.CharField(max_length=255, null=True)
    job_supervision = models.CharField(max_length=255, null=True)
    job_payment = models.CharField(max_length=255, null=True)
    job_vacation = models.CharField(max_length=255, null=True)
    education_money = models.CharField(max_length=255, null=True)
    base_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

<<<<<<< HEAD
    # def __str__(self):
    #     return 'Name: ' + self.base_rofile.first_name + '\t' \
    #     + 'Hospital: ' + self.hospital_name + '\t' \
    #     + 'Position: ' + self.hospital_position + '\t' \
    #     + 'City: ' + self.hospital_location_city + '\t' \
    #     + 'State: ' + self.hospital_location_state + '\t' \
    #     + 'Area Code: ' + self.hospital_location_zipcode + '\t' \

class JobApplicants(models.Model):
    
    class Meta:
        app_label: 'home'

    job_id = models.ForeignKey(JobInfo, on_delete=models.SET_NULL, null=True)
    user_id = models.CharField(max_length=255, null=True)
    #application_date = models.DateTimeField(null=True)

    
=======
    def __str__(self):
        return self.job_type
>>>>>>> 213eaa81e94e4e390881e18b929e66f53d125bc2
