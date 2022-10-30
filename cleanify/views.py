from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
import json
from .forms import RegistrationForm, UserAuthenticationForm


def registration_view(request):
	def is_ajax(request):
		return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'

	context = {}
	if request.POST and is_ajax(request):
		form = RegistrationForm(request.POST)
		data = {}
		if form.is_valid():
			form.save()
			data['success'] = True
			return HttpResponse(json.dumps(data), content_type='application/json')
		else:
			data['error'] = form.errors
			data['success'] = False
			context['registration_form'] = form
			return HttpResponse(json.dumps(data), content_type='application/json')

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)

def login_view(request):
	context = {}
	user = request.user
	# if user.is_authenticated:
	# 	return redirect('cleanify: dashboard') #ganti ini sama nama page dashboard

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				return redirect('cleanify : dashboard')			
	else:
		form = UserAuthenticationForm()
	context['login_form'] = form

	return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect('cleanify:dashboard') 