import razorpay
from django.conf import settings
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Reservation, ParkingSlot

client = razorpay.Client(
    auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
)

# ✅ CREATE PAYMENT ORDER
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_payment_order(request):
    print("User making request:", request.user)
    print("Data received:", request.data)
    print("KEY ID:", settings.RAZORPAY_KEY_ID)
    print("KEY SECRET:", settings.RAZORPAY_KEY_SECRET)

    reservation_id = request.data.get("reservation_id")

    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=404)

    if reservation.is_paid:
        return Response({"error": "Reservation already paid"}, status=400)

    # ✅ CREATE CLIENT HERE (IMPORTANT)
    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    amount_in_paise = int(reservation.amount * 100)

    try:
        order = client.order.create({
            "amount": amount_in_paise,
            "currency": "INR",
            "payment_capture": 1
        })

        reservation.razorpay_order_id = order["id"]
        reservation.save()

        return Response({
            "order_id": order["id"],
            "amount": amount_in_paise,  # ✅ send paise
            "key": settings.RAZORPAY_KEY_ID
        })

    except Exception as e:
        return Response(
            {"error": f"Razorpay order creation failed: {str(e)}"},
            status=500
        )



# ✅ VERIFY PAYMENT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def verify_payment(request):
    data = request.data

    try:
        reservation = Reservation.objects.get(
            razorpay_order_id=data.get("razorpay_order_id")
        )
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=404)

    try:
        client.utility.verify_payment_signature({
            "razorpay_order_id": data.get("razorpay_order_id"),
            "razorpay_payment_id": data.get("razorpay_payment_id"),
            "razorpay_signature": data.get("razorpay_signature"),
        })

        reservation.is_paid = True
        reservation.razorpay_payment_id = data.get("razorpay_payment_id")
        reservation.razorpay_signature = data.get("razorpay_signature")
        reservation.save()

        # Update slot
        slot = reservation.slot
        slot.status = ParkingSlot.RESERVED
        slot.save()

        return Response({"message": "Payment successful"})

    except razorpay.errors.SignatureVerificationError:
        return Response({"error": "Payment verification failed"}, status=400)


# ✅ OPTIONAL CONFIRM PAYMENT
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def confirm_payment_api(request, reservation_id):
    try:
        reservation = Reservation.objects.get(id=reservation_id)
    except Reservation.DoesNotExist:
        return Response({"error": "Reservation not found"}, status=404)

    reservation.is_paid = True
    reservation.save()

    slot = reservation.slot
    slot.status = ParkingSlot.OCCUPIED
    slot.save()

    return Response({
        "message": "Payment confirmed",
        "slot_number": slot.slot_number,
        "slot_status": slot.status
    })
