from django import forms
from .models import UserPreference
from initiatives.models import Category

class UserPreferenceForm(forms.ModelForm):
    """Form for collecting user investment preferences during onboarding"""
    class Meta:
        model = UserPreference
        fields = ['risk_tolerance', 'investment_timeframe', 'min_investment', 
                  'max_investment', 'carbon_priority', 'water_priority', 'energy_priority']
        widgets = {
            'min_investment': forms.NumberInput(attrs={'min': '100', 'step': '100', 'class': 'form-control'}),
            'max_investment': forms.NumberInput(attrs={'min': '1000', 'step': '1000', 'class': 'form-control'}),
            'carbon_priority': forms.NumberInput(attrs={'min': '1', 'max': '10', 'class': 'form-range', 'type': 'range'}),
            'water_priority': forms.NumberInput(attrs={'min': '1', 'max': '10', 'class': 'form-range', 'type': 'range'}),
            'energy_priority': forms.NumberInput(attrs={'min': '1', 'max': '10', 'class': 'form-range', 'type': 'range'}),
        }
        labels = {
            'min_investment': 'Minimum Investment Amount (₹)',
            'max_investment': 'Maximum Investment Amount (₹)',
            'carbon_priority': 'Carbon Reduction Priority',
            'water_priority': 'Water Conservation Priority',
            'energy_priority': 'Energy Efficiency Priority',
        }
        help_texts = {
            'risk_tolerance': 'Choose your comfort level with investment risk',
            'investment_timeframe': 'How long do you plan to keep your investments?',
            'carbon_priority': 'How important is carbon reduction to you? (1-10)',
            'water_priority': 'How important is water conservation to you? (1-10)',
            'energy_priority': 'How important is energy efficiency to you? (1-10)',
        }

class InterestSelectionForm(forms.Form):
    """Form for selecting categories of interest during onboarding"""
    interests = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'interest-checkbox'}),
        required=False,
        label="Select investment categories that interest you"
    )