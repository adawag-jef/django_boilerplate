# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from django.db.models.signals import post_save
from django.dispatch import receiver
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


# User = get_user_model()
from src.apps.authentication.models import User
# from src.apps.user_management.models import Profile
# from src.apps.user_management.serializers import ProfileSerializer

# import django.dispatch
# profile_create = django.dispatch.Signal(providing_args=["profile", "user"])
import django.dispatch
profile_create = django.dispatch.Signal(providing_args=['instance'])


@receiver(post_save, sender=User)
def announce_action_user(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notif", {"type": "user.notif.create",
                      "event": "New User",
                      "username": instance.username})
    else:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "notif", {"type": "user.notif.update",
                      "event": "Updated User",
                      "username": instance.username})


@receiver(profile_create)
def announce_action_profile(sender, instance, **kwargs):
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(
        "notif", {"type": "profile.notif.create",
                  "event": "Create Profile",
                  "instance": instance.code})

# @receiver(post_save, sender=Profile)
# def announce_action_profile(sender, instance, created, **kwargs):
#     if not created:
#         profile = ProfileSerializer(instance).data

#         channel_layer = get_channel_layer()
#         async_to_sync(channel_layer.group_send)(
#             "notif", {"type": "profile.notif.update",
#                       "event": "Update Profile",
#                       "instance": profile})
# @receiver(post_save, sender=Profile)
# def announce_profile_updated(sender, instance, **kwargs):
#     profile = ProfileSerializer(instance).data

#     channel_layer = get_channel_layer()
#     async_to_sync(channel_layer.group_send)(
#         "notif", {"type": "profile.notif.update",
#                   "event": "Update Profile",
#                   "instance": profile})
