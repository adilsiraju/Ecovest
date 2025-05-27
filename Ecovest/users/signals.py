from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import CustomUser, Profile

# Only create profile if not handled elsewhere
@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)

# Remove the save_user_profile signal to avoid interference with our form
# @receiver(post_save, sender=CustomUser)
# def save_user_profile(sender, instance, **kwargs):
#     try:
#         instance.profile.save()
#     except Profile.DoesNotExist:
#         Profile.objects.create(user=instance)