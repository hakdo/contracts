from django import forms
from django.contrib.auth.models import User
from .models import Contract, Partner, Organization
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _

class ContractForm(forms.ModelForm):
    
    class Meta:
        model = Contract
        fields = ('contract_party', 'description', 'valid_from', 'expires', 'contract_type', 'status','document_link','owner','notes',)
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

class RegisterNew(forms.Form):
    epost = forms.EmailField(max_length=128, label=_('E-mail'))
    passord = forms.CharField(max_length=128, widget=forms.PasswordInput, validators=[validate_password], label=_('Password'))
    bekreft_passord = forms.CharField(max_length=128, widget=forms.PasswordInput, label=_('Confirm password'))
    firmanavn = forms.CharField(max_length=128, label=_('Company name'))
    country = forms.CharField(max_length=128, label=_('Country'))
    orgno = forms.CharField(max_length=128, label=_('VAT registration number'))

    def clean_epost(self):
        cleaned_data = super().clean()
        data = cleaned_data['epost']
        # Check if this username exists
        usersearch = User.objects.filter(username = data)
        if usersearch:
            raise forms.ValidationError(_('This email address cannot be used to register an account.'))
        return data
    
    def clean_organisasjonsnummer(self):
        cleaned_data = super().clean()
        data = cleaned_data['orgno']
        # Check if this username exists
        orgsearch = Organization.objects.filter(orgnr = data)
        if orgsearch:
            raise forms.ValidationError(_('The VAT number is already in our systems.'))
        else:
            # Validate or number
            print("Need to add orgnum validation")
        return data
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('passord')
        password2 = cleaned_data.get('bekreft_passord')

        if password1 != password2:
            raise forms.ValidationError(_('Passwords do not match'))
        elif len(password1) < 8:
            raise forms.ValidationError(_('Password is too short'))
        return self.cleaned_data