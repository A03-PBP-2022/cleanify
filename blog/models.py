from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	title = models.TextField()
	content = models.TextField()
	timestamp = models.DateTimeField()

	def __str__(self) -> str:
		return self.title
	
class Comment(models.Model):
	author = models.ForeignKey(User, on_delete=models.CASCADE)
	content = models.TextField()
	timestamp = models.DateTimeField()
	post = models.ForeignKey(Post, on_delete=models.CASCADE)

	def __str__(self) -> str:
		return self.pk