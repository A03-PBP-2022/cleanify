import datetime
from django.shortcuts import render
from banksampah.forms import FormBank
from banksampah.models import Bank
from django.http import HttpResponseRedirect
from django.urls import reverse

# Create your views here.

def form_bank(request):
    context ={}
    context['form']= FormBank()
    return render(request, "banksampah.html", context)
