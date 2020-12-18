from django import forms


class DocumentForm(forms.Form):
    docfile = forms.FileField(
            label='select a file',
            help_text='max 42MB'
            )
