from django import forms
from .models import Account, Address

class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Confirm Password'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'placeholder': 'Enter Password'
    }))
    phone_number= forms.CharField(widget=forms.TextInput(attrs={
        'type':'number',
    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email', 'password', 'phone_number', 'phone_number_prefix']

    def clean(self):
        cleaned_data = super(RegistrationForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!" )
            
    def __init__(self, *args, **kwargs):
        super(RegistrationForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class AddressForm(forms.ModelForm):

    class Meta:
        model  = Address
        exclude = ('user',)           

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.fields['pincode'].widget.attrs['id'] = 'pincode'
        self.fields['pincode'].widget.attrs['onblur'] = 'getPin()'
        self.fields['pincode'].widget.attrs['onfocus'] = 'removePin()'
        self.fields['state'].widget.attrs['id'] = 'state'
        self.fields['city'].widget.attrs['id'] = 'district'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'