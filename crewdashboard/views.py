from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.core import serializers
from .models import Locations
import datetime

# Create your views here.

def show_locations(request):
    return render(request, "dashboard.html")

def show_json(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def add_new_locations(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        image = request.POST.get('description')
        urgency = request.POST.get('urgency')
        description = request.POST.get('description')

        new_location = Locations.objects.create(
            date = datetime.datetime.now(),
            location = location,
            image = image,
            urgency = urgency,
            description = description,
            )
        new_location.save()
        return HttpResponse("")
    return render(request, 'locations.html')