from django.db import models

class ParkingSlot(models.Model):
    # Define constants for status
    AVAILABLE = 'available'
    RESERVED = 'reserved'
    OCCUPIED = 'occupied'

    STATUS_CHOICES = [
        (AVAILABLE, 'Available'),
        (RESERVED, 'Reserved'),
        (OCCUPIED, 'Occupied'),
    ]

    slot_number = models.CharField(max_length=10, unique=True)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=AVAILABLE
    )

    def __str__(self):
        return f"{self.slot_number} ({self.status})"
