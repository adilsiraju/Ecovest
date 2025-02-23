from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.core.validators import MinValueValidator, MaxValueValidator
from . models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    full_name = forms.CharField(max_length=255, required=True)
    age = forms.IntegerField(
        required=True,
        validators=[MinValueValidator(18), MaxValueValidator(100)],
        initial=18
    )
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=False)
    profile_image = forms.ImageField(required=False)

    class Meta:
        model = CustomUser
        fields = ('username', 'full_name', 'age', 'email', 'phone', 'profile_image', 'password1', 'password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        if phone and CustomUser.objects.filter(phone=phone).exists():
            raise forms.ValidationError("This phone number is already in use.")
        return phone
    
class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('full_name', 'age', 'email', 'phone', 'profile_image')