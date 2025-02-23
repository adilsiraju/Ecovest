from django.shortcuts import render, get_object_or_404
from .models import Initiative

def initiative_list(request):
    initiatives = Initiative.objects.all()
    return render(request, 'initiatives/list.html', {'initiatives': initiatives})

def initiative_detail(request, pk):
    initiative = get_object_or_404(Initiative, pk=pk)
    return render(request, 'initiatives/detail.html', {'initiative': initiative})