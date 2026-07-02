# Spécification API Payment - PayCore v2

## Endpoint : `/charge`
Interface de facturation sécurisée.

### Contrat de données (Payload) :
- `amount` (float) : Montant strictement positif.
- `currency` (str) : Devise au standard ISO 4217 (ex: "EUR").
- `source_token` (str) : Jeton de tokenisation (PCI-DSS compliant).

### Matrice des codes de retour :
- `400` : Bad Request (Validation du payload échouée).
- `402` : Payment Required (Provision insuffisante).
- `403` : Forbidden (Rejet par le moteur de scoring de fraude).
