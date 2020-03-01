from django import forms
from django.contrib.auth.models import User
from .models import Contract, Partner, Organization
from django.contrib.auth.password_validation import validate_password

class ContractForm(forms.ModelForm):
    
    class Meta:
        model = Contract
        fields = ('contract_party', 'description', 'valid_from', 'expires', 'contract_type', 'status')
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'expires': forms.DateInput(attrs={'type': 'date'}),
        }

class PartnerForm(forms.ModelForm):

    class Meta:
        model = Partner
        fields = ('name', 'entity_type',)

class MemberConfigForm(forms.Form):
    update_organization_secret = forms.BooleanField(initial=False, required=False)
    allow_new_members = forms.BooleanField(required=False)

class RegisterForm(forms.Form):
    username = forms.CharField(max_length=128)
    password = forms.CharField(max_length=128, widget=forms.PasswordInput, validators=[validate_password])
    confirm_password = forms.CharField(max_length=128, widget=forms.PasswordInput)
    secret_code = forms.UUIDField()

    def clean_username(self):
        cleaned_data = super().clean()
        data = cleaned_data['username']
        # Check if this username exists
        usersearch = User.objects.filter(username = data)
        if usersearch:
            raise forms.ValidationError("You have to pick a different username.")
        return data
    
    def clean_secret_code(self):
        cleaned_data = super().clean()
        data = cleaned_data['secret_code']
        # Check that it exists...
        myorg = Organization.objects.filter(orgsecret = data)
        if len(myorg) == 0:
            raise forms.ValidationError("This invite code is invalid.")
        if not myorg[0].accepting_members:
            raise forms.ValidationError("This invite code is invalid or has expired.")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password')
        password2 = cleaned_data.get('confirm_password')

        if password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data