from django import forms


class QuoteForm(forms.Form):
    firstname = forms.CharField(label="Your firstname", max_length=100)
    lastname = forms.CharField(label="Your lastname", max_length=100)
    email = forms.EmailField(label="Your email", max_length=100)
