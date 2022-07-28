from django import forms


class MyfileUploadForm(forms.Form):    
    files_data = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))