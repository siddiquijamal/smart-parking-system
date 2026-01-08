from django.contrib import admin

# Register your models here.

from .models import ParkingSlot

# admin.site.register(ParkingSlot)

from django.contrib import admin
from .models import ParkingSlot

@admin.register(ParkingSlot)
class ParkingSlotAdmin(admin.ModelAdmin):
    list_display = ('slot_number', 'status')
    list_filter = ('status',)
    search_fields = ('slot_number',)
