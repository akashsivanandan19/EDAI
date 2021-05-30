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
Including another URL conf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView, RedirectView

from webapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    # url(
    #     r'^accounts/signup/company/$',
    #     # views.employee_signup,
    #     #name='employee-signup'
    # ),
    url(r'^', include('allauth_2fa.urls')),
    url(r'^', include('allauth.urls')),
    # path('test/', views.test_view, name='test'),
    path('services/<str:city>/', views.city_view, name='city'),
    path('services/<str:city>/<str:category>', views.appointment_booking_view, name='appointment-booking'),
    path('accounts/', include('allauth.urls')),
    path('account/signup/professional', views.professional_signup_view, name='signup'),
    path('dashboard', views.customer_dashboard_view, name="dashboard"),
    path('employee/dashboard', views.employee_dashboard_view, name="dashboard"),
    path('', views.landing_view, name="home"),
    path('success/', views.success_view, name="success"),
    path('accounts/profile/create', views.profile_creation_view, name='profile-create'),
    path('profile/', views.profile_view, name="profile"), ]
# path("employee/signup", views.employee_signup, name="employee-login"),
