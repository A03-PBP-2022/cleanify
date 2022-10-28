from django import forms
from .models import FAQ

class FAQForm(forms.ModelForm):
    class Meta:
        model = FAQ
        fields = ['q', 'a']
    
    q_attrs = {
        'type':'text',
        'placeholder':'Ask your question here',
        'class':'form-control'
    }

    a_attrs = {
        'type':'text',
        'placeholder':'Input your answer here',
        'class':'form-control'
    }

    q = forms.CharField(label="question",required=True, max_length=400, widget=forms.TextInput(attrs=q_attrs))
    a = forms.CharField(label="answer",required=True, widget=forms.Textarea(attrs=a_attrs))
