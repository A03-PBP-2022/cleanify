from django.db import models
from authc.models import User

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.TextField()
	content = models.TextField()
	created_timestamp = models.DateTimeField(auto_now_add=True)
	modified_timestamp = models.DateTimeField(auto_now=True)

	class Meta:
		permissions = [
			("change_self_post", "Can edit posts made by the user"),
			("change_other_post", "Can edit posts made by other users"),
			("delete_self_post", "Can delete posts made by the user"),
			("delete_other_post", "Can delete posts made by other users"),
		]

	def __str__(self) -> str:
		return str(self.title)
	
class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE)
	created_timestamp = models.DateTimeField(auto_now_add=True)
	modified_timestamp = models.DateTimeField(auto_now=True)

	class Meta:
		permissions = [
			("change_self_comment", "Can edit comments made by the user"),
			("change_other_comment", "Can edit comments made by other users"),
			("delete_self_comment", "Can delete comments made by the user"),
			("delete_other_comment", "Can delete comments made by other users")
		]

	def __str__(self) -> str:
		return str(self.pk)
