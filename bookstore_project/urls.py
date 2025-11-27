from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.urls import re_path
from django.views.static import serve

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path('catalog/', include('catalog.urls')), 
]

if not settings.DEBUG:
    urlpatterns += [
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
    ]

handler404 = "catalog.views.error_404"
handler500 = "catalog.views.error_500"
handler403 = "catalog.views.error_403"
handler400 = "catalog.views.error_400"