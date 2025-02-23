from django.contrib import admin
from .models import Initiative, ProgressUpdate

@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'initiative', 'date_posted')
    list_filter = ('initiative', 'date_posted')
    search_fields = ('title', 'description')

@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'funding_goal', 'amount_raised')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'category', 'funding_goal', 'amount_raised'),
        }),
        ('Environmental Impact Metrics', {
            'fields': ('carbon_saved', 'energy_saved_generated', 'water_saved'),
        }),
    )