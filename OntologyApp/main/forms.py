from django import forms
from django.forms.widgets import Textarea


class SPARQLRequestForm(forms.Form):
    body = forms.CharField(widget=Textarea(
        attrs={'class':'form-control', 'placeholder': 'Enter SPARQL request'}
    ))