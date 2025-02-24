from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator


# Create your models here.

def user_profile_image_path(instance, filename):
    # Upload to: media/users/<username>/profile_images/<filename>
    return f'users/{instance.username}/profile_images/{filename}'

class Badge(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.ImageField(upload_to='badges/', blank=True, null=True)
    criteria = models.JSONField(default=dict)  # Example: {"total_invested": 1000}

    def __str__(self):
        return self.name

class CustomUser(AbstractUser):
    full_name = models.CharField(max_length=255)
    age = models.PositiveIntegerField(
        validators=[MinValueValidator(18), MaxValueValidator(100)]
    )
    email = models.EmailField(unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    profile_image = models.ImageField(upload_to='profile_images/', blank=True, null=True)
    badges = models.ManyToManyField(Badge, blank=True, related_name='users')
    total_investments = models.PositiveIntegerField(default=0)
    total_amount_invested = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    def update_stats(self):
        self.total_investments = self.investment_set.count()
        self.total_amount_invested = sum(inv.amount for inv in self.investment_set.all())
        self.save()

    def __str__(self):
        return self.username