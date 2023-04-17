from .models import SPARQLRequest
from django.forms import ModelForm, Textarea


class SPARQLRequestForm(ModelForm):
    class Meta:
        model = SPARQLRequest
        fields = ["body"]
        widgets = {
            "body": Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter SPARQL Request'
            }),
        }