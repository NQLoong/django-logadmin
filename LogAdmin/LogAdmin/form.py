from django import forms
from .models import SelectP

class SelectForm(forms.ModelForm):
    class Meta:
        model = SelectP
        fields = '__all__'