# forms.py
from django import forms

class RepositoryUploadForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': 'form-control'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}), required=False)
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))