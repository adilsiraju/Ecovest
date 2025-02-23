from django.urls import path
from . import views

urlpatterns = [
    path('initiative/<int:pk>/update/', views.add_progress_update, name='add-progress-update'),
]