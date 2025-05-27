from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, UserProfileForm, UserUpdateForm, EnhancedRegistrationForm
from django.db import models  # Explicitly import models from django.db
from django.db.models import Sum, Count, Q, F, Case, When, Value
from django.db.models.functions import Cast
from investments.models import Investment
from initiatives.models import Initiative, Category
from .models import Profile
from django.db.models.functions import TruncMonth
import json
from django.core.serializers.json import DjangoJSONEncoder
from investments.portfolio_analyzer import PortfolioAnalyzer
from django.db.models.functions import Coalesce
from django.db.models import DecimalField, FloatField
from collections import defaultdict
from onboarding.models import OnboardingProgress, UserPreference

def register(request):
    if request.method == 'POST':
        print("\n==== REGISTRATION POST DATA ====")
        print(f"POST: {request.POST}")
        print(f"FILES: {request.FILES}")
        
        form = EnhancedRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            print("\n==== FORM VALID ====")
            print(f"CLEANED DATA: {form.cleaned_data}")
            
            user = form.save()  # Saves both user and profile
            print(f"USER CREATED: {user.username}, ID: {user.id}")
            print(f"PROFILE DATA: Phone: {user.profile.phone_number}, Address: {user.profile.address_line1}")
            
            login(request, user)
            OnboardingProgress.objects.get_or_create(user=user)
            return redirect('onboarding_welcome')
        else:
            print("Form validation errors:", form.errors)
    else:
        form = EnhancedRegistrationForm()
        
    return render(request, 'users/register.html', {
        'form': form,
        'form_errors': form.errors.items() if request.method == 'POST' else None
    })

@login_required
def dashboard(request):
    # Check if user has completed onboarding
    onboarding_progress, created = OnboardingProgress.objects.get_or_create(user=request.user)
    
    # If onboarding is not complete, redirect to the appropriate onboarding step
    if not onboarding_progress.is_complete:
        if not onboarding_progress.welcome_completed:
            return redirect('onboarding_welcome')
        elif not onboarding_progress.interests_completed:
            return redirect('onboarding_interests')
        elif not onboarding_progress.investment_profile_completed:
            return redirect('onboarding_investment_profile')
        elif not onboarding_progress.tutorial_completed:
            return redirect('onboarding_tutorial')
    
    user = request.user
    investments = user.investments.all().select_related('initiative')
    
    # Get user preferences for personalized recommendations
    try:
        user_preferences = UserPreference.objects.get(user=user)
        
        # Query initiatives that match user preferences
        recommended_initiatives_query = Initiative.objects.filter(
            status='active'  # Use status='active' instead of is_active=True
        ).exclude(
            id__in=[inv.initiative.id for inv in investments]  # Exclude already invested
        ).prefetch_related('categories')
        
        # Filter by user's interested categories if they selected any
        if user_preferences.interested_categories.exists():
            recommended_initiatives_query = recommended_initiatives_query.filter(
                categories__in=user_preferences.interested_categories.all()
            ).distinct()
        
        # Filter by investment amount preferences
        recommended_initiatives_query = recommended_initiatives_query.filter(
            min_investment__lte=user_preferences.max_investment,
            goal_amount__gte=user_preferences.min_investment
        )
        
        # Order by matches to preference priorities
        recommended_initiatives = list(recommended_initiatives_query[:6])
        
        # Calculate match scores based on impact priorities
        for initiative in recommended_initiatives:
            # Base score starts at 50%
            match_score = 50
            
            # Add points for category match
            if initiative.categories.filter(id__in=user_preferences.interested_categories.values_list('id', flat=True)).exists():
                match_score += 15
            
            # Add points for risk match (risk_level 1-3 maps to low, moderate, high)
            risk_map = {'low': 1, 'moderate': 2, 'high': 3}
            if initiative.risk_level == risk_map.get(user_preferences.risk_tolerance, 2):
                match_score += 10
            
            # Add points for impact priorities alignment
            carbon_weight = user_preferences.carbon_priority / 10  # 0.1 to 1.0
            energy_weight = user_preferences.energy_priority / 10
            water_weight = user_preferences.water_priority / 10
            
            # Higher points if high impact in areas user cares about
            if initiative.carbon_impact > 1000 and carbon_weight > 0.5:
                match_score += 5 * carbon_weight
            if initiative.energy_impact > 1000 and energy_weight > 0.5:
                match_score += 5 * energy_weight
            if initiative.water_impact > 1000 and water_weight > 0.5:
                match_score += 5 * water_weight
            
            # Cap at 100%
            initiative.match_score = min(match_score, 100)
            
            # Calculate impact for ₹1000 for each initiative
            from investments.models import Investment
            impact = Investment.calculate_impact_for_amount(initiative, 1000)
            if impact:
                initiative.impact_for_1000 = {k: round(float(v), 2) for k, v in impact.items()}
            else:
                initiative.impact_for_1000 = {}
        
        # Sort by match score
        recommended_initiatives.sort(key=lambda x: getattr(x, 'match_score', 0), reverse=True)
        
    except UserPreference.DoesNotExist:
        user_preferences = None
        recommended_initiatives = []
    
    # Calculate total invested amount
    total_invested = investments.aggregate(
        total=Coalesce(Sum('amount'), 0, output_field=DecimalField())
    )['total']
    
    # Calculate total impact metrics using stored fields with explicit FloatField
    total_impact = investments.aggregate(
        carbon=Coalesce(Sum('carbon_impact'), 0, output_field=models.FloatField()),
        energy=Coalesce(Sum('energy_impact'), 0, output_field=models.FloatField()),
        water=Coalesce(Sum('water_impact'), 0, output_field=models.FloatField())
    )
    total_impact = {k: round(v) for k, v in total_impact.items()}
    
    # Initialize category impact dictionary
    impact_by_category = defaultdict(lambda: {'carbon': 0, 'energy': 0, 'water': 0})
    
    # Group investments by initiative
    grouped_investments = {}
    for investment in investments:
        initiative_id = investment.initiative.id
        if (initiative_id) not in grouped_investments:
            grouped_investments[initiative_id] = {
                'initiative': investment.initiative,
                'total_amount': 0,
                'last_investment_date': investment.created_at,
                'impact_metrics': {'carbon': 0, 'energy': 0, 'water': 0}
            }
        grouped_investments[initiative_id]['total_amount'] += investment.amount
        grouped_investments[initiative_id]['impact_metrics']['carbon'] += investment.carbon_impact
        grouped_investments[initiative_id]['impact_metrics']['energy'] += investment.energy_impact
        grouped_investments[initiative_id]['impact_metrics']['water'] += investment.water_impact
        
        # Add to category impact
        for category_name in [cat.name for cat in investment.initiative.categories.all()]:
            impact_by_category[category_name]['carbon'] += investment.carbon_impact
            impact_by_category[category_name]['energy'] += investment.energy_impact
            impact_by_category[category_name]['water'] += investment.water_impact
    
    # Round category impacts
    for category in impact_by_category:
        impact_by_category[category] = {k: round(v) for k, v in impact_by_category[category].items()}
    
    # Get recent investments
    recent_investments = sorted(
        grouped_investments.values(),
        key=lambda x: x['last_investment_date'],
        reverse=True
    )[:5]
    for investment_data in recent_investments:
        investment_data['impact_metrics'] = {k: round(v) for k, v in investment_data['impact_metrics'].items()}

    # Get investment distribution by category
    category_distribution = investments.values('initiative__categories__name').annotate(total=Sum('amount')).order_by('-total')
    
    # Get monthly investment trends
    monthly_trends = investments.annotate(month=TruncMonth('created_at')).values('month').annotate(total=Sum('amount')).order_by('month')
    
    # Portfolio analysis
    try:
        analyzer = PortfolioAnalyzer()
        portfolio_analysis = analyzer.get_diversification_recommendations(user)
        portfolio_analysis['category_distribution'] = {k: float(v) for k, v in portfolio_analysis['category_distribution'].items()}
        portfolio_analysis['technology_distribution'] = {k: float(v) for k, v in portfolio_analysis['technology_distribution'].items()}
        portfolio_recommendations = portfolio_analysis['recommendations']
    except Exception as e:
        portfolio_analysis = {'category_distribution': {}, 'technology_distribution': {}, 'recommendations': []}
        portfolio_recommendations = []
        print(f"Portfolio analysis error: {str(e)}")

    context = {
        'user': user,
        'total_invested': total_invested,
        'total_impact': total_impact,
        'recent_investments': recent_investments,
        'category_distribution': category_distribution,
        'monthly_trends': monthly_trends,
        'impact_by_category': dict(impact_by_category),
        'portfolio_analysis': json.dumps(portfolio_analysis, cls=DjangoJSONEncoder),
        'portfolio_recommendations': portfolio_recommendations,
        'user_preferences': user_preferences,
        'recommended_initiatives': recommended_initiatives,
    }
    return render(request, 'users/dashboard.html', context)

