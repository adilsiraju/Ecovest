from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from initiatives.models import Initiative
from .models import Investment, InvestmentGoal
from .impact_calculator import ImpactCalculator
from decimal import Decimal, InvalidOperation
from django.contrib import messages
from django.http import JsonResponse

# Note: Avoid global instantiation of ImpactCalculator due to potential threading issues
# We'll instantiate it within the view instead

@login_required
def invest_initiative(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    
    # Check if initiative is already fully funded
    if initiative.status == 'funded':
        messages.error(request, f'This initiative is already fully funded. No further investments are being accepted.')
        return redirect('initiative_detail', pk=initiative.pk)
    
    if request.method == 'POST':
        amount_str = request.POST.get('amount', '')
        print(f"Original amount string: '{amount_str}'")
        
        # Strip any commas, spaces or currency symbols
        amount_str = ''.join(c for c in amount_str if c.isdigit() or c == '.')
        print(f"Cleaned amount string: '{amount_str}'")
        
        if amount_str:
            try:
                # Convert to Decimal for precise financial calculations
                amount = Decimal(amount_str)
                print(f"Converted to Decimal: {amount}")
                
                # Check if accepting this investment would exceed goal amount
                remaining_amount = initiative.goal_amount - initiative.current_amount
                if amount > remaining_amount and remaining_amount > 0:
                    messages.warning(request, f'This initiative only needs ₹{remaining_amount:,} more to be fully funded. Would you like to invest this amount instead?')
                    # Adjust the amount to match the remaining needed amount
                    amount = remaining_amount
                
                if amount < initiative.min_investment:
                    messages.error(request, f'Minimum investment amount is ₹{initiative.min_investment:,}')
                elif initiative.max_investment and amount > initiative.max_investment:
                    messages.error(request, f'Maximum investment amount is ₹{initiative.max_investment:,}')
                else:
                    # Create the investment
                    try:
                        investment = Investment(
                            user=request.user,
                            initiative=initiative,
                            amount=amount
                        )
                        
                        # Calculate impact metrics
                        impact = Investment.calculate_impact_for_amount(initiative, amount)
                        print(f"Impact calculation result: {impact}")
                        
                        # Extract and convert impact values to float
                        investment.carbon_impact = float(impact.get('carbon', 0))
                        investment.energy_impact = float(impact.get('energy', 0))
                        investment.water_impact = float(impact.get('water', 0))
                        
                        # Save the investment - this also updates initiative's current_amount via the save method
                        investment.save()
                        
                        # Clear any previous messages to prevent old errors from showing
                        storage = messages.get_messages(request)
                        storage.used = True
                        
                        # Add success message
                        messages.success(request, f'Successfully invested ₹{amount:,} in {initiative.title}')
                        
                        # If the initiative is now fully funded, add a special message
                        if initiative.status == 'funded':
                            messages.success(request, f'Congratulations! Your investment has fully funded this initiative!')
                        
                        # Redirect to user's dashboard to see their holdings
                        return redirect('dashboard')
                        
                    except Exception as e:
                        print(f"Error saving investment: {str(e)}")
                        messages.error(request, f"An error occurred while processing your investment: {str(e)}")
                        
            except (ValueError, InvalidOperation) as e:
                print(f"Error processing amount '{amount_str}': {e}")
                messages.error(request, 'Please enter a valid amount')
        else:
            print("Amount string is empty")
            messages.error(request, 'Please enter an investment amount')
    
    # Calculate impact metrics for the template using AI predictions
    # Use the user-provided amount if valid, otherwise default to min_investment
    try:
        amount = Decimal(request.POST.get('amount', initiative.min_investment))
        if amount < initiative.min_investment:
            amount = initiative.min_investment
        elif initiative.max_investment and amount > initiative.max_investment:
            amount = initiative.max_investment
    except (ValueError, InvalidOperation):
        amount = initiative.min_investment
    
    impact_metrics = Investment.calculate_impact_for_amount(initiative, amount)
    
    context = {
        'initiative': initiative,
        'impact_metrics': impact_metrics,
        'min_investment': initiative.min_investment,
        'max_investment': initiative.max_investment,
        'roi_estimate': initiative.roi_estimate,
        'risk_level': initiative.get_risk_label(),
        'progress_percentage': initiative.get_progress_percentage()
    }
    
    return render(request, 'investments/invest.html', context)

@login_required
def add_investment_goal(request):
    if request.method == 'POST':
        goal_type = request.POST.get('goal_type')
        target_date = request.POST.get('target_date')
        
        goal = InvestmentGoal(
            user=request.user,
            goal_type=goal_type,
            target_date=target_date
        )
        
        # Set target values based on goal type
        if goal_type == 'amount':
            goal.target_amount = Decimal(request.POST.get('target_amount'))
        elif goal_type == 'impact':
            goal.target_carbon = float(request.POST.get('target_carbon', 0))
            goal.target_energy = float(request.POST.get('target_energy', 0))
            goal.target_water = float(request.POST.get('target_water', 0))
        
        goal.save()
        messages.success(request, 'Investment goal added successfully!')
        return redirect('dashboard')
    
    return render(request, 'investments/add_goal.html')


@login_required
def impact_preview(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    try:
        amount_str = request.GET.get('amount', '')
        print(f"Impact preview - original amount: '{amount_str}'")
        
        # Clean the input similar to the invest view
        amount_str = ''.join(c for c in amount_str if c.isdigit() or c == '.')
        
        if not amount_str:
            amount = initiative.min_investment
        else:
            amount = Decimal(amount_str)
            
        if amount < initiative.min_investment:
            amount = initiative.min_investment
        elif initiative.max_investment and amount > initiative.max_investment:
            amount = initiative.max_investment
    except (ValueError, InvalidOperation) as e:
        print(f"Impact preview - error processing amount: {e}")
        amount = initiative.min_investment
    
    # Get impact data with more precise calculations
    impact = Investment.calculate_impact_for_amount(initiative, amount)
    
    # Format the impact values with proper precision
    formatted_impact = {
        'carbon': round(float(impact.get('carbon', 0)), 1),
        'energy': round(float(impact.get('energy', 0)), 1),
        'water': round(float(impact.get('water', 0)), 1),
    }
    
    return JsonResponse(formatted_impact)