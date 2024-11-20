from django import forms
from .models import UserDetail


tailwindcss = 'dark:bg-gray-700 dark:text-white rounded-lg p-2 w-full'
class UserDetailForm(forms.ModelForm):
    class Meta:
        model = UserDetail
        fields = ['bio', 'location', 'birth_date', 'profile_pic', 'role', 'institute']
        widgets = {
            'bio': forms.Textarea(attrs={'rows': 3, 'class': tailwindcss}),
            'location': forms.TextInput(attrs={'class': tailwindcss}),
            'birth_date': forms.DateInput(attrs={'type': 'date', 'class': tailwindcss}),
            
            'role': forms.Select(attrs={'class': tailwindcss}),
            'institute': forms.TextInput(attrs={'class': tailwindcss}),
        }