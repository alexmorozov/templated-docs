#--coding: utf8--

from django import forms


class SampleForm(forms.Form):
    FORMAT_CHOICES = (
        ('pdf', 'PDF'),
        ('odt', 'OpenDocument'),
        ('docx', 'MS Word'),
        ('png', 'Image'),
        ('html', 'Web page'),
    )
    name = forms.CharField(
        initial='John Doe',
        required=True)
    origin = forms.CharField(
        label='Where are you from?',
        initial='Some lovely place')
    output_format = forms.TypedChoiceField(
        label='Which document format do you want?',
        choices=FORMAT_CHOICES,
        coerce=str,
        initial='pdf')
