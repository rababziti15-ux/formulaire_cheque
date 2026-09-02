from django.db import models

class Cheque(models.Model):
    numero_cheque = models.CharField(max_length=50, unique=True, verbose_name="Numéro du chèque")
    matricule = models.CharField(max_length=50, verbose_name="Matricule du camion")
    date_remise = models.DateField(verbose_name="Date de remise")
    montant_initial = models.FloatField(verbose_name="Montant initial (MAD)")
    
    # Champs mis à jour automatiquement par l'algorithme
    montant_consomme = models.FloatField(default=0.0, verbose_name="Montant consommé")
    solde_restant = models.FloatField(blank=True, null=True, verbose_name="Solde restant")
    date_epuisement = models.DateField(blank=True, null=True, verbose_name="Date d'épuisement")
    est_actif = models.BooleanField(default=True, verbose_name="Chèque actif")

    def save(self, *args, **kwargs):
        # Si c'est un nouveau chèque, le solde restant est égal au montant initial
        if self.solde_restant is None:
            self.solde_restant = self.montant_initial
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.numero_cheque} - {self.matricule} ({self.montant_initial} MAD)"