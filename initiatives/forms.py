from django import forms
from .models import ProgressUpdate

class ProgressUpdateForm(forms.ModelForm):
    class Meta:
        model = ProgressUpdate
        fields = ('title', 'description')