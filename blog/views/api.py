from django.shortcuts import render
from django.http import HttpResponse
from blog.forms import PostForm
from blog.models import Post, Comment
from datetime import date

def apires_bad_request():
	return HttpResponse(status=400)

def apires_unauthorized():
	return HttpResponse(status=403)

def new_comment(request):
	# if not request.user.is_authenticated:
	# 	return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()

	return HttpResponse(status=200)

def new_post(request):
	# if not request.user.is_authenticated:
	# 	return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	form = PostForm(request.POST, instance=Post())
	if not form.is_valid():
		return apires_bad_request()
	to_save = form.save(commit=False)
	to_save.user = request.user
	to_save.timestamp = date.today()
	to_save.save()
	form.save_m2m()
	
	return HttpResponse(status=200)