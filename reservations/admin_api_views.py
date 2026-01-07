from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from .models import ParkingSlot
from .serializers import ParkingSlotSerializer
from .permissions import IsAdminUserOnly

# ✅ ADD SLOT
@api_view(['POST'])
@permission_classes([IsAdminUserOnly])
def add_slot(request):
    serializer = ParkingSlotSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ✅ VIEW ALL SLOTS
@api_view(['GET'])
@permission_classes([IsAdminUserOnly])
def admin_all_slots(request):
    slots = ParkingSlot.objects.all()
    serializer = ParkingSlotSerializer(slots, many=True)
    return Response(serializer.data)


# ✅ UPDATE SLOT STATUS
@api_view(['PUT'])
@permission_classes([IsAdminUserOnly])
def update_slot(request, pk):
    try:
        slot = ParkingSlot.objects.get(id=pk)
    except ParkingSlot.DoesNotExist:
        return Response({"error": "Slot not found"}, status=404)

    serializer = ParkingSlotSerializer(slot, data=request.data, partial=True)

    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)


# ✅ DELETE SLOT
@api_view(['DELETE'])
@permission_classes([IsAdminUserOnly])
def delete_slot(request, pk):
    try:
        slot = ParkingSlot.objects.get(id=pk)
    except ParkingSlot.DoesNotExist:
        return Response({"error": "Slot not found"}, status=404)

    slot.delete()
    return Response({"message": "Slot deleted successfully"})
