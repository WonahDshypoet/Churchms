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
from django.urls import path, include--
from django.http import JsonResponse
from django.http import HttpResponseRedirect, HttpResponsePermanentRedirect
from django.contrib.auth import views as auth_views
from home.views import dashboard, member_dashboard

def root(request):
    return HttpResponsePermanentRedirect("https://churchms-site.webflow.io/#learn-more")


urlpatterns = [
    path('', root),    
    path("", dashboard, name="dashboard"),
    path("member/", member_dashboard, name="member_dashboard"),
    path('admin/', admin.site.urls),
    path('api/', include('home.api_urls')),
    path("logout/", auth_views.LogoutView.as_view(next_page="https://churchms-site.webflow.io/#learn-more"), name="logout"),
    path('login/', auth_views.LoginView.as_view(template_name="login.html"), name="login"),
]