@login_required
def profile(request):
    # Get or create the profile to ensure it exists
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        # Check if profile image is being updated
        if 'profile_image' in request.FILES:
            profile = request.user.profile
            profile.profile_image = request.FILES['profile_image']
            profile.save()
            messages.success(request, "Profile picture updated successfully")
            return redirect('profile')
            
        # Check if password change was submitted
        if 'old_password' in request.POST:
            password_form = PasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # Keep the user logged in after password change
                update_session_auth_hash(request, user)
                messages.success(request, 'Your password was successfully updated!')
                return redirect('profile')
            else:
                messages.error(request, 'Please correct the errors below.')
                # Pass the password form with errors to the template
                user_form = UserUpdateForm(instance=request.user)
                profile_form = UserProfileForm(instance=profile)
                context = {
                    'user_form': user_form, 
                    'profile_form': profile_form, 
                    'password_form': password_form
                }
                return render(request, 'users/profile.html', context)
                
        # Handle profile update
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = UserProfileForm(instance=profile)
        password_form = PasswordChangeForm(request.user)
    
    context = {
        'user_form': user_form, 
        'profile_form': profile_form,
        'password_form': password_form
    }
    return render(request, 'users/profile.html', context)

@login_required
def user_initiative_detail(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    user_investments = request.user.investments.filter(initiative=initiative)
    
    # Calculate total invested amount and impact with explicit FloatField
    totals = user_investments.aggregate(
        total_invested=Coalesce(Sum('amount'), 0, output_field=DecimalField()),
        carbon=Coalesce(Sum('carbon_impact'), 0, output_field=models.FloatField()),
        energy=Coalesce(Sum('energy_impact'), 0, output_field=models.FloatField()),
        water=Coalesce(Sum('water_impact'), 0, output_field=models.FloatField())
    )
    total_invested = totals['total_invested']
    impact_metrics = {
        'carbon': round(totals['carbon']),
        'energy': round(totals['energy']),
        'water': round(totals['water'])
    }
    
    # Get investment history
    investment_history = user_investments.order_by('-created_at')
    
    context = {
        'initiative': initiative,
        'total_invested': total_invested,
        'impact_metrics': impact_metrics,
        'investment_history': investment_history,
        'total_investors': initiative.investments.values('user').distinct().count(),
    }
    return render(request, 'users/user_initiative_detail.html', context)