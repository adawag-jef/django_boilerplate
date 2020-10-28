from django.db import models
from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver

from src.utils.Utils import Utility
from src.utils.enums import Prefix
from src.utils.common_model import CreatedAndUpdatedModel, CodeModel

from src.apps.company_management.models import Company
from notifier.signals import profile_create

User = get_user_model()


class Profile(CreatedAndUpdatedModel, CodeModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    location = models.CharField(max_length=30, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    company = models.ForeignKey(
        Company, null=True, blank=True, to_field='code', on_delete=models.CASCADE)

    def save(self, *args, **kwargs):
        super(Profile, self).save(*args, **kwargs)
        Utility.generate_code(Profile, Prefix.PROFILE.value, self.id)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile.objects.create(user=instance)
        instance = Profile.objects.get(id=profile.id)
        profile_create.send(sender=Profile, instance=instance)


# @receiver(post_save, sender=User)
# def save_user_profile(sender, instance, **kwargs):
#     instance.profile.save()
