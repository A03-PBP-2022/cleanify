from django.urls import path
from .views import api, page 
app_name = 'blog'

urlpatterns = [
	path('', page.show_index_blog, name='blog_index'),
	path('new-post/', page.create_post_page, name='blog_new_post'),
	path('<int:id>/', page.show_post, name='view_post'),
	path('api/new-post', api.new_post, name='api_new_post')
]