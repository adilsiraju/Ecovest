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
    # Default to 'active' status if no status filter is provided
    status = request.GET.get('status')
    if status:
        initiatives = Initiative.objects.filter(status=status)
    else:
        initiatives = Initiative.objects.filter(status='active')
    
    # Apply other filters
    category = request.GET.get('category')
    search = request.GET.get('search')
    sort = request.GET.get('sort', 'newest')

    if category:
        initiatives = initiatives.filter(categories__name=category)
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

    # Calculate impact for ₹1000
    total_carbon = 0
    for initiative in initiatives:
        impact = Investment.calculate_impact_for_amount(initiative, 1000)
        if impact:
            initiative.impact_for_1000 = {k: round(float(v), 2) for k, v in impact.items()}
            total_carbon += initiative.impact_for_1000.get('carbon', 0)
        else:
            initiative.impact_for_1000 = {}

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
        'default_status': 'active' if not status else status,
    }
    return render(request, 'initiatives/initiative_list.html', context)


def initiative_detail(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)

    # Calculate impact for ₹1000
    impact_metrics = Investment.calculate_impact_for_amount(initiative, 1000)
    impact_metrics = {k: round(float(v), 2) for k, v in impact_metrics.items()} if impact_metrics else {}

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
