from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin, Group

class AccountManager(BaseUserManager):
	def create_user(self, email, username, password=None):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)
		user.set_password(password)

		if user.role == 'crew':
			user_group = Group.objects.get_or_create(name='crew')
			user.groups.add(user_group)
		else:
			user_group = Group.objects.get_or_create(name='user')
			user.groups.add(user_group)

		user.save(using=self._db)
		return user
	
	def create_superuser(self, email, username, password):
		user = self.create_user(
			email=self.normalize_email(email),
			password=password,
			username=username,
		)
		user.is_admin = True
		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)
		return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
	is_admin = models.BooleanField(default=False)
	is_active = models.BooleanField(default=True)
	is_staff = models.BooleanField(default=False)
	is_superuser = models.BooleanField(default=False)
	nama = models.CharField(max_length=100)
	kontak = models.CharField(max_length=100)
	alamat = models.TextField()
	role = models.CharField(max_length=20)

	#yang dibutuhkan untuk login 
	USERNAME_FIELD = 'email'
	#yang required saat signup
	REQUIRED_FIELDS = ['username']

	objects = AccountManager()

	def __str__(self): #yang mau ditampilin ke template
		return self.username


# link referensi : https://youtu.be/eCeRC7E8Z7Y