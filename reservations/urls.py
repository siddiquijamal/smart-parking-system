from django.urls import path
from . import views

from django.urls import path
from . import views

urlpatterns = [
    path('reservationpage/', views.reserve_slot, name='reservationpage'),
    path('payment/<int:reservation_id>/', views.payment_page, name='payment_page'),
    path('confirm-payment/<int:reservation_id>/', views.confirm_payment, name='confirm_payment'),
    path("reservations/<int:id>/", views.ReservationDetailView.as_view()),

    
]



