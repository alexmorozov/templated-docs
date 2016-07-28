#--coding: utf8--

from django import forms

from invoices.models import Customer


class InvoiceForm(forms.Form):
    FORMAT_CHOICES = (
        ('pdf', 'PDF'),
        ('docx', 'MS Word'),
        ('html', 'HTML'),
    )
    number = forms.CharField(label='Invoice #')
    customer = forms.ModelChoiceField(queryset=Customer.objects.all())
    subject = forms.CharField()
    amount = forms.DecimalField()
    model = forms.CharField(
        required=False,
        help_text="Optional. Absolute Path for alternative ODT template."
    )
    format = forms.ChoiceField(choices=FORMAT_CHOICES)
