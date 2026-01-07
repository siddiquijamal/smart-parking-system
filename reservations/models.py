from django.db import models
from parking.models import ParkingSlot
from django.contrib.auth.models import User

class Reservation(models.Model):
    vehicle_number = models.CharField(max_length=20)
    slot = models.ForeignKey(ParkingSlot, on_delete=models.CASCADE)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    amount = models.IntegerField(default=100)
    is_paid = models.BooleanField(default=False)

    # Razorpay payment fields
    razorpay_order_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_payment_id = models.CharField(max_length=100, blank=True, null=True)
    razorpay_signature = models.CharField(max_length=255, blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    # Rate per hour
    RATE_PER_HOUR = 50

    def save(self, *args, **kwargs):
        # Calculate amount based on start and end time
        if self.start_time and self.end_time:
            duration = self.end_time - self.start_time
            hours = duration.total_seconds() / 3600
            self.amount = round(hours * self.RATE_PER_HOUR, 2)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.vehicle_number} - Slot {self.slot.slot_number}"
