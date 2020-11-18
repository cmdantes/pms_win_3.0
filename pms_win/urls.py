
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('isa.urls')),
    path('isa/', include('isa.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('admin/', admin.site.urls),
    path('devices/', include('devices.urls')),
]
