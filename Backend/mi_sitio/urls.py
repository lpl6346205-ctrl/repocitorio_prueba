"""
URL configuration for mi_sitio project.

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
from django.urls import path
from django.views.generic import RedirectView
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('userregistration/', views.userregistration),
    path('', RedirectView.as_view(url='userregistration/')),  # Redirige la raíz a userregistration
    path('api/login/', views.login_api, name='login_api'),
    path('api/logout/', views.logout_api, name='logout_api'),
    path('api/auth-status/', views.check_auth_api, name='auth_status'),
    path('employee_registration/', views.employee_registration, name = 'employee_registration'),
    path('employees/', views.employee_list, name = 'employee_list'),
    path('employees/<int:pk>/', views.edit_employee, name = 'edit_employee')
]

