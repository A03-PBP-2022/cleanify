from django.shortcuts import render
from .models import FAQ
from .forms import FAQForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.core import serializers
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, permission_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
# @permission_required('faq.view_faq')
def index(request):
    faqs = FAQ.objects.order_by('-thumbsUp')
    context = {'faqs': faqs}
    return render(request, 'faq.html', context)

# @permission_required('faq.view_faq')
def json(request):
    # sort according to thumbs up
    data = serializers.serialize('json', FAQ.objects.order_by('-thumbsUp'))

    return HttpResponse(data, content_type="application/json")

@login_required
@permission_required('faq.update_faq')
def update_thumbsUp(request):
    pk = request.POST.get('pk')
    faq = FAQ.objects.get(pk=pk)

    # update thumbs up
    faq.thumbsUp += 1
    faq.save(update_fields=['thumbsUp'])

    # sorting
    data = serializers.serialize('json', FAQ.objects.order_by('-thumbsUp'))

    return HttpResponseRedirect('/faq')

@permission_required('faq.add_faq')
def add(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['q']
            answer = form.cleaned_data['a']
            FAQ.objects.create(question = question, answer = answer)
            return HttpResponseRedirect('/faq')
    else:
        form = FAQForm()

    return render(request, 'faq-form.html', {'form': form})

@csrf_exempt
# @permission_required('faq.add_faq')
def Add_from_flutter(request):
    if request.method == 'POST':

        new_FAQ = FAQ.objects.create(
            question = request.POST['q'],
            answer = request.POST['a'],
        )

        new_FAQ.save()


    return JsonResponse({"instance": "FAQ berhasil ditambahkan"}, status=200)


