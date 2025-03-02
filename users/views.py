from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib import messages
from .forms import CustomUserCreationForm, ProfileUpdateForm
from decimal import Decimal
from datetime import datetime, timedelta
import random
from json import dumps

def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Your account has been created successfully!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = CustomUserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required
def dashboard(request):
    investments = request.user.investment_set.select_related('initiative')
    total_invested = sum(inv.amount for inv in investments)
    
    # Calculate environmental impact metrics
    total_carbon = sum(inv.amount * inv.initiative.carbon_saved for inv in investments)
    total_energy = sum(inv.amount * inv.initiative.energy_saved_generated for inv in investments)
    total_water = sum(inv.amount * inv.initiative.water_saved for inv in investments)
    total_trees = total_carbon / Decimal('21.77')  # 1 tree ≈ 21.77 kg CO₂
    total_plastic = total_water / Decimal('1000')  # Example: 1 kg plastic ≈ 1000 liters water saved

    # Prepare data for the "Your Holdings" table
    holdings_data = []
    for investment in investments:
        roi = Decimal(str(investment.initiative.roi))  # Convert to Decimal safely
        current_value = investment.amount * (Decimal('1') + roi/Decimal('100'))  # Calculate with ROI
        holdings_data.append({
            'initiative': investment.initiative,
            'amount': investment.amount,
            'current_value': current_value,
            'roi': roi
        })

    # Prepare data for the line graph (value of holdings over time)
    today = datetime.today()
    dates = [(today - timedelta(days=i)).strftime("%b %d") for i in range(6, -1, -1)]
    
    # Generate random values for the graph (convert to float for JSON serialization)
    values = [float(total_invested * (Decimal('1') + Decimal(str(random.uniform(-0.1, 0.1))))) for _ in range(7)]

    line_graph_data = {
        'labels': dumps(dates),
        'values': dumps(values)
    }

    return render(request, 'users/dashboard.html', {
        'total_invested': total_invested,
        'total_carbon': total_carbon,
        'total_energy': total_energy,
        'total_water': total_water,
        'total_trees': total_trees,
        'total_plastic': total_plastic,
        'investments': holdings_data,
        'line_graph_data': line_graph_data,
    })

@login_required
def profile_update(request):
    """Handle updating the user's profile."""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})

def user_login(request):
    """Handle user login."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in successfully!')
            return redirect('dashboard')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    return render(request, 'registration/login.html')

