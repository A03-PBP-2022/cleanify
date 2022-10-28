from django.shortcuts import render
from .models import FAQ
from .forms import FAQForm
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import QueryDict
from django.core import serializers
from django.contrib.auth.decorators import login_required
import json
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def faq_index(request):
    faqs = FAQ.objects.order_by('-thumbsUp')
    context = {'faqs': faqs}
    return render(request, 'faq.html', context)

def faq_json(request):
    # sort according to thumbs up
    data = serializers.serialize('json', FAQ.objects.order_by('-thumbsUp'))

    return HttpResponse(data, content_type="application/json")

csrf_exempt
def faq_update_thumbsUp(request):
    pk = request.POST.get('pk')
    faq = FAQ.objects.get(pk=pk)

    # update thumbs up
    faq.thumbsUp += 1
    faq.save(update_fields=['thumbsUp'])

    # sorting
    data = serializers.serialize('json', FAQ.objects.order_by('-thumbsUp'))

    return HttpResponseRedirect('/faq')

def faq_add(request):
    if request.method == 'POST':
        form = FAQForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['q']
            answer = form.cleaned_data['a']
            FAQ.objects.create(question = question, answer = answer)
            return HttpResponseRedirect('/faq')
    else:
        form = FAQForm()

    return render(request, 'form4faq.html', {'form': form})

