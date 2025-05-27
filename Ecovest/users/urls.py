from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.profile, name='profile'),
    path('initiative/<int:pk>/', views.user_initiative_detail, name='user_initiative_detail'),
]