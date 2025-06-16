from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views.static import serve
from django.urls import re_path
import os

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
]

# Serve static files during development
if settings.DEBUG:
    # Serve regular static files
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    
    # Serve media files (uploaded content)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Serve files from the root static directory
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', serve, {
            'document_root': os.path.join(settings.BASE_DIR.parent.parent, 'static'),
        }),
    ]
