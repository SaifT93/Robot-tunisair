
import requests
from bs4 import BeautifulSoup
import smtplib
from datetime import datetime

# Configuration des critères de recherche
URL = "https://www.tunisair.com"  # Adapter avec l'URL exacte pour Paris-Djerba
PRIX_MAX_PAR_PERSONNE = 550  # euros
NB_PERSONNES = 3
VILLE_DEPART = "Paris"
VILLE_DESTINATION = "Djerba"
DATE_DEBUT = datetime(2025, 7, 18)
DATE_FIN = datetime(2025, 8, 25)
DUREE_MIN = 15  # jours

headers = {"User-Agent": "Mozilla/5.0"}

def verifier_disponibilite():
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')

    prix_elements = soup.select('.tripsummary-price-amount-text')
    date_elements = soup.select('.tripsummary-title.tripsummary-date.tripsummary-details span[aria-hidden="true"]')

    if len(date_elements) < 2 or not prix_elements:
        print("Impossible de récupérer les informations nécessaires.")
        return

    prix_total = float(prix_elements[0].text.strip().replace('€', '').replace(',', '.').replace(' ', ''))
    prix_par_personne = prix_total / NB_PERSONNES

    date_depart = datetime.strptime(date_elements[0].text.strip(), "%a %d %b %Y")
    date_retour = datetime.strptime(date_elements[1].text.strip(), "%a %d %b %Y")

    duree_sejour = (date_retour - date_depart).days

    if DATE_DEBUT <= date_depart <= DATE_FIN and duree_sejour >= DUREE_MIN and prix_par_personne <= PRIX_MAX_PAR_PERSONNE:
        envoyer_notification(prix_total, prix_par_personne, date_depart, date_retour)

def envoyer_notification(prix_total, prix_par_personne, date_depart, date_retour):
    serveur = smtplib.SMTP('smtp.gmail.com', 587)
    serveur.starttls()
    serveur.login('ake54846@gmail.com', 'Tuto7575#')  # Utilise des identifiants sécurisés

    sujet = f'🚨 Offre Paris-Djerba à saisir rapidement !'
    corps_message = (f"Vol aller-retour {VILLE_DEPART}-{VILLE_DESTINATION} pour {NB_PERSONNES} personnes disponible à {prix_total}€ (soit {prix_par_personne:.2f}€ par personne).
"
                     f"Dates : du {date_depart.strftime('%d/%m/%Y')} au {date_retour.strftime('%d/%m/%Y')}
"
                     f"Lien : {URL}")

    message = f"Subject: {sujet}

{corps_message}"

    serveur.sendmail('ake54846@gmail.com', 'ake54846@gmail.com', message.encode('utf-8'))
    serveur.quit()
    print("Notification envoyée avec succès !")

# Exécute la vérification
if __name__ == "__main__":
    verifier_disponibilite()
