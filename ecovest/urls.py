"""
URL configuration for ecovest project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from initiatives import views as initiative_views
from investments import views as investment_views
from users import views as user_views
from . views import landing_page
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    # Django admin interface URL
    path('admin/', admin.site.urls),
    
    # Landing page - serves as the root/index page (www.example.com/)
    path('', landing_page, name='landing'),
    
    # Initiative list page - shows all climate initiatives (www.example.com/home/)
    path('projects/', initiative_views.initiative_list, name='projects'),

    # Detailed view for a specific initiative using its ID (www.example.com/initiatives/1/)
    path('initiatives/<int:pk>/', initiative_views.initiative_detail, name='initiative-detail'),
    
    # Investment creation endpoint for a specific initiative (www.example.com/invest/1/)
    path('invest/<int:pk>/', investment_views.create_investment, name='invest'),
    
    # User dashboard showing investments and stats (www.example.com/dashboard/)
    path('dashboard/', user_views.dashboard, name='dashboard'),
    
    # User registration page (www.example.com/register/)
    path('register/', user_views.register, name='register'),
    
    # Django's built-in auth URLs (login, logout, password reset, etc.)
    path('accounts/', include('django.contrib.auth.urls')),
    
    # User profile update page (www.example.com/profile/update/)
    path('profile/update/', user_views.profile_update, name='profile_update'),
    
    # Include all URLs from the initiatives app
    path('initiatives/', include('initiatives.urls')),
    
    # Serves media files (user uploads) during development
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)