"""
URL configuration for config project.

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
# Import the views from your dashboard app
from dashboard.views import home_view, dashboard_home
urlpatterns = [
    # 1. Map the root URL ('/') to the home_view
    path('', home_view, name='home'), 

    # 2. Map /dashboard/ to the dashboard view
    path('dashboard/', dashboard_home, name='dashboard_home'),
    path('admin/', admin.site.urls),
    # Add Allauth URLs for all account management
    path('accounts/', include('allauth.urls')),
]
