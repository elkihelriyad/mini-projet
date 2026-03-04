# Sécurité et Authentification - Manuel d'Installation

## Prérequis
*   Python 3.8+
*   Dépendances : `flask`, `werkzeug`, `sqlite3`

## Installation
1.  Installer les dépendances :
    ```bash
    pip install -r requirements.txt
    ```
    (Assurez-vous que `Werkzeug` est présent).

2.  Initialiser la Base de Données et les Hashs :
    Si vous partez d'une base vide ou existante avec des codes en clair, lancez le script de seed :
    ```bash
    python seed_users.py
    ```
    *Ce script met à jour les comptes de test (o.elmessaoudi, r.elkihel, a.haloubi) avec des versions hachées de leurs codes.*

## Tests
Une suite de tests unitaires dédiés à l'authentification est disponible :
```bash
python tests_auth.py
```
Si les tests passent (`OK`), le système de login fonctionne correctement.

## Configuration
Dans `app.py`, les paramètres de sécurité suivants sont configurés :
*   `PERMANENT_SESSION_LIFETIME = 7 jours`
*   `SESSION_COOKIE_HTTPONLY = True`
*   `SESSION_COOKIE_SAMESITE = Lax`

En production, changez `app.secret_key` par une variable d'environnement aléatoire.
