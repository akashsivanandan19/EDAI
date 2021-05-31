import datetime

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager


class CustomUser(AbstractBaseUser, PermissionsMixin):
    PUNE = "P"
    MUMBAI = "M"
    BANGALORE = "B"
    DELHI = "D"
    CITY = (
        (MUMBAI, 'Mumbai'),
        (PUNE, 'Pune'),
        (BANGALORE, 'Bangalore'),
        (DELHI, 'Delhi'),
    )
    email = models.EmailField(_('email address'), unique=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    date_joined = models.DateTimeField(default=timezone.now)
    name = models.CharField(max_length=30, blank=True, null=True, default=None)
    phno = PhoneNumberField(blank=True)
    address = models.CharField(max_length=300, blank=False, null=False, default="Pune")
    # city = models.CharField(max_length=30, blank=False, null=False, default=PUNE)
    city = models.CharField(max_length=10, blank=False, null=True,
                            choices=CITY,
                            default=PUNE,
                            )
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phno']

    objects = CustomUserManager()

    def __str__(self):
        return self.email


# class Employer(models.Model):
#     email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
#     # address = models.CharField(max_length=300, blank=False, null=False)
#
#     def __str__(self):
#         return str(self.email)


class Employee(models.Model):
    ELECTRICIAN = 'A'
    PEST_CONTROL = 'P'
    SANITIZATION = 'S'
    PLUMBING = 'M'

    CATEGORY = (
        (ELECTRICIAN, 'Electrician'),
        (PEST_CONTROL, 'Pest Control'),
        (SANITIZATION, 'Sanitization'),
        (PLUMBING, 'Plumbing'),
    )

    email = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    experience = models.IntegerField(null=False, blank=False)
    category = models.CharField(
        max_length=1,
        choices=CATEGORY,
        default=None,
        blank=False,
        null=True,
    )

    def __str__(self):
        return str(self.email)


class Review(models.Model):
    rating = models.FloatField(null=True, blank=True, default=None)

    def __str__(self):
        return self.rating


class Contact(models.Model):
    email = models.EmailField(_('email address'))
    name = models.CharField(max_length=30, blank=True, null=True)
    message = models.CharField(max_length=200, blank=False, null=True)

    def __str__(self):
        return self.email


class Task(models.Model):
    AC = 'A'
    PEST = 'P'
    SANITIZATION = 'S'
    PLUMBING = 'M'
    ASSIGNED = 'A'
    WAITING = 'W'
    IN_PROGRESS = 'P'
    COMPLETED = 'C'
    TOMORROW = 'T'
    THIS_WEEK = 'W'
    THIS_MONTH = 'M'
    PUNE = 'P'
    MUMBAI = 'M'
    BANGALORE = 'B'
    DELHI = 'D'
    JOB_STATUS = (
        (ASSIGNED, 'Assigned'),
        (WAITING, 'Waiting'),
        (IN_PROGRESS, 'In Progress'),
        (COMPLETED, 'Completed'),
    )
    CITY = (
        (MUMBAI, 'Mumbai'),
        (PUNE, 'Pune'),
        (BANGALORE, 'Bangalore'),
        (DELHI, 'Delhi'),
    )
    PREFERENCE = (
        (TOMORROW, 'Tomorrow'),
        (THIS_WEEK, 'This week'),
        (THIS_MONTH, 'This month'),
    )

    CATEGORIES = (
        (AC, 'AC repair and servicing'),
        (PEST, 'Pest control'),
        (PLUMBING, 'Plumbing work'),
        (SANITIZATION, 'Sanitization'),

    )

    employer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    description = models.CharField(max_length=300, blank=False, null=True)
    city = models.CharField(max_length=10, blank=False, null=True,
                            choices=CITY,
                            default=PUNE, )
    address = models.CharField(max_length=300, blank=False, null=False, default="address")
    # name = models.CharField(max_length=100, blank=False, null=True)
    employee = models.EmailField(_("Employee assigned"), unique=False)
    category = models.CharField(
        max_length=1,
        choices=CATEGORIES,
        default=None,
        blank=False,
        null=True,
    )
    status = models.CharField(
        max_length=1,
        choices=JOB_STATUS,
        default=WAITING,
    )
    preference = models.CharField(
        max_length=1,
        choices=PREFERENCE,
        default=TOMORROW,
    )
    issue_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return self.description


class ServiceRequest(models.Model):
    request_placed_employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE)
    task = models.OneToOneField(Task,
                                on_delete=models.CASCADE)
    request_date = models.DateField(default=datetime.date.today)

    def __str__(self):
        return str(self.task.description)
