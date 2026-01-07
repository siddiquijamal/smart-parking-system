from django.urls import path

from reservations.views import ReservationDetailView
from .api_views import all_slots, slot_counts, create_reservation
from .auth_api_views import register_api, login_api, logout_api
from .admin_api_views import add_slot, admin_all_slots, update_slot, delete_slot
from .payment_api_views import confirm_payment_api, create_payment_order, verify_payment


urlpatterns = [
    path('slots/', all_slots),
    path('dashboard/', slot_counts),
    path('reserve/', create_reservation),
]


urlpatterns += [
    path('auth/register/', register_api),
    path('auth/login/', login_api),
    path('auth/logout/', logout_api),
]


urlpatterns += [
    path('admin/slots/', admin_all_slots),
    path('admin/slots/add/', add_slot),
    path('admin/slots/update/<int:pk>/', update_slot),
    path('admin/slots/delete/<int:pk>/', delete_slot),
]


urlpatterns += [
    path('payment/create-order/', create_payment_order),
    path('payment/verify/', verify_payment),
    # urls.py
    path('reservations/<int:reservation_id>/confirm-payment/', confirm_payment_api),
    path('reservations/<int:id>/', ReservationDetailView.as_view(), name='reservation_detail'),  # ✅ add this
]




