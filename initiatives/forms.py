from django import forms
from .models import Initiative, Category, get_landlocked_states

class InitiativeForm(forms.ModelForm):
    class Meta:
        model = Initiative
        fields = [
            'title', 'description', 'image', 'categories', 'location',
            'goal_amount', 'min_investment', 'max_investment',
            'project_scale', 'duration_months'
        ]
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4}),
            'categories': forms.CheckboxSelectMultiple(),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add Bootstrap classes to form fields
        for field in self.fields.values():
            if isinstance(field.widget, forms.TextInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Textarea):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.Select):
                field.widget.attrs.update({'class': 'form-select'})
            elif isinstance(field.widget, forms.NumberInput):
                field.widget.attrs.update({'class': 'form-control'})
            elif isinstance(field.widget, forms.CheckboxSelectMultiple):
                field.widget.attrs.update({'class': 'form-check'})
                
    def clean(self):
        cleaned_data = super().clean()
        categories = cleaned_data.get('categories')
        location = cleaned_data.get('location')
        
        # Check if Ocean Conservation is selected for a landlocked state
        if categories and location:
            landlocked_states = get_landlocked_states()
            ocean_category = Category.objects.filter(name='Ocean Conservation').first()
            
            if ocean_category in categories and location in landlocked_states:
                self.add_error(
                    'categories', 
                    'Ocean Conservation projects cannot be created in landlocked states like {}. '
                    'Please select a coastal state or a different category.'.format(location)
                )
                
        return cleaned_data