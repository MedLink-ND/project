from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class JobInfo(models.Model):

    class Meta:
        app_label = 'home'

    job_name = models.CharField(max_length=255, null=True)
    job_type = models.CharField(max_length=255, null=True)
    job_start_time = models.DateTimeField(null=True)
    job_end_time = models.DateTimeField(null=True)
    job_hour_start = models.CharField(max_length=255, null=True)
    job_hour_end = models.CharField(max_length=255, null=True)    
    job_description = models.CharField(max_length=255, null=True)
    job_location_hospital = models.CharField(max_length=255, null=True)
    job_location_city = models.CharField(max_length=255, null=True)
    base_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    # def __str__(self):
    #     return 'Name: ' + self.base_rofile.first_name + '\t' \
    #     + 'Hospital: ' + self.hospital_name + '\t' \
    #     + 'Position: ' + self.hospital_position + '\t' \
    #     + 'City: ' + self.hospital_location_city + '\t' \
    #     + 'State: ' + self.hospital_location_state + '\t' \
    #     + 'Area Code: ' + self.hospital_location_zipcode + '\t' \