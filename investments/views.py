from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from initiatives.models import Initiative
from decimal import Decimal  # Add this import
from django.contrib import messages


@login_required
def create_investment(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    
    if request.method == 'POST':
        amount = float(request.POST.get('amount', 0))
        
        # Mock payment processing
        if amount > 0:
            initiative.amount_raised += amount
            initiative.save()
            request.user.investment_set.create(
                initiative=initiative,
                amount=amount
            )
            # Check if funding goal is met
            initiative.check_funding_status()
            messages.success(request, f'Successfully invested ${amount} in {initiative.title}.')
        else:
            messages.error(request, 'Invalid investment amount. Please enter a positive number.')
        return redirect('initiative-detail', pk=pk)
    
    return redirect('initiative-detail', pk=pk)