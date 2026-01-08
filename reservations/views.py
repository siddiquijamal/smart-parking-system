from django.shortcuts import render, redirect, get_object_or_404
from django.utils.dateparse import parse_datetime
from datetime import timedelta, datetime
from parking.models import ParkingSlot
from reservations.api_views import update_slot_statuses
from reservations.models import Reservation
from django.db.models import Q

from rest_framework.generics import RetrieveAPIView
from .models import Reservation
from .serializers import ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view

from rest_framework.permissions import IsAuthenticated

class ReservationDetailView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'id'



from parking.models import ParkingSlot

# Home page view
def home_page(request):
    # Always try to update slot statuses
    try:
        update_slot_statuses()
    except Exception as e:
        print("Slot update error:", e)

    # ALWAYS define variables (no conditions)
    available_slots = ParkingSlot.objects.filter(status=ParkingSlot.AVAILABLE)
    reserved_slots = ParkingSlot.objects.filter(status=ParkingSlot.RESERVED)
    occupied_slots = ParkingSlot.objects.filter(status=ParkingSlot.OCCUPIED)

    total_slots = ParkingSlot.objects.count()

    return render(request, 'home.html', {
        'total_slots': total_slots,
        'available_slots_count': available_slots.count(),
        'reserved_slots_count': reserved_slots.count(),
        'occupied_slots_count': occupied_slots.count(),
        'available_slots': available_slots,
        'reserved_slots': reserved_slots,
        'occupied_slots': occupied_slots
    })


from django.contrib.auth.decorators import login_required

@login_required
def reserve_slot(request):
    available_slots = ParkingSlot.objects.filter(status=ParkingSlot.AVAILABLE)
    if request.method == "POST":
        vehicle_number = request.POST.get('vehicle_number')
        slot_id = request.POST.get('slot')
        start_time = parse_datetime(request.POST.get('start_time'))
        end_time = parse_datetime(request.POST.get('end_time'))

        slot = get_object_or_404(ParkingSlot, id=slot_id)

        # Check overlapping reservations (only paid slots count)
        overlapping = Reservation.objects.filter(
            slot=slot,
            end_time__gt=start_time,
            start_time__lt=end_time,
            is_paid=True
        )

        if overlapping.exists():
            return render(request, 'reservations.html', {
                'available_slots': available_slots,
                'error': f"Slot {slot.slot_number} is already booked for this time!"
            })

        # Calculate duration and amount
        duration = end_time - start_time
        total_hours = max(1, int(duration.total_seconds() // 3600))
        rate_per_hour = 50  # Can be dynamic later
        amount = total_hours * rate_per_hour

        # Create reservation
        reservation = Reservation.objects.create(
            vehicle_number=vehicle_number,
            slot=slot,
            start_time=start_time,
            end_time=end_time,
            amount=amount
        )

        # Update slot status
        slot.status = ParkingSlot.RESERVED
        slot.save()

        # Redirect to payment page
        return redirect('payment_page', reservation_id=reservation.id)

    return render(request, 'reservations.html', {
        'available_slots': available_slots
    })


# Payment page
def payment_page(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        # Simulate payment success
        reservation.is_paid = True
        reservation.save()
        return redirect('confirm_payment', reservation_id=reservation.id)

    return render(request, 'payment.html', {'reservation': reservation})


# Confirm payment and occupy slot
def confirm_payment(request, reservation_id):
    reservation = get_object_or_404(Reservation, id=reservation_id)

    if request.method == "POST":
        reservation.is_paid = True
        reservation.save()

        # Mark slot as occupied
        slot = reservation.slot
        slot.status = 'OCCUPIED'

        slot.save()

        return render(request, 'success.html', {
            'reservation': reservation
        })
