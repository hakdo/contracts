from django import forms

from .models import Contract, Partner

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