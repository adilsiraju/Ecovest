from django.contrib import admin
from django.core.exceptions import ValidationError
from django import forms
from .models import Category, Initiative, get_landlocked_states


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


class InitiativeAdminForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = '__all__'

    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')
        location = cleaned_data.get('location')

        if hasattr(self, 'cleaned_data') and 'categories' in self.data and location:
            landlocked_states = get_landlocked_states()
            ocean_category = Category.objects.filter(name='Ocean Conservation').first()

            if location in landlocked_states and ocean_category and str(ocean_category.id) in self.data.getlist('categories'):
                self.add_error(
                    'categories',
                    f"Ocean Conservation projects cannot be created in landlocked states like {location}. "
                    "Please select a coastal state or a different category."
                )

        return cleaned_data


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    form = InitiativeAdminForm
    list_display = (
        'title',
        'status',
        'location',
        'goal_amount',
        'current_amount',
        'project_scale',
        'risk_level',
        'duration_months'
    )
    list_filter = (
        'status',
        'location',
        'project_scale',
        'risk_level',
        'categories'
    )
    search_fields = ('title', 'description', 'location')
    filter_horizontal = ('categories',)
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'description', 'image', 'categories', 'location', 'technology_type'),
            'description': '<div style="padding: 10px; margin-bottom: 10px; border-left: 4px solid #007bff; background-color: #f8f9fa;">'
                           '<strong>Note:</strong> Ocean Conservation projects can only be created in coastal states. '
                           'Landlocked states like Rajasthan, Madhya Pradesh, and others will be rejected.</div>'
        }),
        ('Financial Details', {
            'fields': ('goal_amount', 'current_amount', 'min_investment', 'max_investment', 'roi_estimate')
        }),
        ('Project Details', {
            'fields': ('project_scale', 'risk_level', 'duration_months')
        }),
        ('Status Information', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )

    def save_model(self, request, obj, form, change):
        landlocked_states = get_landlocked_states()
        location = obj.location
        ocean_category = Category.objects.filter(name='Ocean Conservation').first()

        if change:
            if location in landlocked_states and ocean_category in obj.categories.all():
                raise ValidationError(
                    f"Ocean Conservation projects cannot be created in landlocked states like {location}. "
                    "Please select a coastal state or a different category."
                )

        super().save_model(request, obj, form, change)

        if not change:
            obj.refresh_from_db()
            if location in landlocked_states and ocean_category in obj.categories.all():
                obj.delete()
                raise ValidationError(
                    f"Ocean Conservation projects cannot be created in landlocked states like {location}. "
                    "Please select a coastal state or a different category."
                )
