from django.contrib import admin
from .models import Category, Initiative, ProgressUpdate

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name',)

@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'funding_goal', 'amount_raised', 'roi')
    list_filter = ('category', 'status')
    search_fields = ('title', 'description')
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'category', 'funding_goal', 'amount_raised', 'status', 'roi')
        }),
        ('Metrics', {
            'fields': ('carbon_saved', 'energy_saved_generated', 'water_saved')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )

    actions = ['mark_as_active', 'mark_as_funded', 'mark_as_completed']
    
    def mark_as_active(self, request, queryset):
        queryset.update(status='active')
    mark_as_active.short_description = "Mark selected initiatives as Active"

    def mark_as_funded(self, request, queryset):
        queryset.update(status='funded')
    mark_as_funded.short_description = "Mark selected initiatives as Funded"

    def mark_as_completed(self, request, queryset):
        queryset.update(status='completed')
    mark_as_completed.short_description = "Mark selected initiatives as Completed"


@admin.register(ProgressUpdate)
class ProgressUpdateAdmin(admin.ModelAdmin):
    list_display = ('initiative', 'title', 'date_posted')
    list_filter = ('initiative', 'date_posted')
    search_fields = ('title', 'description')