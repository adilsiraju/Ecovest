from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, Profile

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Choose a username',
                'class': 'form-control',
                'autocomplete': 'username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'you@example.com',
                'class': 'form-control',
                'autocomplete': 'email'
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Your first name',
                'class': 'form-control',
                'autocomplete': 'given-name'
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Your last name',
                'class': 'form-control',
                'autocomplete': 'family-name'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Override the default widgets for password fields
        self.fields['password1'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Create a password',
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget = forms.PasswordInput(attrs={
            'placeholder': 'Confirm password',
            'class': 'form-control',
            'autocomplete': 'new-password'
        })
        
        # Custom help text
        self.fields['email'].help_text = "We'll never share your email with anyone else."
        # Remove default Django help text that will be replaced with our custom UI feedback
        self.fields['password1'].help_text = ""

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name')
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'Enter your username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Enter your email'}),
            'first_name': forms.TextInput(attrs={'placeholder': 'Enter your first name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Enter your last name'}),
        }

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = (
            'profile_image', 'phone_number', 'address_line1', 'address_line2', 
            'city', 'state', 'postal_code', 'country', 'bio'
        )
        widgets = {
            'phone_number': forms.TextInput(attrs={'placeholder': 'e.g., +919876543210'}),
            'address_line1': forms.TextInput(attrs={'placeholder': 'Street address'}),
            'address_line2': forms.TextInput(attrs={'placeholder': 'Apartment, suite, etc. (optional)'}),
            'city': forms.TextInput(attrs={'placeholder': 'City'}),
            'state': forms.TextInput(attrs={'placeholder': 'State/Province'}),
            'postal_code': forms.TextInput(attrs={'placeholder': 'Postal/ZIP Code'}),
            'country': forms.TextInput(attrs={'placeholder': 'Country'}),
            'bio': forms.Textarea(attrs={'placeholder': 'Tell us about yourself (max 500 characters)', 'rows': 4}),
        }

class EnhancedRegistrationForm(forms.ModelForm):
    """A form that combines user registration with profile details"""
    
    # User fields
    username = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Choose a username',
        'class': 'form-control',
        'autocomplete': 'username'
    }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={
        'placeholder': 'you@example.com',
        'class': 'form-control',
        'autocomplete': 'email'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your first name',
        'class': 'form-control',
        'autocomplete': 'given-name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'placeholder': 'Your last name',
        'class': 'form-control',
        'autocomplete': 'family-name'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Create a password',
        'class': 'form-control',
        'autocomplete': 'new-password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm password',
        'class': 'form-control',
        'autocomplete': 'new-password'
    }))
    
    # Profile fields
    profile_image = forms.ImageField(required=False, widget=forms.FileInput(attrs={
        'class': 'form-control',
        'accept': 'image/*'
    }))
    phone_number = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'e.g., +919876543210',
        'class': 'form-control',
        'autocomplete': 'tel'
    }))
    address_line1 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Street address',
        'class': 'form-control',
        'autocomplete': 'address-line1'
    }))
    address_line2 = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Apartment, suite, etc. (optional)',
        'class': 'form-control',
        'autocomplete': 'address-line2'
    }))
    city = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'City',
        'class': 'form-control',
        'autocomplete': 'address-level2'
    }))
    state = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'State/Province',
        'class': 'form-control',
        'autocomplete': 'address-level1'
    }))
    postal_code = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Postal/ZIP Code',
        'class': 'form-control',
        'autocomplete': 'postal-code'
    }))
    country = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'placeholder': 'Country',
        'class': 'form-control',
        'autocomplete': 'country-name'
    }))
    
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return cleaned_data

    def save(self, commit=True):
        # Save the CustomUser instance
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
            # Create or update the Profile instance
            profile, created = Profile.objects.get_or_create(user=user)
            profile.phone_number = self.cleaned_data.get('phone_number', '')
            profile.address_line1 = self.cleaned_data.get('address_line1', '')
            profile.address_line2 = self.cleaned_data.get('address_line2', '')
            profile.city = self.cleaned_data.get('city', '')
            profile.state = self.cleaned_data.get('state', '')
            profile.postal_code = self.cleaned_data.get('postal_code', '')
            profile.country = self.cleaned_data.get('country', '')
            if 'profile_image' in self.files:
                profile.profile_image = self.files['profile_image']
            profile.save()
        return user