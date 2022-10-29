from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.views import redirect_to_login
from blog.models import Post, Comment
from django.contrib.auth.decorators import login_required, permission_required

def show_index(request):

	posts = Post.objects.all().order_by('-created_timestamp')

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

@permission_required('blog:create_post')
def create_post(request):

	return render(request, "post-create.html", {})

def edit_post(request, id):

	post = Post.objects.get(pk=id)

	if not post:
		return HttpResponse(status=404)
	
	# (request.user.has_perm('blog.delete_other_comment') or request.user.has_perm('blog.delete_self_comment'))

	if not (post.author == (request.user and request.user.has_perm('blog.edit_self_post')) or request.user.has_perm('blog.edit_other_post')):
		return redirect_to_login(request.path)
	
	return render(request, "post-edit.html", {
		'post': post
	})