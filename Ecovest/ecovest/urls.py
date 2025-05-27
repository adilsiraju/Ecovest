from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.defaults import page_not_found, server_error

handler404 = page_not_found
handler500 = server_error

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
    path('users/', include('users.urls')),
    path('initiatives/', include('initiatives.urls')),
    path('investments/', include('investments.urls')),
    path('onboarding/', include('onboarding.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)