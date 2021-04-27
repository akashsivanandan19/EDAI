from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30, blank=True, null=True, default=None)
    phno = PhoneNumberField(blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name','phno']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


class Employer(models.Model):
    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    address = models.CharField(max_length=300, blank=False, null=False)


class Employee(models.Model):
    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    experience = models.IntegerField(null=False, blank=False)


class Contact(models.Model):
    email = models.EmailField(_('email address'))
    name = models.CharField(max_length=30, blank=True, null=True)
    message = models.CharField(max_length=200, blank=False, null=True)

    def __str__(self):
        return self.email
