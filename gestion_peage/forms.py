from django import forms
from .models import Cheque

class ChequeForm(forms.ModelForm):
    class Meta:
        model = Cheque
        # On ne met que les champs que le responsable doit remplir
        fields = ['numero_cheque', 'matricule', 'date_remise', 'montant_initial']
        widgets = {
            'numero_cheque': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: CH-0001'}),
            'matricule': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Scania 73596 -A-7'}),
            'date_remise': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'montant_initial': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ex: 4000'}),
        }