from django.urls import path
from . import views

urlpatterns = [
    path('initiative/<int:pk>/update/', views.add_progress_update, name='add-progress-update'),
    path('initiative/<int:pk>/complete/', views.mark_as_completed, name='mark-as-completed'),
]