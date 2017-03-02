from django import forms


class MailForm(forms.Form):
    to = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)
    subject = forms.CharField()
