from django.urls import path, include
from . import views

urlpatterns = [
    #path('signup', views.signup, name='signup'),
    path('login', views.login, name='login'),
    path('logout', views.logout, name='logout'),
    #path('logout', views.logout, name='logout'),
    #path('operator_reg', views.operator_reg, name='operator_reg'),
    #path('register_done', views.register_done, name='register_done'),
    #path('password_change_form', views.password_change_form, name='password_change_form'),
]