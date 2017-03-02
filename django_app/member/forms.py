from django import forms


class MailForm(forms.Form):
    to = forms.EmailField()
    message = forms.Textarea()
    subject = forms.CharField(blank=True)
