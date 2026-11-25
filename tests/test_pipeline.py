"""Tests automatiques du pipeline de données (étape 3 du TP).

Chaque test utilise un petit jeu de données inventé dont on connaît
à l'avance le bon résultat, calculé à la main.
"""
import pandas as pd

from pipeline import agreger_par_categorie, agreger_par_ville, transformer


def donnees_exemple():
    """Petit jeu de données qui contient exprès les 4 types d'anomalies."""
    return pd.DataFrame({
        # Ligne 1 et 2 : doublon (même vente deux fois)
        # Ligne 3 : quantité manquante (None)
        # Ligne 4 : quantité négative (-1)
        # Ligne 5 : ville mal écrite (" lyon" avec un espace et en minuscules)
        "quantite": [2, 2, None, -1, 3],
        "prix_unitaire": [10.0, 10.0, 5.0, 5.0, 20.0],
        "ville": ["paris", "paris", "Lyon", "Lyon", " lyon"],
    })


def test_supprime_les_doublons_et_lignes_invalides():
    # On part de 5 lignes : on enlève le doublon, la ligne vide
    # et la quantité négative. Il doit rester 2 lignes.
    resultat = transformer(donnees_exemple())
    assert len(resultat) == 2


def test_normalise_les_villes():
    # "paris" doit devenir "Paris" et " lyon" doit devenir "Lyon".
    resultat = transformer(donnees_exemple())
    assert sorted(resultat["ville"]) == ["Lyon", "Paris"]


def test_calcule_le_montant():
    # Montant = quantité x prix : 2 x 10 + 3 x 20 = 20 + 60 = 80.
    resultat = transformer(donnees_exemple())
    assert resultat["montant"].sum() == 80.0


def test_agregation_par_ville():
    # Lyon (60) doit arriver avant Paris (20), car le tri est décroissant.
    resultat = agreger_par_ville(transformer(donnees_exemple()))
    assert resultat.iloc[0]["ville"] == "Lyon"
    assert resultat.iloc[0]["montant"] == 60.0


def test_agregation_par_categorie():
    # 5e test (exercice) : chiffre d'affaires par catégorie.
    # Informatique = 1 x 100 + 3 x 50 = 250 ; Mobilier = 2 x 10 = 20.
    donnees = pd.DataFrame({
        "quantite": [1, 2, 3],
        "prix_unitaire": [100.0, 10.0, 50.0],
        "ville": ["Paris", "Lyon", "Lille"],
        "categorie": ["Informatique", "Mobilier", "Informatique"],
    })
    resultat = agreger_par_categorie(transformer(donnees))
    assert resultat.iloc[0]["categorie"] == "Informatique"
    assert resultat.iloc[0]["montant"] == 250.0
    assert resultat.iloc[1]["montant"] == 20.0