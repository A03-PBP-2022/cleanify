from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.core import serializers
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage
from authc.models import User
from blog.forms import PostForm, CommentForm
from blog.models import Post, Comment
from datetime import date, datetime
from django.views.decorators.csrf import csrf_exempt
import bleach
import json

def HttpResponseJson(json_obj, **kwargs):
	return HttpResponse(json.dumps(json_obj), content_type="application/json", **kwargs)

def apires_ok(data={"status": "OK"}):
	return HttpResponseJson(data, status=200)

def apires_created(data={"status": "Created"}):
	return HttpResponseJson(data, status=201)

def apires_bad_request(data={"status": "Bad Request"}):
	return HttpResponseJson(data, status=400)

def apires_unauthorized(data={"status": "Forbidden"}):
	return HttpResponseJson(data, status=403)

def apires_not_found(data={"status": "Not Found"}):
	return HttpResponseJson(data, status=404)

def object_to_json(data):
	return json.loads(serializers.serialize("json", [data]))[0]

def list_posts(request):
	if not request.method == "GET":
		return apires_bad_request([])

	posts = Post.objects.all()
	paginator = Paginator(posts, 10)
	page_number = request.GET.get('page') or 1
	
	return HttpResponse(serializers.serialize("json", paginator.get_page(page_number)), content_type="application/json")

def get_post(request, post_id):
	if not request.method == "GET":
		return apires_bad_request([])

	post = Post.objects.filter(pk=post_id).first()
	
	if not post:
		return apires_not_found([])
	
	return JsonResponse(object_to_json(post))

@csrf_exempt
def create_post(request):
	if not request.user.is_authenticated or not request.user.has_perm('blog.add_post'):
		return apires_unauthorized([])
	if not request.method == "POST":
		return apires_bad_request([])
	
	form = PostForm(request.POST or json.loads(request.body), instance=Post())

	if not form.is_valid():
		return apires_bad_request([])
	
	post = form.save(commit=False)
	post.title = bleach.clean(post.title)
	post.content = bleach.clean(post.content)
	post.author = request.user
	post.save()
	form.save_m2m()
	
	return apires_created(object_to_json(post))

@csrf_exempt
def edit_post(request, post_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.change_other_post') or request.user.has_perm('blog.change_self_post')):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_bad_request()
	if not request.user.has_perm('blog.change_other_post'):
		if not request.user != post.author:
			return apires_unauthorized()

	data = request.POST or json.loads(request.body)

	post.title = bleach.clean(data['title'])
	post.content = bleach.clean(data['content'])
	post.save()

	return apires_ok(object_to_json(post))

@csrf_exempt
def delete_post(request, post_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.delete_other_post') or request.user.has_perm('blog.delete_self_post')):
		return apires_unauthorized()
	if not request.method == "DELETE":
		return apires_bad_request()
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_bad_request()
	if not request.user.has_perm('blog.delete_other_post'):
		if not request.user != post.author:
			return apires_unauthorized()

	post.delete()

	return apires_ok()

def list_comments(request, post_id):
	if not request.method == "GET":
		return apires_bad_request([])
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_not_found([])
	
	comments_all = Comment.objects.filter(post=post)
	paginator = Paginator(comments_all, 10)
	page_number = request.GET.get('page') or 1
	
	try:
		comments = json.loads(serializers.serialize("json", paginator.page(page_number)))
	except EmptyPage:
		return apires_ok([])
		
	for comment in comments:
		
		user = User.objects.get(pk=comment['fields']['author'])

		comment['fields']['author'] = {
			'username': user.username,
			'name': user.name,
		}

		comment['perms'] = {
			'edit': (user == request.user and request.user.has_perm('blog.change_self_comment')) or request.user.has_perm('blog.change_other_comment'),
			'delete': (user == request.user and request.user.has_perm('blog.delete_self_comment')) or request.user.has_perm('blog.delete_other_comment'),
		}

	return apires_ok(comments)

def get_comment(request, post_id, comment_id):
	if not request.method == "GET":
		return apires_bad_request([])
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_not_found([])
	
	comment = Comment.objects.filter(post=post, pk=comment_id).first()

	return apires_ok(object_to_json(comment))

@csrf_exempt
def create_comment(request, post_id):
	if not request.user.is_authenticated or not request.user.has_perm('blog.add_comment'):
		return apires_unauthorized()
	if not request.method == "POST":
		return apires_bad_request()
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_not_found()

	form = CommentForm(request.POST or json.loads(request.body), instance=Comment())

	if not form.is_valid():
		return apires_bad_request()
	
	comment = form.save(commit=False)
	comment.content = bleach.clean(comment.content)
	comment.author = request.user
	comment.post = post
	comment.save()
	form.save_m2m()

	return apires_created(object_to_json(comment))

@csrf_exempt
def edit_comment(request, post_id, comment_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.change_other_comment') or request.user.has_perm('blog.change_self_comment')):
		return apires_unauthorized([])
	if not request.method == "POST":
		return apires_bad_request([])
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_not_found([])
	
	comment = Comment.objects.filter(pk=comment_id).first()

	if not comment or not comment.post == post:
		return apires_bad_request([])
	if not request.user.has_perm('blog.change_other_comment'):
		if not request.user != post.author:
			return apires_unauthorized([])
		
	data = request.POST or json.loads(request.body)
	
	comment.content = bleach.clean(data['content'])
	comment.save()

	return apires_created(object_to_json(comment))

@csrf_exempt
def delete_comment(request, post_id, comment_id):
	if not request.user.is_authenticated or not (request.user.has_perm('blog.delete_other_comment') or request.user.has_perm('blog.delete_self_comment')):
		return apires_unauthorized()
	if not (request.method == "DELETE" or request.method == "POST"):
		print(request.post)
		return apires_bad_request()
	
	post = Post.objects.filter(pk=post_id).first()

	if not post:
		return apires_not_found()
	if not request.user.has_perm('blog.delete_other_comment'):
		if not request.user != post.author:
			return apires_unauthorized()
	
	comment = Comment.objects.filter(pk=comment_id).first()

	if not comment or not comment.post == post:
		return apires_not_found()
	
	comment.delete()

	return apires_ok()
