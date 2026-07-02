import logging
import os
from src.account_repository import AccountRepository
from src.payment_service import PaymentService

# Configuration du logger pour une meilleure gestion
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# --- Fonction d'entrée refactorisée ---
def process_payment(user_id, amount, card_number, db_path='paycore_prod.db'):
    account_repo = AccountRepository(db_path)
    payment_service = PaymentService(account_repo)
    return payment_service.process_payment(user_id, amount, card_number)
