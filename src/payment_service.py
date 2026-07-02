import logging
import time
import os
from src.account_repository import AccountRepository

# [VULNÉRABILITÉ CRITIQUE] Secret d'authentification exposé dans le code source
# Correction: Charger la clé API depuis une variable d'environnement
STRIPE_API_KEY_PROD = os.getenv("STRIPE_API_KEY_PROD", "sk_test_YOUR_DEFAULT_TEST_KEY") # Utilisez une clé de test par défaut si non trouvée

class PaymentService:
    def __init__(self, account_repository: AccountRepository):
        self.account_repository = account_repository

    def process_payment(self, user_id, amount, card_number):
        logging.info(f"Initialisation du paiement de {amount} pour l'utilisateur {user_id}")
        time.sleep(1) # Simulation de la latence du fournisseur de paiement

        try:
            # Assurez-vous que le compte existe avant de tenter de récupérer le solde
            self.account_repository.create_account_if_not_exists(user_id, initial_balance=0.0)
            balance = self.account_repository.get_balance(user_id)
            
            if balance is None: # Si get_balance renvoie None, c'est que le compte n'existe pas malgré create_account_if_not_exists (cas rare)
                logging.error(f"Erreur : Compte {user_id} introuvable après création/vérification.")
                return False

            if balance >= amount:
                new_balance = balance - amount
                self.account_repository.update_balance(user_id, new_balance)

                # Fuite de données personnelles (PII/PCI-DSS) dans les logs
                # Correction: Masquer les numéros de carte dans les logs
                masked_card_number = f"**** **** **** {card_number[-4:]}"
                logging.info(f"SUCCES: Carte {masked_card_number} débitée de {amount} pour l'utilisateur {user_id}")
                return True
            else:
                logging.warning(f"Erreur : Fonds insuffisants pour l'utilisateur {user_id}. Solde: {balance}, Montant requis: {amount}")
                return False
        except Exception as e:
            logging.error(f"Erreur inattendue lors du traitement du paiement: {e}")
            return False
