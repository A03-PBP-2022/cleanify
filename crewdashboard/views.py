from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core import serializers
from .models import Locations
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.

def is_crew(user):
    return user.groups.filter(name='crew').exists()

@login_required
@user_passes_test(is_crew)
def show_locations(request):
    return render(request, "dashboard.html")

def show_json(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@login_required
def add_new_locations(request):
    if request.method == 'POST':
        location = request.POST.get('location')
        urgency = request.POST.get('urgency')
        description = request.POST.get('description')

        new_location = Locations.objects.create(
            date = datetime.datetime.now(),
            location = location,
            urgency = urgency,
            description = description,
            )
        new_location.save()
        return HttpResponse("")
    return render(request, 'locations.html');