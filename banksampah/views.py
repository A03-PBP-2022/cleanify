import datetime
from django.shortcuts import render
from banksampah.forms import FormBank
from banksampah.models import Bank
from django.http import JsonResponse


# Create your views here.
def create_post(request):
    context ={}
    context['form']= FormBank()
    if request.method == 'POST':
        jenis = request.POST.get('jenis')
        alamat = request.POST.get('alamat')
        tanggal = request.POST.get('tanggal')
        kontak = request.POST.get('kontak')
        
        new_project = Bank(
            jenis=jenis,
            alamat=alamat,
            tanggal=tanggal,
            kontak=kontak,
        )
        new_project.save()
    return render(request, 'banksampah.html', context)

def show_bank(request):
    data_bank = Bank.objects.all()
    context = {
    'list_bank': data_bank,
    }
    return render(request, "showbank.html", context)

def delete_bank(request, id):
    bank = Bank.objects.get(id=id)
    bank.delete()
    return show_bank(request)