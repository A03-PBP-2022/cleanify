from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test, permission_required
from django.http import HttpResponse
from django.core import serializers
from .models import Location
import datetime
from django.views.decorators.csrf import csrf_exempt
from .forms import FormReport
from django.shortcuts import redirect

# Create your views here.

@permission_required('crewdashboard:view_location')
def show_locations(request):
    return render(request, "dashboard.html")

@permission_required('crewdashboard:delete_location')
def delete_card(request):
    if request.method == "POST":
        card = Location.objects.get(id=request.POST["id"])
        card.delete()
    return redirect('todolist:show_todolist')

@permission_required('crewdashboard:view_location')
def show_json(request):
    data = Location.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@permission_required('crewdashboard:add_location')
def add_new_locations(request):
    context ={}
    context['form']= FormReport()
    if request.method == 'POST':
        location = request.POST.get('location')
        urgency = request.POST.get('urgency')
        description = request.POST.get('description')
        new_location = Location(
            date = datetime.datetime.now(),
            location = location,
            urgency = urgency,
            description = description,
        )
        new_location.save()
    return render(request, 'locations.html', context)
