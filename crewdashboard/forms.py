from django import forms
from crewdashboard.models import Location

class FormReport(forms.ModelForm):
    class Meta:
        model = Location
        fields = ["date", "location", "urgency", "description"]

    def __str__(self):
        return ""