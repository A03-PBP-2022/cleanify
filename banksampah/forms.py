from django import forms
from django import forms
from banksampah.models import Bank

class FormBank(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["jenis", "alamat", "tanggal", "kontak"]