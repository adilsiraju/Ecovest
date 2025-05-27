from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from .models import OnboardingProgress, UserPreference
from .forms import UserPreferenceForm, InterestSelectionForm

@login_required
def onboarding_welcome(request):
    """First step in onboarding - welcome screen"""
    # Get or create onboarding progress
    progress, created = OnboardingProgress.objects.get_or_create(user=request.user)
    
    # If user has completed onboarding, redirect to dashboard
    if progress.is_complete:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Mark welcome step as completed
        progress.welcome_completed = True
        progress.save()
        return redirect('onboarding_interests')
    
    # Prepare context to send to template
    context = {
        'user': request.user,
        'progress': progress
    }
    
    return render(request, 'onboarding/welcome.html', context)

@login_required
def onboarding_interests(request):
    """Second step in onboarding - select interests"""
    # Get onboarding progress
    progress, created = OnboardingProgress.objects.get_or_create(user=request.user)
    
    # Redirect if user hasn't completed previous step or has completed all steps
    if not progress.welcome_completed:
        return redirect('onboarding_welcome')
    if progress.is_complete:
        return redirect('dashboard')
    
    # Get or create user preference
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = InterestSelectionForm(request.POST)
        if form.is_valid():
            # Save selected categories
            selected_categories = form.cleaned_data['interests']
            preference.interested_categories.set(selected_categories)
            
            # Mark interests step as completed
            progress.interests_completed = True
            progress.save()
            
            return redirect('onboarding_investment_profile')
    else:
        form = InterestSelectionForm()
    
    context = {
        'user': request.user,
        'form': form,
        'progress': progress
    }
    
    return render(request, 'onboarding/interests.html', context)

@login_required
def onboarding_investment_profile(request):
    """Third step in onboarding - investment profile"""
    # Get onboarding progress
    progress, created = OnboardingProgress.objects.get_or_create(user=request.user)
    
    # Redirect if user hasn't completed previous steps or has completed all steps
    if not progress.interests_completed:
        return redirect('onboarding_interests')
    if progress.is_complete:
        return redirect('dashboard')
    
    # Get or create user preference
    preference, created = UserPreference.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = UserPreferenceForm(request.POST, instance=preference)
        if form.is_valid():
            form.save()
            
            # Mark investment profile step as completed
            progress.investment_profile_completed = True
            progress.save()
            
            return redirect('onboarding_tutorial')
    else:
        form = UserPreferenceForm(instance=preference)
    
    context = {
        'user': request.user,
        'form': form,
        'progress': progress
    }
    
    return render(request, 'onboarding/investment_profile.html', context)

@login_required
def onboarding_tutorial(request):
    """Fourth step in onboarding - platform tutorial"""
    # Get onboarding progress
    progress, created = OnboardingProgress.objects.get_or_create(user=request.user)
    
    # Redirect if user hasn't completed previous steps
    if not progress.investment_profile_completed:
        return redirect('onboarding_investment_profile')
    if progress.is_complete:
        return redirect('dashboard')
    
    if request.method == 'POST':
        # Mark tutorial step as completed and set completion timestamp
        progress.tutorial_completed = True
        progress.completed_at = timezone.now()
        progress.save()
        
        return redirect('dashboard')
    
    context = {
        'user': request.user,
        'progress': progress
    }
    
    return render(request, 'onboarding/tutorial.html', context)
