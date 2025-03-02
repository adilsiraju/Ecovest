from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.db.models import Q
from .models import Initiative, ProgressUpdate, Category
from .forms import ProgressUpdateForm

def initiative_list(request):
    """Display a list of initiatives with search and filtering options."""
    initiatives = Initiative.objects.all()
    categories = Category.objects.all()
    # Search functionality
    query = request.GET.get('q')
    if query:
        initiatives = initiatives.filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )

    # Filter by category
    category_id = request.GET.get('category')
    if category_id:
        initiatives = initiatives.filter(category_id=category_id)

    return render(request, 'initiatives/list.html', {
        'initiatives': initiatives,
        'category_choices': categories,
    })

def initiative_detail(request, pk):
    """Display details of a specific initiative."""
    initiative = get_object_or_404(Initiative, pk=pk)
    return render(request, 'initiatives/detail.html', {'initiative': initiative})

@login_required
@user_passes_test(lambda u: u.is_staff)
def add_progress_update(request, pk):
    """Add a progress update for a specific initiative (admin-only)."""
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            progress_update = form.save(commit=False)
            progress_update.initiative = initiative
            progress_update.save()
            messages.success(request, 'Progress update added successfully!')
            return redirect('initiative-detail', pk=pk)
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = ProgressUpdateForm()
    return render(request, 'initiatives/add_progress_update.html', {'form': form, 'initiative': initiative})

@login_required
@user_passes_test(lambda u: u.is_staff)
def mark_as_completed(request, pk):
    """Mark an initiative as completed (admin-only)."""
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        if initiative.status == 'funded':
            initiative.status = 'completed'
            initiative.save()
            messages.success(request, 'Initiative marked as completed!')
    return redirect('initiative-detail', pk=pk)