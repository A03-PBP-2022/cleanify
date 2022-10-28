from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post, Comment
from django.contrib.auth.decorators import login_required

def show_index(request):

	posts = Post.objects.all()

	return render(request, "index-blog.html", {
		'posts': posts
	})

def view_post(request, id):

	post = Post.objects.get(pk=id)

	if not post:
		return HttpResponse(status=404)
	
	comments = Comment.objects.filter(post=post)

	return render(request, "post.html", {
		'post': post,
		'comments': comments
	})

@login_required
def create_post(request):

	return render(request, "post-create.html", {})

@login_required
def edit_post(request, id):

	post = Post.objects.get(pk=id)

	if not post:
		return HttpResponse(status=404)

	return render(request, "post-edit.html", {
		'post': post
	})