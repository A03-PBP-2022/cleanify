from tkinter.tix import Select
from django import forms
from django import forms
from banksampah.models import Bank

class FormBank(forms.ModelForm):
    class Meta:
        model = Bank
        fields = ["tanggal", "kontak", "alamat", "jenis"]