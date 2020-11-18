from django.urls import path, include
from . import views


urlpatterns = [

    path('status', views.status, name='status'),
    path('trigger_devices', views.trigger_devices, name='trigger_devices'),

]
