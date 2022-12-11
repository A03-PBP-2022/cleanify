import datetime
from django.shortcuts import render
from banksampah.forms import FormBank
from banksampah.models import Bank
from django.core import serializers
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, permission_required


# Create your views here.

@permission_required('banksampah.add_bank')
def create_bank(request):
    context ={}
    context['form']= FormBank()
    if request.method == 'POST':
        user = request.user
        jenis = request.POST.get('jenis')
        alamat = request.POST.get('alamat')
        tanggal = request.POST.get('tanggal')
        kontak = request.POST.get('kontak')
        
        new_project = Bank(
            user=user,
            jenis=jenis,
            alamat=alamat,
            tanggal=tanggal,
            kontak=kontak,
        )
        new_project.save()
    return render(request, 'banksampah.html', context)

@permission_required('banksampah.view_bank')
def show_bank(request):
    data_bank = Bank.objects.all()
    context = {
        'list_bank': data_bank,
    }
    return render(request, "showbank.html", context)

@permission_required('banksampah.delete_bank')
def delete_bank(request, id):
    bank = Bank.objects.get(id=id)
    bank.delete()
    return show_bank(request)

@permission_required('banksampah.view_bank')
def show_banksampah_json(request):
    data = Bank.objects.all()
    data_banksampah = serializers.serialize("json", data)
    return HttpResponse(data_banksampah, content_type="application/json")