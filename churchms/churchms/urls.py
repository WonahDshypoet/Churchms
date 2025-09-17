"""
URL configuration for churchms project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from home.auth_views import RegisterView, CustomLoginView, CurrentUserView, EmailLoginView
from django.http import HttpResponsePermanentRedirect
from django.contrib.auth import views as auth_views
from home.views import dashboard, member_dashboard, register_view
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from rest_framework_simplejwt.views import TokenRefreshView


def root(request):
    return HttpResponsePermanentRedirect("https://churchms-site.webflow.io/#learn-more")


urlpatterns = [
    path('', root),    
    path("dashboard/", dashboard, name="dashboard"),
    path("login/", EmailLoginView.as_view(), name="login"),
    path("member/", member_dashboard, name="member"),
    path('admin/', admin.site.urls),
    path('api/', include('home.api_urls')),
    path("logout/", auth_views.LogoutView.as_view(next_page="https://churchms-site.webflow.io/#learn-more"), name="logout"),
    path("register/", register_view, name="register"),
    path("auth/me/", CurrentUserView.as_view(), name="auth_me"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
