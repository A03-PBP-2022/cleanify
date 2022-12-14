from django.urls import path, include
from .views import api, api2, page
app_name = 'blog'

urlpatterns = [
	path('', page.show_index, name='index'),
	path('new/', page.create_post, name='create_post'),
	path('<int:id>/', page.view_post, name='view_post'),
	path('<int:id>/edit', page.edit_post, name='edit_post'),
    
    path('api2/', include(api2.router.urls)),
    
	path('api/post', api.list_posts, name='api_list_posts'),
	path('api/post/new', api.create_post, name='api_create_post'),
	path('api/post/<int:post_id>', api.get_post, name='api_get_post'),
    path('api/post/<int:post_id>/edit', api.edit_post, name="api_edit_post"),
    path('api/post/<int:post_id>/delete', api.delete_post, name="api_delete_post"),
	path('api/post/<int:post_id>/comment', api.list_comments, name="api_list_comments"),
	path('api/post/<int:post_id>/comment/new', api.create_comment, name="api_create_comment"),
    path('api/post/<int:post_id>/comment/<int:comment_id>', api.get_comment, name="api_get_comment"),
    path('api/post/<int:post_id>/comment/<int:comment_id>/edit', api.edit_comment, name="api_edit_comment"),
    path('api/post/<int:post_id>/comment/<int:comment_id>/delete', api.delete_comment, name="api_delete_comment")
]