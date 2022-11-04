import email
from email.headerregistry import Address
from enum import auto
from operator import mod
from statistics import mode
from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
GENDER_LIST = [
    ('male', 'Male'),
	('female', 'Female'),
]

SECTION_LIST = [
    ('nur', 'Nursery'),
    ('pri', 'Primary'),
    ('jss', 'Junior'),
    ('sss', 'Senior'),
]

class Applicant(models.Model):
    first_name = models.CharField(_('First Name'), max_length=20)
    second_name = models.CharField(_('Second Name'), max_length=20)
    last_name = models.CharField(_('Last Name'), max_length=20)
    gender = models.CharField(_('Gender'), max_length=10, choices=GENDER_LIST, default=1)
    date_of_birth = models.DateField(_('Date of Birth'), blank=True, null=True)
    age = models.IntegerField(_('Age'), blank=True)
    phone_number = models.CharField(_('Phone Number'), max_length=11)
    email_address = models.EmailField(_('Email Address'))
    per_address = models.TextField(_('Present Address'))
    section = models.CharField(_('Section'), max_length=10, choices=SECTION_LIST, default=1)
    class_room = models.CharField(_('Class'), max_length=20)
    sessions = models.CharField(_('Session'), max_length=20, default='2022/2023')

    def __str__(self) -> str:
        return f'{self.first_name} {self.second_name} {self.last_name} > {self.class_room}'
    
    def get_fullname(self) -> str:
        return f'{self.first_name} {self.second_name} {self.last_name}'

    def validate_email(self) -> str:
        return self.email_address

    def delete(self, *args, **kwargs):
        self.image.delete()
        super().delete(*args, **kwargs)

class Sponsor(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    name = models.CharField(_('Sponsor/Guardian Name'), max_length=50)
    phone_number = models.CharField(_('Phone Number'), max_length=11)
    email_address = models.EmailField(_('Email Address'))
    per_address = models.TextField(_('Address'))

    def __str__(self) -> str:
        return f'{self.name} Parent/Guardian of {self.applicant}'

class NextOfKin(models.Model):
    applicant = models.ForeignKey(Applicant, on_delete=models.CASCADE)
    name = models.CharField(_('Next of Kin Name'), max_length=50)
    phone_number = models.CharField(_('Phone Number'), max_length=11)
    email_address = models.EmailField(_('Email Address'))
    per_address = models.TextField(_('Address'))

    def __str__(self) -> str:
        return f'{self.name} Next of Kin of {self.applicant}'

class classSection(models.Model):
    section = models.CharField(_('Section'), max_length=20)
    classes = models.CharField(_('Class'), max_length=30, unique=True)

    def __str__(self) -> str:
        return f'{self.classes}'

class Session(models.Model):
    session = models.CharField(_('New Session'), max_length=9, unique=True)
    status = models.CharField(_('Status'), max_length=10, default='active')
    current_session = models.CharField(_('Current Session'), max_length=10, default=0)
    date_added = models.DateField(_("Date Added"), auto_now=True)

    class Meta:
        ordering = ['date_added']

    def __str__(self) -> str:
        return f'{self.session}'

class Admission(models.Model):
    applicant = models.ForeignKey(Applicant, related_name='admissions', on_delete=models.CASCADE)
    admitted = models.BooleanField(_('Admitted'), default=False)
    session = models.ForeignKey(Session, related_name="sessions", on_delete=models.CASCADE)

    class Meta:
        ordering = ['session']