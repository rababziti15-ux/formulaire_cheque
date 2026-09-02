import pandas as pd
from sqlalchemy import create_engine
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import ChequeForm
from .models import Cheque

def ajouter_cheque(request):
    # Si le responsable a cliqué sur "Enregistrer" (Méthode POST)
    if request.method == 'POST':
        form = ChequeForm(request.POST)
        if form.is_valid():
            form.save() # C'est cette ligne qui injecte directement dans PostgreSQL !
            messages.success(request, "Le chèque a été enregistré avec succès dans la base de données.")
            return redirect('ajouter_cheque') # Recharge la page pour vider le formulaire
    
    # Si c'est juste un affichage normal de la page (Méthode GET)
    else:
        form = ChequeForm()
        
    return render(request, 'gestion_peage/ajouter_cheque.html', {'form': form})

def lancer_algorithme_soldes(request):
    """
    C'est le cerveau de l'application : il croise les chèques et les trajets.
    """
    try:
        # 1. Connexion à PostgreSQL pour lire la table des trajets (qui n'est pas gérée par Django)
        DATABASE_URL = "postgresql://airflow:airflow@20.100.196.68:5432/db_transport_telemetrie"
        engine = create_engine(DATABASE_URL)

        # 2. Charger les trajets par ordre chronologique
        trajets_df = pd.read_sql('SELECT * FROM trajets_geozones ORDER BY "Date départ", "Heure départ"', engine)
        
        # Convertir la colonne date de Pandas pour la comparer avec les dates Django
        trajets_df['Date départ'] = pd.to_datetime(trajets_df['Date départ']).dt.date

        # 3. Récupérer uniquement les chèques qui sont encore "Actifs"
        cheques_actifs = Cheque.objects.filter(est_actif=True)

        # 4. LA LOGIQUE MATHÉMATIQUE
        for cheque in cheques_actifs:
            solde = cheque.montant_initial
            date_epuisement = None

            # On filtre : Même matricule ET Date trajet >= Date de remise du chèque
            trajets_valides = trajets_df[
                (trajets_df['Matricule'] == cheque.matricule) & 
                (trajets_df['Date départ'] >= cheque.date_remise)
            ]

            # On soustrait chaque péage un par un
            for index, trajet in trajets_valides.iterrows():
                prix_peage = float(trajet['Prix Péage (MAD)'])
                
                if prix_peage > 0:
                    solde -= prix_peage
                    
                    # Si le chèque tombe dans le rouge, on note la date et on arrête de chercher !
                    if solde <= 0:
                        date_epuisement = trajet['Date départ']
                        break 
            
            # 5. Sauvegarde des résultats dans PostgreSQL
            cheque.solde_restant = solde
            cheque.montant_consomme = cheque.montant_initial - solde
            
            if solde <= 0:
                cheque.est_actif = False
                cheque.date_epuisement = date_epuisement
                
            cheque.save() # Django met à jour la table gestion_peage_cheque automatiquement

        messages.success(request, "🧠 Algorithme terminé : Tous les soldes ont été mis à jour avec succès !")
        
    except Exception as e:
        messages.error(request, f"Erreur lors du calcul : {str(e)}")

    # On redirige vers la page d'accueil après le calcul
    return redirect('ajouter_cheque')