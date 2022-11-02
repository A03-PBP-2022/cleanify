from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core import serializers
from .models import Locations
import datetime
from django.views.decorators.csrf import csrf_exempt
from .forms import FormReport
from django.shortcuts import redirect

# Create your views here.

def is_crew(user):
    return user.groups.filter(name='crew').exists()

@login_required
@user_passes_test(is_crew)
def show_locations(request):
    return render(request, "dashboard.html")

def delete_card(request):
    if request.method == "POST":
        card = Locations.objects.get(id=request.POST["id"])
        card.delete()
    return redirect('todolist:show_todolist')

def show_json(request):
    data = Locations.objects.all()
    return HttpResponse(serializers.serialize("json", data), content_type="application/json")

@csrf_exempt
@login_required
def add_new_locations(request):
    context ={}
    context['form']= FormReport()
    if request.method == 'POST':
        location = request.POST.get('location')
        urgency = request.POST.get('urgency')
        description = request.POST.get('description')
        new_location = Locations(
            date = datetime.datetime.now(),
            location = location,
            urgency = urgency,
            description = description,
        )
        new_location.save()
    return render(request, 'locations.html', context)
