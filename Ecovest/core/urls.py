from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing_page'),
    path('learn-more/', views.learn_more, name='learn_more'),
]