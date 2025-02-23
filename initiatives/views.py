from django.shortcuts import render, get_object_or_404
from . models import Initiative, ProgressUpdate
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from . forms import ProgressUpdateForm

def initiative_list(request):
    initiatives = Initiative.objects.all()
    category_choices = Initiative.CATEGORY_CHOICES

    # Search functionality
    query = request.GET.get('q')
    if query:
        initiatives = initiatives.filter(title__icontains=query) | initiatives.filter(description__icontains=query)

    # Filter by category
    category = request.GET.get('category')
    if category:
        initiatives = initiatives.filter(category=category)

    

    return render(request, 'initiatives/list.html', {
        'initiatives': initiatives,
        'category_choices': category_choices,
    })

def initiative_detail(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    return render(request, 'initiatives/detail.html', {'initiative': initiative})

@login_required
@user_passes_test(lambda u: u.is_staff)  # Only staff (admins) can access this view
def add_progress_update(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        form = ProgressUpdateForm(request.POST)
        if form.is_valid():
            progress_update = form.save(commit=False)
            progress_update.initiative = initiative
            progress_update.save()
            return redirect('initiative-detail', pk=pk)
    else:
        form = ProgressUpdateForm()
    return render(request, 'initiatives/add_progress_update.html', {'form': form, 'initiative': initiative})

@login_required
@user_passes_test(lambda u: u.is_staff)  # Only staff (admins) can access this view
def mark_as_completed(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    if request.method == 'POST':
        if initiative.status == 'funded':
            initiative.status = 'completed'
            initiative.save()
    return redirect('initiative-detail', pk=pk)