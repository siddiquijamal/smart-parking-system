from django.urls import path
from . import views

urlpatterns = [
    path('add_slot/', views.add_slot, name='add_slot'),
]
