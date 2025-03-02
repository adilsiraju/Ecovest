from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from initiatives.models import Initiative
from decimal import Decimal
from datetime import datetime

@login_required
def create_investment(request, pk):
    """Handle creating a new investment."""
    initiative = get_object_or_404(Initiative, pk=pk)
    
    if request.method == 'POST':
        # Convert the amount to Decimal
        try:
            amount = Decimal(request.POST.get('amount', '0'))
        except:
            messages.error(request, 'Invalid investment amount. Please enter a valid number.')
            return redirect('initiative-detail', pk=pk)
        
        if amount <= 0:
            messages.error(request, 'Invalid investment amount. Please enter a positive number.')
        else:
            initiative.amount_raised += amount  # Now both are Decimal
            initiative.save()
            request.user.investment_set.create(
                initiative=initiative,
                amount=amount
            )
            initiative.check_funding_status()
            messages.success(request, f'Successfully invested ${amount:.2f} in {initiative.title}.')
    

        return redirect('initiative-detail', pk=pk)
    
    return redirect('initiative-detail', pk=pk)