from django.shortcuts import render
from django.http import HttpResponse
from blog.models import Post, Comment

def show_index_blog(request):

	posts = Post.objects.all()
	print(posts)

	return render(request, "blog-index.html", {
		'posts': posts
	})


def show_post(request, id):

	post = Post.objects.filter(pk=id)

	if not post:
		return HttpResponse(status=404)
	
	print(post)

	return render(request, "view-post.html", {
		'post': post[0]
	})

def create_post_page(request):

	return render(request, "create-post.html", {})
