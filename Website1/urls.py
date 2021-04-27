"""Website1 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    url(
        r'^accounts/signup/company/$',
        views.employer_signup,
        name='employer-signup'
    ),
    url(r'^', include('allauth_2fa.urls')),
    url(r'^', include('allauth.urls')),
    path('login_new', views.login_test_view),
    path('signup_new', views.signup_test_view),
    path('accounts/', include('allauth.urls')),
    path('', views.landing_view, name="home"),
    path("employer/signup", views.employer_signup, name="employee-login"), ]
