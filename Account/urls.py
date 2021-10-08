from django.contrib.auth import login
from django.urls import path, include
from . import views
import  django.contrib.auth.views as auth_views


app_name='Account'

urlpatterns = [

    path('login/', auth_views.LoginView.as_view(template_name='Account/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    
]