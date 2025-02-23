from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import login
from . forms import CustomUserCreationForm
from . forms import ProfileUpdateForm

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
    total_carbon = sum(inv.amount * inv.initiative.carbon_saved for inv in investments)
    total_energy = sum(inv.amount * inv.initiative.energy_saved_generated for inv in investments)
    total_water = sum(inv.amount * inv.initiative.water_saved for inv in investments)
    
    return render(request, 'users/dashboard.html', {
        'investments': investments,
        'total_invested': total_invested,
        'total_carbon': total_carbon,
        'total_energy': total_energy,
        'total_water': total_water,
    })

@login_required
def profile_update(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')
    else:
        form = ProfileUpdateForm(instance=request.user)
    return render(request, 'users/profile_update.html', {'form': form})