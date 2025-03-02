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
    path('admin/', admin.site.urls),
    
    path('', landing_page, name='landing'),  # Landing page as the home page
    path('home/', initiative_views.initiative_list, name='home'),  # Move old home page to /home/

    path('initiatives/<int:pk>/', initiative_views.initiative_detail, name='initiative-detail'),
    path('invest/<int:pk>/', investment_views.create_investment, name='invest'),
    path('dashboard/', user_views.dashboard, name='dashboard'),
    
    path('register/', user_views.register, name='register'),
    path('accounts/', include('django.contrib.auth.urls')),  # Includes login/logout URLs
    path('profile/update/', user_views.profile_update, name='profile_update'),
    
    path('initiatives/', include('initiatives.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
