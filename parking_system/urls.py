"""
URL configuration for parking_system project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

def home_redirect(request):
    return redirect('reservationpage')

from django.urls import path, include
from reservations import views as res_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', res_views.home_page, name='home'),
    path('', include('reservations.urls')),
    path('api/', include('reservations.api_urls')),

     path('', include('accounts.urls')),   # 👈 add this
     path('', include('parking.urls')),   # 👈 add this
    #  path('', include('parking.api_urls')),   # 👈 add this
# other URLs like reservation page
]
