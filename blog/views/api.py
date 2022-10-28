from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from datetime import date, datetime
import bleach
import json

def HttpResponseJson(json_obj, **kwargs):
	return HttpResponse(json.dumps(json_obj), content_type="application/json", **kwargs)

def apires_ok():
	return HttpResponseJson({"status": "OK"}, status=200)

def apires_created():
	return HttpResponseJson({"status": "Created"}, status=201)

def apires_bad_request():
	return HttpResponseJson({"status": "Bad Request"}, status=400)

def apires_unauthorized():
	return HttpResponseJson({"status": "Forbidden"}, status=403)

def apires_not_found():
	return HttpResponseJson({"status": "Not Found"}, status=404)

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
		return apires_not_found()
	
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
	to_save.title = bleach.clean(to_save.title)
	to_save.content = bleach.clean(to_save.content)
	to_save.author = request.user
	to_save.save()
	form.save_m2m()
	
	return HttpResponseJson({"id": to_save.pk}, status=201)

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

	data = request.POST or json.loads(request.body)

	post.title = bleach.clean(data['title'])
	post.content = bleach.clean(data['content'])
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
		return apires_not_found()
	
	comments = Post.objects.filter(post=post)

	return JsonResponse(comments)

def get_comment(request, post_id, comment_id):
	if not request.method == "GET":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_not_found()
	
	comment = Post.objects.get(post=post, pk=comment_id)

	return JsonResponse(comment)

def create_comment(request, post_id):
	if not request.user.is_authenticated or not request.user.has_perm('create_comment'):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_not_found()

	form = CommentForm(request.POST or json.loads(request.body), instance=Comment())

	if not form.is_valid():
		return apires_bad_request()
	
	to_save = form.save(commit=False)
	to_save.content = bleach.clean(to_save.content)
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
		return apires_not_found()
	
	comment = Comment.objects.get(pk=comment_id)

	if not comment or not comment.post == post:
		return apires_bad_request()
	if not request.user.has_perm('blog.edit_other_comment'):
		if not request.user != post.author:
			return apires_unauthorized()
		
	data = request.POST or json.loads(request.body)
	
	comment.content = clean(data['content'])
	comment.save()

	return apires_created()

def delete_comment(request, post_id, comment_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.delete_other_comment') or request.user.has_perm('blog.delete_self_comment')):
		return apires_unauthorized()
	if not request.method == "DELETE":
		return apires_bad_request()
	
	post = Post.objects.get(pk=post_id)

	if not post:
		return apires_not_found()
	if not request.user.has_perm('blog.delete_other_comment'):
		if not request.user != post.author:
			return apires_unauthorized()
	
	comment = Comment.objects.get(pk=comment_id)

	if not comment or not comment.post == post:
		return apires_not_found()
	
	comment.delete()

	return apires_ok()
