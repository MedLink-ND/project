from django.db import models
from django.contrib.auth.models import (
    BaseUserManager, AbstractBaseUser
)
from django import forms
from datetime import datetime

# Create your models here.
class UserManager(BaseUserManager):
  class Meta:
    app_label = 'signup'

  def create_user(self, email, first_name=None, last_name=None, phone=None, field=None, password=None, hospital_name=None, location=None, worker=False, hospital=False):
    """
    Creates and saves a User with the given email and password.
    """
    '''
    if not email:
        raise ValueError('Users must have an email address')
    if not first_name or last_name:
        raise ValueError('Users must have first and last name')
    if not phone:
        raise ValueError('Users must have a valid phone number')
    if not field:
        raise ValueError('Users must have a speciality')
    '''
    user = self.model(
        email=self.normalize_email(email),
        first_name=first_name,
        last_name=first_name,
        phone=phone,
        field=field,
        location=location,
        hospital_name=hospital_name,
        worker=worker,
        hospital=hospital,
    )

    user.set_password(password)
    user.save(using=self._db)
    return user

def create_staffuser(self, email, first_name=None, last_name=None, phone=None, field=None, password=None, hospital_name=None, location=None, worker=False, hospital=False):
    """
    Creates and saves a staff user with the given email and password.
    """
    user = self.create_user(
        email=self.normalize_email(email),
        first_name=first_name,
        last_name=first_name,
        phone=phone,
        field=field,
        location=location,
        hospital_name=hospital_name,
        worker=worker,
        hospital=hospital,
    )
    user.staff = True
    user.save(using=self._db)
    return user

def create_superuser(self, email, first_name=None, last_name=None, phone=None, field=None, password=None, hospital_name=None, location=None, worker=False, hospital=False):
    """
    Creates and saves a superuser with the given email and password.
    """
    user = self.create_user(
        email=self.normalize_email(email),
        first_name=first_name,
        last_name=first_name,
        phone=phone,
        field=field,
        location=location,
        hospital_name=hospital_name,
        worker=worker,
        hospital=hospital,
    )
    user.staff = True
    user.admin = True
    user.save(using=self._db)
    return user

# User Model

class User(AbstractBaseUser):
    class Meta:
        app_label = 'signup'

    email           = models.EmailField(verbose_name='Email address', max_length=255, unique=True)#, validators=[validate_email])
    first_name      = models.CharField(verbose_name='First Name', max_length=255, blank=True, null=True, default='')
    last_name       = models.CharField(verbose_name='Last Name', max_length=255, blank=True, null=True, default='')
    phone           = models.CharField(verbose_name='Phone Number', max_length=255, blank=True, unique=True, default='')
    field           = models.CharField(verbose_name='Field/Specialty', max_length=255, blank=True, null=True, default='')
    hospital_name   = models.CharField(verbose_name='Hospital Name', max_length=255, blank=True, null=True, default='')
    location        = models.CharField(verbose_name='Location', max_length=255, blank=True, null=True, default='')
    active          = models.BooleanField(default=False) # Cannot log in
    staff           = models.BooleanField(default=False) # a admin user; non super-user
    admin           = models.BooleanField(default=False) # a superuser
    worker          = models.BooleanField(default=False) # a medical worker
    hospital        = models.BooleanField(default=False) # a hosptial
    
    USERNAME_FIELD = 'email'

    #REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'field'] 
    # Email & Password are required by default.

    objects = UserManager()

    def get_full_name(self):
        # The user is identified by their email address
        return self.first_name + ' ' + self.last_name

    def get_short_name(self):
        # The user is identified by their email address
        return self.first_name

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        return self.staff

    @property
    def is_admin(self):
        "Is the user a admin member?"
        return self.admin

    @property
    def is_active(self):
        "Is the user active?"
        return self.active

    @property
    def is_hospital(self):
        "Is the user a hospital?"
        return self.hospital

    @property
    def is_worker(self):
        "Is the user a medical worker?"
        return self.worker