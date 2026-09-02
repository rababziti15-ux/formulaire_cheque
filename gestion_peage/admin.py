from django.contrib import admin
from .models import Cheque

@admin.register(Cheque)
class ChequeAdmin(admin.ModelAdmin):
    list_display = ('numero_cheque', 'matricule', 'date_remise', 'montant_initial', 'solde_restant', 'est_actif')
    list_filter = ('est_actif', 'matricule')
    search_fields = ('numero_cheque', 'matricule')