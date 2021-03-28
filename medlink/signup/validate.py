from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User

def validate_email_exist(email):
    try:
        get_user_model().objects.get(email=email)
    #print("Email is correct")
    except:
        raise ValidationError("Please enter a valid email address!")
