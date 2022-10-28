from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post, Comment

def show_index(request):

	posts = Post.objects.all()

	return render(request, "index-blog.html", {
		'posts': posts
	})


def show_post(request, id):

	post = Post.objects.get(pk=id)

	if not post:
		return HttpResponse(status=404)
	
	comments = Comment.objects.filter(post=post)

	return render(request, "post.html", {
		'post': post,
		'comments': comments
	})

def create_post(request):

	return render(request, "post-create.html", {})
