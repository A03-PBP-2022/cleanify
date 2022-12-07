from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, authenticate, logout
from .models import User
from django.contrib.auth.models import Group, Permission
import json
from .forms import RegistrationForm, UserAuthenticationForm
from django.contrib import messages
from django.views.decorators.csrf import csrf_exempt

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		data = {}
		if form.is_valid():
			form.save()
			data['success'] = True
			return JsonResponse({
				"success": True,
				"message": "Registration success!",
			}, status=200)
		else:
			return JsonResponse({
				"success": False,
				"message": "Registration failed!",
				"error": form.errors
			}, status=400)

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'register.html', context)

def login_view(request):
	context = {}
	# user = request.user
	if request.user.is_authenticated:
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
				_update_user_roles(user_authc)

				if 'next' in request.POST and request.POST['next']:
					return redirect(request.POST['next'])
				return redirect('index:index_page')

			else:
				messages.info(request, 'Login failed! Check your username and/or password.')	

	else:
		form = UserAuthenticationForm()
	context['login_form'] = form

	return render(request, "login.html", context)

def logout_view(request):
	logout(request)
	return redirect('authc:login') 

@csrf_exempt
def api_login(request):

	try:
		email = request.POST['email']
		password = request.POST['password']
		user = authenticate(email=email, password=password)
		
		if user:
			login(request, user)
			user_authc = User.objects.get(pk=user.pk)
			_update_user_roles(user_authc)
			
			print(user_info(request.user))
			return JsonResponse({
				"status": True,
				"message": "Login success!",
				"info": user_info(request.user)
			}, status=200)

		else:
			return JsonResponse({
				"status": False,
				"message": "Login failed! Check your username and/or password."
			}, status=401)
		
	except:
		return JsonResponse({
			"status": False,
			"message": "Invalid request! Check your inputs again! This may happen on wrong credentials."
		})

@csrf_exempt
def api_register(request):

	try:
		form = RegistrationForm(request.POST)

		if form.is_valid():
			form.save()
			return JsonResponse({
				"status": True,
				"message": "Registration success!",
			}, status=200)
		else:
			return JsonResponse({
				"status": False,
				"message": "Registration failed!",
				"details": form.errors
			}, status=400)
	except:
		return JsonResponse({
			"status": False,
			"message": "Invalid request! Check your inputs again! This may happen on wrong credentials."
		})

@csrf_exempt
def api_logout(request):

	logout(request)
	return JsonResponse({
		"status": True,
		"message": "Logged out!"
	}, status=200)

def _update_user_roles(user_authc):
	if user_authc.role == 'crew':
		user_group = Group.objects.get_or_create(name='crew')[0]
		user_authc.groups.add(user_group)
	elif user_authc.role == 'user':
		user_group = Group.objects.get_or_create(name='user')[0]
		user_authc.groups.add(user_group)

def get_user_permissions(user):
	if user.is_superuser:
		return Permission.objects.all()
	if not user.is_authenticated:
		return user.user_permissions.all()
	return user.user_permissions.all() | Permission.objects.filter(group__user=user)

def get_user_permissions_list(user):
	
	perms = get_user_permissions(user)
	perms_codenames = []
	
	for perm in perms:
		perms_codenames.append(perm.codename)

	return perms_codenames

def user_info(user):
	email = None
	username = None
	name = None
	phoneNumber = None
	address = None
	role = "anonymous"
	permissions = get_user_permissions_list(user)
	if user.is_authenticated:
		user_obj: User = User.objects.get(pk=user.pk)
		email = user_obj.email
		username = user_obj.username
		name = user_obj.name
		phoneNumber = user_obj.phoneNumber
		address = user_obj.address
		role = user_obj.role
		if user.is_superuser:
			role = "superuser"
	
	return {
		"email": email,
		"username": username,
		"name": name,
		"phoneNumber": phoneNumber,
		"address": address,
		"role": role,
		"permissions": permissions,
	}

def api_info(request):

	# print(user_info(request.user))
	return JsonResponse(user_info(request.user))