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

# def form_bank(request):
#     context ={}
#     context['form']= FormBank()
#     return render(request, "banksampah.html", context)

# def create_post(request):
    # posts = Bank.objects.all()
    # response_data = {}

    # if request.POST.get('action') == 'post':
    #     jenis = request.POST.get('jenis')
    #     alamat = request.POST.get('alamat')
    #     tanggal = request.POST.get('tanggal')
    #     kontak = request.POST.get('kontak')

    #     response_data['jenis'] = jenis
    #     response_data['alamat'] = alamat
    #     response_data['tanggal'] = tanggal
    #     response_data['kontak'] = kontak

    #     Bank.objects.create(
    #         jenis = jenis,
    #         alamat = alamat,
    #         tanggal = tanggal,
    #         kontak = kontak,
    #         )
    #     return JsonResponse(response_data)

    # return render(request, 'banksampah.html', {'posts':posts})
