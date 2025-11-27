from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('store.urls')),
    path('catalog/', include('catalog.urls')), 
]

handler404 = "catalog.views.error_404"
handler500 = "catalog.views.error_500"
handler403 = "catalog.views.error_403"
handler400 = "catalog.views.error_400"