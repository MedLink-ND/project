from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class JobInfo(models.Model):

    class Meta:
        app_label = 'home'

    job_name = models.CharField(max_length=255, null=True)
    job_type = models.CharField(max_length=255, null=True)
    job_location_zipcode = models.IntegerField(max_length=5, null=True)
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


class WorkerInfo(models.Model):

    class Meta:
        app_label = 'home'

    name = models.CharField(max_length=255, null=True)
    address = models.CharField(max_length=255, null=True)
    email = models.IntegerField(max_length=5, null=True)
    education = models.CharField(max_length=255, null=True)
    certifications = models.CharField(max_length=255, null=True)
    provider_type = models.CharField(max_length=255, null=True)
    peer_references = models.CharField(max_length=255, null=True)
    cpr_certifications = models.CharField(max_length=255, null=True)
    base_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return 'Name: ' + self.base_rofile.first_name + '\t' \
    #     + 'Hospital: ' + self.hospital_name + '\t' \
    #     + 'Position: ' + self.hospital_position + '\t' \
    #     + 'City: ' + self.hospital_location_city + '\t' \
    #     + 'State: ' + self.hospital_location_state + '\t' \
    #     + 'Area Code: ' + self.hospital_location_zipcode + '\t' \