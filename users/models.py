from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

def user_profile_image_path(instance, filename):
    # Upload to: media/users/<username>/profile_images/<filename>
    return f'users/{instance.username}/profile_images/{filename}'

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255, default='')
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)],  # Age range: 18-100
        default=18
    )
    email = models.EmailField(unique=True)  # Ensure email is unique
    phone = models.CharField(max_length=15, blank=True, null=True)  # Optional phone number
    profile_image = models.ImageField(
        upload_to=user_profile_image_path,
        blank=True,
        null=True,
        verbose_name='Profile Image'
    )
    
    def __str__(self):
        return self.username