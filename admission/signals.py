from django.db.models.signals import pre_save
from django.dispatch import receiver
from .models import Applicant
from .utils import calculate_age

@receiver(pre_save, sender=Applicant)
def pre_save_applicant_reciever(sender, instance, *args, **kwargs):
	
	instance.age = calculate_age(instance, instance.date_of_birth)
		
pre_save.connect(pre_save_applicant_reciever, sender=Applicant)