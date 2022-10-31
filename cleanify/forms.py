from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from cleanify.models import User


class RegistrationForm(UserCreationForm):
	email = forms.EmailField(max_length=60, help_text='Wajib memasukkan alamat email.')

	class Meta:
		model = User
		fields = ('email', 'username', 'password1', 'password2', 'nama', 'kontak', 'alamat','role')

    #referensi : https://youtu.be/oZUb372g6Do

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

        
    #referensi : https://youtu.be/tTvSl3RHBjE