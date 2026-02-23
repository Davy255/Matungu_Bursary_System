"""
URL configuration for bursary_system project.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users import views as users_views

urlpatterns = [
    path('', users_views.index_view, name='index'),
    path('admin/', admin.site.urls),
    path('users/', include('users.urls')),
    path('schools/', include('schools.urls')),
    path('applications/', include('applications.urls')),
    path('notifications/', include('notifications.urls')),
    path('admin-panel/', include('admin_panel.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

admin.site.site_header = "Bursary Management System"
admin.site.site_title = "Bursary Admin"
admin.site.index_title = "Welcome to Bursary Management System"
