from django.contrib import admin
from .models import Initiative, ProgressUpdate

@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('title', 'initiative', 'date_posted')
    list_filter = ('initiative', 'date_posted')
    search_fields = ('title', 'description')

@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'funding_goal', 'amount_raised')
    list_filter = ('status', 'category')
    search_fields = ('title', 'description')
    fieldsets = (
        ('General Information', {
            'fields': ('title', 'description', 'category', 'funding_goal', 'amount_raised', 'image'),
        }),
        ('Environmental Impact Metrics', {
            'fields': ('carbon_saved', 'energy_saved_generated', 'water_saved'),
        }),
    )

    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark selected initiatives as Active"

    def mark_as_funded(self, request, queryset):
        queryset.update(status='funded')
    mark_as_funded.short_description = "Mark selected initiatives as Funded"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected initiatives as Completed"