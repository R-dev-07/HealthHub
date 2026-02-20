"""
URL configuration for healthhub project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from healthhub import views as core_views

urlpatterns = [
    path('', core_views.home, name='home'),
    path('register/', core_views.register, name='register'),
    path('login/', core_views.user_login, name='login'),
    path('logout/', core_views.user_logout, name='logout'),
    
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    
    # App URLs
    path('patients/', include('patients.urls')),
    path('doctors/', include('doctors.urls')),
    path('hospitals/', include('hospitals.urls')),
    path('labs/', include('labs.urls')),
    path('pharmacy/', include('pharmacy.urls')),
    path('appointments/', include('appointments.urls')),
    path('payments/', include('payments.urls')),
    path('chat/', include('chat.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    if 'django_debug_toolbar' in settings.INSTALLED_APPS:
        import debug_toolbar
        urlpatterns = [
            path('__debug__/', include(debug_toolbar.urls)),
        ] + urlpatterns
