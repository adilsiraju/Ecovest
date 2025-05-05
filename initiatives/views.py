from django.shortcuts import redirect, render, get_object_or_404
from .models import Initiative, Category
from investments.models import Investment
from django.db.models import Q, ExpressionWrapper, F, Sum, FloatField, DecimalField, Count
from django.core.paginator import Paginator
from django.db.models.functions import Coalesce, Cast
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import InitiativeForm
from django.urls import reverse

def initiative_list(request):
    initiatives = Initiative.objects.all()
    
    # Apply filters
    category = request.GET.get('category')
    status = request.GET.get('status')
    search = request.GET.get('search')
    sort = request.GET.get('sort', 'newest')
    
    if category:
        initiatives = initiatives.filter(categories__name=category)
    if status:
        initiatives = initiatives.filter(status=status)
    if search:
        initiatives = initiatives.filter(title__icontains=search)
    
    # Apply sorting
    if sort == 'progress':
        initiatives = initiatives.order_by('-current_amount')
    elif sort == 'amount':
        initiatives = initiatives.order_by('-goal_amount')
    else:  # newest
        initiatives = initiatives.order_by('-created_at')
    
    # Calculate total metrics
    total_initiatives = Initiative.objects.count()
    total_investors = Initiative.objects.aggregate(total=Count('investments__user', distinct=True))['total']
    total_invested = Initiative.objects.aggregate(total=Sum('current_amount'))['total'] or 0
    
    # Calculate impact for ₹1000 using static method
    total_carbon = 0
    for initiative in initiatives:
        impact = Investment.calculate_impact_for_amount(initiative, 1000)
        print(f"Initiative: {initiative.title}, Predicted Impact: {impact}")  # Debugging log
        initiative.impact_for_1000 = {k: round(float(v), 2) for k, v in impact.items()}  # Ensure numeric values
        total_carbon += initiative.impact_for_1000.get('carbon', 0)
    
    # Pagination
    paginator = Paginator(initiatives, 8)
    page = request.GET.get('page')
    initiatives = paginator.get_page(page)
    
    context = {
        'initiatives': initiatives,
        'categories': Category.objects.all(),
        'total_initiatives': total_initiatives,
        'total_investors': total_investors,
        'total_invested': total_invested,
        'total_carbon': total_carbon,
    }
    return render(request, 'initiatives/initiative_list.html', context)

def initiative_detail(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    
    # Calculate impact for ₹1000 using static method
    impact_metrics = Investment.calculate_impact_for_amount(initiative, 1000)
    impact_metrics = {k: round(float(v), 2) for k, v in impact_metrics.items()}
    
    # Get recent investments
    recent_investments = initiative.investments.all().order_by('-created_at')[:5]
    
    # Get similar initiatives
    similar_initiatives = Initiative.objects.filter(
        categories__in=initiative.categories.all()
    ).exclude(pk=initiative.pk).distinct()[:3]
    
    context = {
        'initiative': initiative,
        'impact_metrics': impact_metrics,
        'recent_investments': recent_investments,
        'similar_initiatives': similar_initiatives,
        'total_investors': initiative.investments.values('user').distinct().count(),
    }
    return render(request, 'initiatives/initiative_detail.html', context)
