from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.models import Group
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
	if user.is_authenticated:
		if 'GET' in request and 'next' in request.GET:
			pass
		else:
			return redirect('index:index_page')

	if request.POST:
		form = UserAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)
			if user:
				login(request, user)
				user_authc = User.objects.get(pk=user.pk)

				print(user_authc.role)

				if user_authc.role == 'crew':
					user_group = Group.objects.get_or_create(name='crew')[0]
					user_authc.groups.add(user_group)
				elif user_authc.role == 'user':
					user_group = Group.objects.get_or_create(name='user')[0]
					user_authc.groups.add(user_group)

				if 'next' in request.POST and request.POST['next']:
					return redirect(request.POST['next'])
				return redirect('index:index_page')			
	else:
		form = UserAuthenticationForm()
	context['login_form'] = form

	return render(request, "login.html", context)

def logout_view(request):
    logout(request)
    return redirect('authc:login') 