from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from initiatives.models import Initiative
from decimal import Decimal  # Add this import

@login_required
def create_investment(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    
    if request.method == 'POST':
        # Convert the amount to Decimal instead of float
        amount = Decimal(request.POST.get('amount', 0))
        
        # Mock payment processing
        if amount > 0:
            initiative.amount_raised += amount
            initiative.save()
            request.user.investment_set.create(
                initiative=initiative,
                amount=amount
            )
        return redirect('initiative-detail', pk=pk)
    
    return redirect('initiative-detail', pk=pk)