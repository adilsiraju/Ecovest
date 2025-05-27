from django.db import models
from django.conf import settings
from initiatives.models import Category

class OnboardingProgress(models.Model):
    """Track the progress of a user through onboarding steps"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='onboarding_progress')
    welcome_completed = models.BooleanField(default=False)
    interests_completed = models.BooleanField(default=False)
    investment_profile_completed = models.BooleanField(default=False)
    tutorial_completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.user.username}'s Onboarding Progress"
    
    @property
    def is_complete(self):
        """Check if all onboarding steps are complete"""
        return all([
            self.welcome_completed,
            self.interests_completed,
            self.investment_profile_completed,
            self.tutorial_completed
        ])
        
class UserPreference(models.Model):
    """Store user preferences for investment recommendations"""
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='investment_preferences')
    
    # Investment preferences
    RISK_CHOICES = [
        ('low', 'Low Risk'),
        ('moderate', 'Moderate Risk'),
        ('high', 'High Risk'),
    ]
    risk_tolerance = models.CharField(max_length=10, choices=RISK_CHOICES, default='moderate')
    
    # Investment timeframe
    TIMEFRAME_CHOICES = [
        ('short', 'Short-term (< 1 year)'),
        ('medium', 'Medium-term (1-5 years)'),
        ('long', 'Long-term (5+ years)'),
    ]
    investment_timeframe = models.CharField(max_length=10, choices=TIMEFRAME_CHOICES, default='medium')
    
    # Investment amount preferences
    min_investment = models.DecimalField(max_digits=12, decimal_places=2, default=1000.00)
    max_investment = models.DecimalField(max_digits=12, decimal_places=2, default=500000.00)
    
    # Interest categories (many-to-many relationship)
    interested_categories = models.ManyToManyField(Category, related_name='interested_users')
    
    # Impact preferences
    carbon_priority = models.IntegerField(default=5)  # Scale of 1-10
    water_priority = models.IntegerField(default=5)   # Scale of 1-10
    energy_priority = models.IntegerField(default=5)  # Scale of 1-10
    
    def __str__(self):
        return f"{self.user.username}'s Investment Preferences"
