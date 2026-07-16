from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Account, Profile



@receiver(post_save,sender=Account)
def create_profile(sender,instance,created,**kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user
        )