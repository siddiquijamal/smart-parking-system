from rest_framework import serializers
from .models import Reservation, ParkingSlot

class ParkingSlotSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParkingSlot
        fields = ["id", "slot_number", "status"]

class ReservationSerializer(serializers.ModelSerializer):
    slot = ParkingSlotSerializer(read_only=True)
    slot_id = serializers.PrimaryKeyRelatedField(
        queryset=ParkingSlot.objects.all(),
        source="slot",
        write_only=True
    )

    class Meta:
        model = Reservation
        fields = [
            "id",
            "vehicle_number",
            "slot",          # ✅ MUST include this
            "slot_id",       # ✅ write-only
            "start_time",
            "end_time",
            "amount",
            "is_paid",
            "razorpay_order_id",
            "razorpay_payment_id",
            "razorpay_signature",
        ]
