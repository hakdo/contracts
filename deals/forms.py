from django import forms

from .models import Contract

class ContractForm(forms.ModelForm):
    
    class Meta:
        model = Contract
        fields = ('contract_party', 'description', 'valid_from', 'expires', 'contract_type', 'status')
        widgets = {
            'valid_from': forms.DateInput(attrs={'type': 'date'}),
            'expires': forms.DateInput(attrs={'type': 'date'}),
        }

        