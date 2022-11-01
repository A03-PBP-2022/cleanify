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

		user.save(using=self._db)

		return user
	
	def create_superuser(self, email, username, password):
		if not email:
			raise ValueError('Users must have an email address')
		if not username:
			raise ValueError('Users must have a username')

		user = self.model(
			email=self.normalize_email(email),
			username=username,
		)
		user.set_password(password)

		user.is_staff = True
		user.is_superuser = True
		user.save(using=self._db)

		user_group = Group.objects.get_or_create(name='administrator')[0]
		user.groups.add(user_group)

		return user

class User(AbstractBaseUser, PermissionsMixin):
	email = models.EmailField(verbose_name="email", max_length=60, unique=True)
	username = models.CharField(max_length=30, unique=True)
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