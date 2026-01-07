from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='loginpage'),
    path('register/', views.register_view, name='registerationspage'),
    path('logout/', views.logout_view, name='logoutpage'),
]
