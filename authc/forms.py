# https://youtu.be/oZUb372g6Do
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from authc.models import User
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.utils.translation import gettext_lazy as _


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Wajib memasukkan alamat email.')

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2', 'nama', 'kontak', 'alamat','role')

# https://youtu.be/tTvSl3RHBjE
class UserAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label="password", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'password',)

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid Login")

# https://github.com/Microdisseny/django-groupadmin-users/blob/main/groupadmin_users/forms.py

# Code from https://stackoverflow.com/a/39648244/593907
# modified according to https://docs.djangoproject.com/en/1.11/topics/forms/modelforms/#the-save-method

User = get_user_model()

# Create ModelForm based on the Group model.
class GroupAdminForm(forms.ModelForm):
    class Meta:
        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple('users', False),
        label=_('Users'),
    )

    def __init__(self, *args, **kwargs):
        # Do the normal form initialisation.
        super(GroupAdminForm, self).__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields['users'].initial = self.instance.user_set.all()

    def save_m2m(self):
        # Add the users to the Group.
        # Deprecated in Django 1.10: Direct assignment to a reverse foreign key
        #                            or many-to-many relation
        self.instance.user_set.set(self.cleaned_data['users'])

    def save(self, *args, **kwargs):
        # Default save
        instance = super(GroupAdminForm, self).save()
        # Save many-to-many data
        self.save_m2m()
        return instance