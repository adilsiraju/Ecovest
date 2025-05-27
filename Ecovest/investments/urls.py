from django.urls import path
from . import views

urlpatterns = [
    path('invest/<int:pk>/', views.invest_initiative, name='invest_initiative'),
    path('impact-preview/<int:pk>/', views.impact_preview, name='impact_preview'),
    path('goals/add/', views.add_investment_goal, name='add_investment_goal'),
]