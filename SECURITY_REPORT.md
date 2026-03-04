# Rapport de Sécurité et Correctifs d'Authentification

## 1. Résumé des Correctifs
Le système d'authentification a été refondu pour corriger les problèmes bloquants et améliorer la sécurité :

*   **Correction du Login** : Le formulaire de connexion soumet désormais correctement les données au serveur. La boucle infinie "En train de se connecter" a été résolue en corrigeant le JavaScript qui bloquait l'événement `submit`.
*   **Sécurisation des Mots de Passe** : Les codes d'accès ne sont plus comparés en clair. Nous utilisons désormais `Werkzeug.security` (PBKDF2/Scrypt) pour hacher et vérifier les codes.
*   **Persistance de Session** : La session Flask est configurée pour être permanente (durée de 7 jours) et sécurisée (`HttpOnly`, `SameSite=Lax`).
*   **Sauvegarde des Résultats** : Le flux "Test -> Connexion -> Sauvegarde" est implémenté. Si un utilisateur passe le test avant de se connecter, ses résultats sont temporairement stockés en session puis enregistrés en base de données dès la connexion réussie.

## 2. Risques Identifiés et Atténués
*   **Stockage en Clair (Critique)** : 
    *   *Avant* : Codes stockés en clair. Risque de fuite massive.
    *   *Après* : Codes hachés. Risque mitigé (nécessite bruteforce coûteux pour casser les hashs).
*   **Blocage UI Login (Majeur)** :
    *   *Avant* : Bouton bloqué, UX cassée.
    *   *Après* : Gestion d'erreur fluide, feedback visuel (secousse), soumission fiable.

## 3. Recommandations Futures (Phase Suivante)
1.  **Protection CSRF** : Ajouter un token CSRF complet sur tous les formulaires POST pour prévenir les attaques Cross-Site Request Forgery. Actuellement, la protection repose sur `SameSite=Lax`.
2.  **Rate Limiting** : Implémenter une limite de tentatives (ex: 5 essais / 15 min) pour bloquer les attaques par force brute sur les codes d'accès.
3.  **Rotation des Codes** : Permettre aux étudiants de changer leur code d'accès par défaut pour un mot de passe personnel.
4.  **HTTPS** : Forcer le flag `Secure` sur les cookies en production (déjà préparé dans `app.py`).

## 4. Instructions de Migration
Le script `seed_users.py` a été exécuté pour mettre à jour les comptes de test avec des hashs. Pour tout nouveau déploiement :
1.  Initialiser la DB : `python -c "from app import init_db; init_db()"`
2.  Peupler/Migrer les utilisateurs : `python seed_users.py`
