from django import forms


tailwind = "bg-gray-50 border border-gray-300 text-gray-900 text-sm rounded-lg focus:ring-blue-500 focus:border-blue-500 block w-1/2 ps-10 p-2.5  dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400 dark:text-white dark:focus:ring-blue-500 dark:focus:border-blue-500"
class RepositoryUploadForm(forms.Form):
    name = forms.CharField(max_length=255, widget=forms.TextInput(attrs={'class': f'form-control {tailwind}'}))
    description = forms.CharField(widget=forms.Textarea(attrs={'class': f'form-control {tailwind}'}), required=False)
    file = forms.FileField(widget=forms.FileInput(attrs={'class': 'form-control'}))