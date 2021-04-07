from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.

class HospitalProfile(models.Model):

    class Meta:
        app_label = 'login'

    hospital_name = models.CharField(max_length=255, null=True)
    hospital_position = models.CharField(max_length=255, null=True)
    hospital_location_city = models.CharField(max_length=255, null=True)
    hospital_location_state = models.CharField(max_length=255, null=True)
    hospital_location_zipcode = models.CharField(max_length=255, null=True)
    base_profile = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    looking_for_worker = models.BooleanField(default=True)

    def __str__(self):
        return 'Name: ' + self.base_rofile.first_name + '\t' \
        + 'Hospital: ' + self.hospital_name + '\t' \
        + 'Position: ' + self.hospital_position + '\t' \
        + 'City: ' + self.hospital_location_city + '\t' \
        + 'State: ' + self.hospital_location_state + '\t' \
        + 'Area Code: ' + self.hospital_location_zipcode + '\t' \
        + 'Looking for worker: ' + str(self.looking_for_worker)