from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import ParkingSlot, Reservation
from .serializers import ParkingSlotSerializer, ReservationSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import RetrieveAPIView


from django.utils import timezone
from rest_framework.permissions import AllowAny
from rest_framework.decorators import permission_classes


def update_slot_statuses():
    now = timezone.now()

    for slot in ParkingSlot.objects.all():
        active = Reservation.objects.filter(
            slot=slot,
            start_time__lte=now,
            end_time__gte=now,
            is_paid=True
        ).exists()

        future = Reservation.objects.filter(
            slot=slot,
            start_time__gt=now,
            is_paid=True
        ).exists()

        if active:
            slot.status = ParkingSlot.OCCUPIED
        elif future:
            slot.status = ParkingSlot.RESERVED
        else:
            slot.status = ParkingSlot.AVAILABLE

        slot.save()
        
        
class ReservationDetailView(RetrieveAPIView):
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    permission_classes = [IsAuthenticated]  # or AllowAny if you want
    lookup_field = 'id'



# ✅ All slots
@api_view(['GET'])
@permission_classes([AllowAny])
def all_slots(request):
    update_slot_statuses()   # 🔥 ADD THIS LINE
    slots = ParkingSlot.objects.all()
    serializer = ParkingSlotSerializer(slots, many=True)
    return Response(serializer.data)



# ✅ Dashboard counts
@api_view(['GET'])
@permission_classes([AllowAny])
def slot_counts(request):
    update_slot_statuses()   # 🔥 ADD THIS LINE
    data = {
        "total": ParkingSlot.objects.count(),
        "available": ParkingSlot.objects.filter(status=ParkingSlot.AVAILABLE).count(),
        "reserved": ParkingSlot.objects.filter(status=ParkingSlot.RESERVED).count(),
        "occupied": ParkingSlot.objects.filter(status=ParkingSlot.OCCUPIED).count(),
    }
    return Response(data)




# ✅ Create reservation endpoint

@api_view(['POST'])
@permission_classes([IsAuthenticated])  # only logged-in users
def create_reservation(request):
    update_slot_statuses()  # ensure slot statuses are up-to-date

    # Pass request in context so HiddenField (user) works
    serializer = ReservationSerializer(data=request.data, context={'request': request})
    serializer.is_valid(raise_exception=True)  # auto 400 if invalid

    slot = serializer.validated_data['slot']
    start = serializer.validated_data.get('start_time')
    end = serializer.validated_data.get('end_time')

    # Check if slot is available
    if slot.status != ParkingSlot.AVAILABLE:
        return Response(
            {"error": f"Slot {slot.slot_number} is already booked or occupied"},
            status=status.HTTP_400_BAD_REQUEST
        )

    # Check for overlapping reservations
    if start and end:
        conflict = Reservation.objects.filter(
            slot=slot,
            start_time__lt=end,
            end_time__gt=start,
             is_paid=True
        ).exists()
        if conflict:
            return Response(
                {"error": "This slot is already booked for this time"},
                status=status.HTTP_400_BAD_REQUEST
            )

    # Save reservation (user automatically attached)
    serializer.save()

    # Update slot status to RESERVED
    slot.status = ParkingSlot.RESERVED
    slot.save()

    # Return reservation + dashboard counts
    return Response({
        "reservation": serializer.data,
        "dashboard": {
            "total": ParkingSlot.objects.count(),
            "available": ParkingSlot.objects.filter(status=ParkingSlot.AVAILABLE).count(),
            "reserved": ParkingSlot.objects.filter(status=ParkingSlot.RESERVED).count(),
            "occupied": ParkingSlot.objects.filter(status=ParkingSlot.OCCUPIED).count(),
        }
    }, status=status.HTTP_201_CREATED)
