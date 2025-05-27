from django.contrib import admin
from .models import OnboardingProgress, UserPreference

@admin.register(OnboardingProgress)
class OnboardingProgressAdmin(admin.ModelAdmin):
    list_display = ('user', 'welcome_completed', 'interests_completed', 'investment_profile_completed', 'tutorial_completed', 'is_complete', 'completed_at')
    list_filter = ('welcome_completed', 'interests_completed', 'investment_profile_completed', 'tutorial_completed')
    search_fields = ('user__username', 'user__email')

@admin.register(UserPreference)
class UserPreferenceAdmin(admin.ModelAdmin):
    list_display = ('user', 'risk_tolerance', 'investment_timeframe', 'min_investment', 'max_investment')
    list_filter = ('risk_tolerance', 'investment_timeframe')
    search_fields = ('user__username', 'user__email')
    filter_horizontal = ('interested_categories',)
