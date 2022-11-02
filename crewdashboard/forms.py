from django import forms
from crewdashboard.models import Locations

class FormReport(forms.ModelForm):
    class Meta:
        model = Locations
        fields = ["date", "location", "urgency", "description"]

    def __str__(self):
        return ""