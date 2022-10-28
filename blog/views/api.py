from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from datetime import date, datetime
import json

def apires_ok():
	return HttpResponse(status=200)

def apires_created():
	return HttpResponse(status=201)

def apires_bad_request():
	return HttpResponse(status=400)

def apires_unauthorized():
	return HttpResponse(status=403)

# TODO Cek permissions!

def list_posts(request):
	if not request.method == "GET":
		return apires_bad_request()

	# TODO Implementasi Paginator
	data = Post.objects.all()
	return HttpResponse(serializers.serialize("json", data), content_type="application/json")

def get_post(request, post_id):
	if not request.method == "GET":
		return apires_bad_request()

	post = Post.objects.get(post_id)

	if not post:
		return apires_bad_request()
	
	return JsonResponse(post)

def create_post(request):
	if not request.user.is_authenticated or not request.user.has_perm('create_post'):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	form = PostForm(request.POST or json.loads(request.body), instance=Post())

	if not form.is_valid():
		return apires_bad_request()
	
	to_save = form.save(commit=False)
	to_save.author = request.user
	to_save.save()
	form.save_m2m()
	
	return apires_created()

def edit_post(request, post_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.edit_other_post') or request.user.has_perm('blog.edit_self_post')):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()
	if not request.user.has_perm('blog.edit_other_post'):
		if not request.user != post.author:
			return apires_unauthorized()

	post.title = request.body['title']
	post.content = request.body['content']
	post.save()

	return apires_ok()

def delete_post(request, post_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.delete_other_post') or request.user.has_perm('blog.delete_self_post')):
		return apires_unauthorized()
	if not request.method == "DELETE":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()
	if not request.user.has_perm('blog.delete_other_post'):
		if not request.user != post.author:
			return apires_unauthorized()

	post.delete()

	return apires_ok()

def list_comments(request, post_id):
	if not request.method == "GET":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()
	
	comments = Post.objects.filter(post=post)

	return JsonResponse(comments)

def get_comment(request, post_id, comment_id):
	if not request.method == "GET":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()
	
	comment = Post.objects.get(post=post, pk=comment_id)

	return JsonResponse(comment)

def create_comment(request, post_id):
	if not request.user.is_authenticated or not request.user.has_perm('create_comment'):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()

	form = CommentForm(request.POST or json.loads(request.body), instance=Comment())

	if not form.is_valid():
		return apires_bad_request()
	
	to_save = form.save(commit=False)
	to_save.author = request.user
	to_save.post = post
	to_save.save()
	form.save_m2m()

	return apires_created()

def edit_comment(request, post_id, comment_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.edit_other_comment') or request.user.has_perm('blog.edit_self_comment')):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()
	
	comment = Comment.objects.get(pk=comment_id)

	if not comment or not comment.post == post:
		return apires_bad_request()
	if not request.user.has_perm('blog.edit_other_comment'):
		if not request.user != post.author:
			return apires_unauthorized()
	
	comment.content = request.body['content']
	comment.save()

	return apires_created()

def delete_comment(request, post_id, comment_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.delete_other_comment') or request.user.has_perm('blog.delete_self_comment')):
		return apires_unauthorized()
	if not request.method == "DELETE":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_bad_request()
	if not request.user.has_perm('blog.delete_other_comment'):
		if not request.user != post.author:
			return apires_unauthorized()
	
	comment = Comment.objects.get(pk=comment_id)

	if not comment or not comment.post == post:
		return apires_bad_request()
	
	comment.delete()

	return apires_ok()
