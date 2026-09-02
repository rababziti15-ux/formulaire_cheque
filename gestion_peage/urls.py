from django.urls import path
from . import views

urlpatterns = [
    path('saisie-cheque/', views.ajouter_cheque, name='ajouter_cheque'),
    path('calculer-soldes/', views.lancer_algorithme_soldes, name='lancer_algorithme'),
]