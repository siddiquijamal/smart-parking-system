from django.shortcuts import render

# Create your views here.

from django.shortcuts import render, redirect
from .forms import ParkingSlotForm

def add_slot(request):
    if request.method == 'POST':
        form = ParkingSlotForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')  # go back to dashboard
    else:
        form = ParkingSlotForm()

    return render(request, 'add_slot.html', {'form': form})
