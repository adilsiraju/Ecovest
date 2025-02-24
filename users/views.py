from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from . forms import CustomUserCreationForm
from . forms import ProfileUpdateForm
from decimal import Decimal

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
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
    total_trees = sum(inv.amount * (inv.initiative.carbon_saved / Decimal('21.77')) for inv in investments)  # 1 tree ≈ 21.77 kg CO₂
    total_plastic = sum(inv.amount * (inv.initiative.water_saved / Decimal('1000')) for inv in investments)  # Example: 1 kg plastic ≈ 1000 liters water saved

    return render(request, 'users/dashboard.html', {
        'investments': investments,
        'total_invested': total_invested,
        'total_carbon': total_carbon,
        'total_energy': total_energy,
        'total_water': total_water,
        'total_trees': total_trees,
        'total_plastic': total_plastic,
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile has been updated successfully!')
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})

from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

def user_login(request):
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