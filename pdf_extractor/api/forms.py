from django import forms
from .models import Pdf

class PdfForm(forms.ModelForm):
    class Meta:
        model = Pdf
        fields = ('file',)