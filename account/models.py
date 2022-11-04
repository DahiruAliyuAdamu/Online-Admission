from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _

class Account(AbstractUser):
    name = models.CharField(_('Fullname'), max_length=50)
    email = models.EmailField(_('Email Address'), unique=True)
    phone_number = models.CharField(_('Phone Number'), max_length=11, unique=True)
    username = models.CharField(_('Username'), max_length=10, unique=True)
    password = models.CharField(_('Password'), max_length=16)