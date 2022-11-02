from django.shortcuts import render
from django.contrib.auth.decorators import login_required, user_passes_test
from django.http import HttpResponse
from django.core import serializers
from .models import Locations
import datetime
from django.views.decorators.csrf import csrf_exempt
from .forms import FormReport

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
    # form = FormReport()
    # if request.method == "POST":
    #     form = FormReport(request.POST)
    #     if form.is_valid():
    #         dlocation = form.cleaned_data["location"]
    #         durgency = form.cleaned_data["urgency"]
    #         ddescription = form.cleaned_data["description"]
    #         dtime = datetime.datetime.now()
    #         updated = Locations(location = dlocation, urgency = durgency, description =ddescription, date = dtime)
    #         updated.save()
    # context = {
    #     'form': form,
    # }
    # return render(request, "locations.html", context)
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
    # if request.method == 'POST':
    #     location = request.POST.get('location')
    #     urgency = request.POST.get('urgency')
    #     description = request.POST.get('description')
    #     new_location = Locations.objects.create(
    #         date = datetime.datetime.now(),
    #         location = location,
    #         urgency = urgency,
    #         description = description,
    #         )
    #     new_location.save()
    #     return HttpResponse("")
    # return render(request, 'locations.html')