from django.urls import path
from . import views

urlpatterns = [
    path('welcome/', views.onboarding_welcome, name='onboarding_welcome'),
    path('interests/', views.onboarding_interests, name='onboarding_interests'),
    path('investment-profile/', views.onboarding_investment_profile, name='onboarding_investment_profile'),
    path('tutorial/', views.onboarding_tutorial, name='onboarding_tutorial'),
]