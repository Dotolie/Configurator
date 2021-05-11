from django import forms
from django.forms import ModelForm

# ------ ywkim
from .models import MyDevice
# ------ 


class DocumentForm(forms.Form):
    docfile = forms.FileField(
            label='select a file',
            help_text='max 42MB'
            )

class deviceForm(ModelForm):
    class Meta:
        model = MyDevice
        fields = ['mainPort', 'subPort', 'deviceName', 'deviceSpeed', 'deviceBus' ]
        
