from django import forms


class ContactForm(forms.Form):
    first_name = forms.CharField(label='First name', max_length=100)
    last_name = forms.CharField(label='Last name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    email = forms.EmailField(label='Email', required=False)
    address = forms.CharField(label='Address', max_length=100)
    address2 = forms.CharField(label='Address 2', max_length=100, required=False)
    country = forms.ChoiceField(label='Country', choices=[('US', 'United States')])  # Add more options if needed
    state = forms.ChoiceField(label='State', choices=[('CA', 'California')])  # Add more options if needed
    zip_code = forms.CharField(label='Zip', max_length=10)
