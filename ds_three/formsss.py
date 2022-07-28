from django import forms


class MyfileUploadForm__(forms.Form):    
    files_data__ = forms.FileField(widget=forms.FileInput(attrs={'class':'form-control'}))