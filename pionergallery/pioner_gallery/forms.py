from django import forms
from pioner_gallery.webapp.models import Contact


class ContactForm(forms.ModelForm):
    class Meta:
        model = Contact
        fields = ['first_name', "last_name", 'email', 'message_subject', 'message_body',]
